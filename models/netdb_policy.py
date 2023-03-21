
from models.netdb_column import netdbColumn
from models.netdb_device import netdbDevice
from util.mongo_api      import MongoAPI

class netdbPolicy(netdbColumn):

    _COLUMN     = 'policy'
    _ELEMENT_ID = netdbColumn.ELEMENT_ID[_COLUMN]

    CATEGORIES  = {
            'route_map'   :  [], 
            'prefix_list' :  [], 
            }

    _TO_MONGO = {
            'prefix_lists' : 'prefix_list',
            'route_maps'   : 'route_map',
            }

    _FROM_MONGO = {
            'prefix_list' : 'prefix_lists',
            'route_map'   : 'route_maps',
            '_roles'      : 'roles',
            }

    def __init__(self, data = {}):
        self.data = data
        self.mongo = MongoAPI( netdbColumn.DB_NAME, self._COLUMN )


    def to_mongo(self):
        out = []

        for config_set, categories in self.data.items():
            if config_set.startswith('_'):
                entry = {
                        'set_id'     : config_set,
                        'category'   : '_roles',
                        'roles'      : categories['roles'],
                        }
                out.append(entry)

            for category, contents in categories.items():
                if category in ['prefix_lists', 'route_maps']:
                    for family, items in contents.items():
                        for item, elements in items.items():
                            entry = { 
                                    'set_id'          : config_set,
                                    'category'        : self._TO_MONGO[category],
                                    'family'          : family,
                                    self._ELEMENT_ID  : item,
                                    }

                            if not config_set.startswith('_'):
                                entry.update({ 'id' : config_set })

                            entry.update(elements)
                            out.append(entry)

                elif category in ['aspath_lists', 'community_lists']:
                    entry = { 
                            'set_id'         : config_set,
                            'category'       : self._TO_MONGO[category],
                            self._ELEMENT_ID : "%s.%s" % (config_set, category),
                            }

                    if not config_set.startswith('_'):
                       entry.update({ 'id' : config_set })

                    entry.update(elements)
                    out.append(entry)
        return out


    def from_mongo(self, data):
        out = {}

        for element in data:
            config_set = element.pop('set_id')
            if config_set not in out:
                out[config_set] = {}

            category = element.pop('category')
            new_cat  = self._FROM_MONGO[category]

            if category in ['prefix_list', 'route_map']:
                family = element.pop('family')
                elem   = element.pop('element_id')

                if new_cat not in out[config_set]:
                    out[config_set][new_cat] = {}

                if family not in out[config_set][new_cat]:
                    out[config_set][new_cat][family] = {}
                    
                out[config_set][new_cat][family][elem] = element

            elif category in ['aspath_list', 'community_list']:
                element.pop('element_id', None)
                out[config_set][new_cat] = element

            elif category == '_roles':
                out[config_set]['roles'] = element['roles']

            else:
                out = {}

        self.data = out


    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        devices     = netdbDevice().fetch( filt = {} )['out']
        config_sets = netdbPolicy().fetch( filt = {} )['out']

        for top_id, categories in self.data.items():

            if top_id in config_sets.keys():
                return { 'result': False, 'comment': "%s: config set already exists" % top_id }

            if top_id.startswith('_'):
                if 'roles' not in categories.keys():
                    return { 'result': False, 'comment': "%s: roles required for shared config set" % top_id }

            elif top_id not in devices.keys():
                return { 'result': False, 'comment': "%s: device not registered" % top_id }

            for category, contents in categories.items():
                if category in ['prefix_lists', 'route_maps']:
                    for family, items in contents.items():
                        if family not in ['ipv4', 'ipv6']:
                            return { 'result': False, 'comment': "%s.%s: family must me either ipv4 or ipv6" % (top_id, category) }
                        for element, elem_data in items.items():
                            if 'rules' not in elem_data:
                                return { 'result': False, 'comment': "%s.%s.%s: only rules element should be set" % (top_id, category, element) }
                            for rule in elem_data['rules']:
                                # Needs to be a schema
                                for key in rule.keys():
                                    if category == 'route_maps':
                                        if key not in ['action', 'continue', 'match', 'number', 'set']:
                                            return { 'result': False, 'comment': "%s.%s.%s: rules key invalid" % (top_id, category, element) }
                                    else:
                                        if key not in ['prefix', 'ge', 'le']:
                                            return { 'result': False, 'comment': "%s.%s.%s: rules key invalid" % (top_id, category, element) }

                elif category in ['aspath_lists', 'community_lists']:
                    for element, elem_data in contents.items():
                        if 'rules' not in elem_data:
                            return { 'result': False, 'comment': "%s.%s.%s: only rules element should be set" % (top_id, category, element) }
                        for rule in elem_data['rules']:
                            # Needs to be a schema
                            for key in rule.keys():
                                if key not in ['action', 'description', 'regex']:
                                    return { 'result': False, 'comment': "%s.%s.%s: rules key invalid" % (top_id, category, element) }

                elif top_id.startswith('_') and category == 'roles':
                    if not isinstance(contents, list):
                        return { 'result': False, 'comment': "%s: roles must be a list" % top_id }

                else:
                    return { 'result': False, 'comment': "%s: invalid category found" % top_id}

        return { 'result': True, 'comment': "%s - all checks passed" % top_id }
