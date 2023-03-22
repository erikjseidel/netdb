
from models.netdb_column import netdbColumn
from models.netdb_device import netdbDevice
from util.mongo_api      import MongoAPI

class netdbPolicy(netdbColumn):

    _COLUMN     = 'policy'

    _COLUMN_CAT  = {
            'type_1'   :  [ 'prefix_lists', 'route_maps' ],
            'type_2'   :  [ 'aspath_lists', 'community_lists' ],
            'type_3'   :  [],
            }

    _MONGO_CAT  = {
            'type_1'   :  [ 'prefix_list', 'route_map' ],
            'type_2'   :  [ 'aspath_list', 'community_list' ],
            'type_3'   :  [],
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
