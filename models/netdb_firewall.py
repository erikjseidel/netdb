
from models.netdb_column import netdbColumn
from models.netdb_device import netdbDevice
from util.mongo_api      import MongoAPI

class netdbFirewall(netdbColumn):

    _COLUMN     = 'firewall'
    _ELEMENT_ID = netdbColumn.ELEMENT_ID[_COLUMN]

    CATEGORIES  = {
            'options'      :  [],
            'zone_policy'  :  [ 'zone' ],
            'state_policy' :  [], 
            'policy'       :  [], 
            'group'        :  [ 'network' ],
            }

    _TO_MONGO = {
            'policies'     : 'policy',
            'groups'       : 'group',
            'zone_policy'  : 'zone_policy',
            'state_policy' : 'state_policy',
            'options'      : 'option_set',
            }

    _FROM_MONGO = {
            'policy'       : 'policies',
            'group'        : 'groups',
            'zone_policy'  : 'zone_policy',
            'state_policy' : 'state_policy',
            'option_set'   : 'options',
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
                        'roles'      : config_set['roles'],
                        }
                out.append(entry)

            for category, contents in categories.items():
                if category in ['policies', 'groups']:
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

                elif category == 'zone_policy':
                    for item, elements in contents['zone'].items():
                        entry = { 
                                'set_id'         : config_set,
                                'category'       : self._TO_MONGO[category],
                                'type'           : 'zone',
                                self._ELEMENT_ID : item,
                                }

                        if not config_set.startswith('_'):
                            entry.update({ 'id' : config_set })

                        entry.update(elements)
                        out.append(entry)

                elif category in ['options', 'state_policy']:
                    entry = { 
                            'set_id'         : config_set,
                            'category'       : self._TO_MONGO[category],
                            self._ELEMENT_ID : "%s.%s" % (config_set, category),
                            }

                    if not config_set.startswith('_'):
                        entry.update({ 'id' : config_set })

                    entry.update(category)
                    out.append(entry)

                else:
                    return None

        return out


    def from_mongo(self, data):
        out = {}

        for element in data:
            config_set = element.pop('set_id')
            if config_set not in out:
                out[config_set] = {}

            category = element.pop('category')

            if category in ['policy', 'group']:
                family = element.pop('family')
                elem   = element.pop('element_id')

                if category not in out[config_set]:
                    out[config_set][self._FROM_MONGO[category]] = {}

                if family not in out[config_set][category]:
                    out[config_set][self._FROM_MONGO[category]][family] = {}
                    
                out[config_set][category][family][elem] = element

            elif category in ['zone_policy']:
                elem_type = element.pop['type']
                elem      = element.pop['element_id']

                if category not in out[config_set]:
                    out[config_set][self._FROM_MONGO[category]] = {}

                if elem_type not in out[config_set][category]:
                    out[config_set][self._FROM_MONGO[category]][elem_type] = {}

                out[config_set][category][elem_type][elem] = element

            elif category in ['option_set', 'state_policy']:
                out[config_set][self._FROM_MONGO[category]] = element

            elif category == '_roles':
                out[config_set]['roles'] = element['roles']

            else:
                out = {}

        self.data = out


    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        devices     = netdbDevice().fetch( filt = {} )['out']
        config_sets = netdbFirewall().fetch( filt = {} )['out']

        for top_id, categories in self.data.items():

            if top_id in config_sets.keys():
                return { 'result': False, 'comment': "%s: config set already exists" % top_id }

            if top_id.startswith('_'):
                if 'roles' not in config_data:
                    return { 'result': False, 'comment': "%s: roles required for shared config set" % top_id }

            elif top_id not in devices.keys():
                return { 'result': False, 'comment': "%s: device not registered" % top_id }

            for category, contents in categories.items():
                if category in ['policies', 'groups']:
                    for family, items in category.items():
                        if family not in ['ipv4', 'ipv6']:
                            return { 'result': False, 'comment': "%s.%s: family must me either ipv4 or ipv6" % (top_id, category) }


                elif category == 'zone_policy':
                    if 'zone' not in contents:
                        return { 'result': False, 'comment': "%s.%s: zone node required" % (top_id, category) }
                    for item, elements in contents['zone'].items():
                        for element, elem_data in elements.items():
                            if element == 'interfaces' and not isinstance(elem_data, list):
                                return { 'result': False, 'comment': "%s.%s.%s.%s: must be a list" % (top_id, category, item, element) }
                            elif element == 'default_action' and elem_data not in ['drop', 'accept']:
                                return { 'result': False, 'comment': "%s.%s.%s.%s: must be drop or accept" % (top_id, category, item, element) }
                            elif element == 'from':
                                if not isinstance(elem_data, list):
                                    for zone in elem_data:
                                        if 'zone' not in zone:
                                            return { 'result': False, 'comment': "%s.%s.%s.%s: invalid from data" % (top_id, category, item, element) }
                            else:
                                return { 'result': False, 'comment': "%s.%s.%s.%s: invalid node" % (top_id, category, item, element) }

                elif category == 'state_policy':
                    for option, value in contents.items():
                        if option not in ['established', 'related'] or value not in ['accept', 'drop']:
                            return { 'result': False, 'comment': "%s.%s: invalid option or value" % (top_id, category) }

                elif category == 'options':
                    for option, value in contents.items():
                        if not isinstance(option, str) or not isinstance(value, str) or not isinstance(value, int):
                            return { 'result': False, 'comment': "%s.%s: invalid option or value" % (top_id, category) }

                elif top_id.startswith('_') and category == 'roles':
                    if not isinstance(contents, list):
                        return { 'result': False, 'comment': "%s: roles must be a list" % top_id }

                else:
                    return { 'result': False, 'comment': "%s: invalid category found" % top_id}

        return { 'result': True, 'comment': "%s - all checks passed" % top_id }

