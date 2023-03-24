
from .netdb_column      import netdbColumn
from .netdb_device      import netdbDevice
from util.mongo_api     import MongoAPI

class netdbFirewall(netdbColumn):

    _COLUMN     = 'firewall'

    _COLUMN_CAT  = {
            'type_1'   :  [ 'policies', 'groups' ],
            'type_2'   :  [ 'zone_policy' ],
            'type_3'   :  [ 'options', 'state_policy', 'mss_clamp' ],
            }

    def __init__(self, data = {}):
        self.data = data
        self.mongo = MongoAPI( netdbColumn.DB_NAME, self._COLUMN )


    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        devices     = netdbDevice().fetch()['out']
        config_sets = netdbFirewall().fetch()['out']

        for top_id, categories in self.data.items():

            if top_id in config_sets.keys():
                return { 'result': False, 'comment': "%s: config set already exists" % top_id }

            if top_id.startswith('_'):
                if 'roles' not in categories.keys():
                    return { 'result': False, 'comment': "%s: roles required for shared config set" % top_id }

            elif top_id not in devices.keys():
                return { 'result': False, 'comment': "%s: device not registered" % top_id }

            for category, contents in categories.items():
                if category in ['policies', 'groups']:
                    for family, items in contents.items():
                        if family not in ['ipv4', 'ipv6']:
                            return { 'result': False, 'comment': "%s.%s: family must me either ipv4 or ipv6" % (top_id, category) }

                elif category == 'zone_policy':
                    for item, elements in contents.items():
                        for element, elem_data in elements.items():
                            if element == 'interfaces':
                                if not isinstance(elem_data, list):
                                    return { 'result': False, 'comment': "%s.%s.%s.%s: must be a list" % (top_id, category, item, element) }
                            elif element == 'default_action':  
                                if elem_data not in ['drop', 'accept']:
                                    return { 'result': False, 'comment': "%s.%s.%s.%s: must be drop or accept" % (top_id, category, item, element) }
                            elif element == 'from':
                                if not isinstance(elem_data, list):
                                    for zone in elem_data:
                                        if 'zone' not in zone:
                                            return { 'result': False, 'comment': "%s.%s.%s.%s: invalid from data" % (top_id, category, item, element) }
                            else:
                                return { 'result': False, 'comment': "%s.%s.%s.%s: HERE invalid node" % (top_id, category, item, element) }

                elif category == 'state_policy':
                    for option, value in contents.items():
                        if option not in ['established', 'related'] or value not in ['accept', 'drop']:
                            return { 'result': False, 'comment': "%s.%s.%s: invalid key or value" % (top_id, category, option) }

                elif category == 'options':
                    for option, value in contents.items():
                        if not isinstance(value, str) and not isinstance(value, int):
                            return { 'result': False, 'comment': "%s.%s.%s: invalid key or value" % (top_id, category, option) }

                elif category == 'mss_clamp':
                    for option, value in contents.items():
                        if option not in ['ipv4', 'ipv6', 'interfaces']:
                            return { 'result': False, 'comment': "%s.%s.%s: invalid key" % (top_id, category, option) }
                        if option == 'interfaces' and not isinstance(value, list):
                            return { 'result': False, 'comment': "%s.%s.%s: invalid value" % (top_id, category, option) }

                elif top_id.startswith('_') and category == 'roles':
                    if not isinstance(contents, list):
                        return { 'result': False, 'comment': "%s: roles must be a list" % top_id }

                else:
                    return { 'result': False, 'comment': "%s: invalid category found" % top_id}

        return { 'result': True, 'comment': "%s - all checks passed" % top_id }

