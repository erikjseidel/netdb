
from .netdb_column      import netdbColumn

class netdbBgp(netdbColumn):

    _COLUMN     = 'bgp'

    _COLUMN_CAT  = {
            'type_1'   :  [ 'address_family' ],
            'type_2'   :  [ 'peer_groups', 'neighbors' ],
            'type_3'   :  [ 'options' ],
            }

    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        for top_id, categories in self.data.items():

            if top_id.startswith('_'):
                if 'roles' not in categories.keys():
                    return { 'result': False, 'comment': "%s: roles required for shared config set" % top_id }

            for category, contents in categories.items():
                if category == 'address_family':
                    for family, items in contents.items():
                        if family not in ['ipv4', 'ipv6']:
                            return { 'result': False, 'comment': "%s.%s: family must me either ipv4 or ipv6" % (top_id, category) }

                elif category in ['peer_groups', 'neighbors']:
                    for element, elem_data in contents.items():
                        if category == 'peer_groups':
                            for i in elem_data.keys():
                                if i not in ['family', 'type', 'remote_asn', 'source', 'password', 'multihop']:
                                    return { 'result': False, 'comment': "%s.%s.%s: invalid peer_group key" % (top_id, category, element) }
                        else:
                            for i in elem_data.keys():
                                if i not in ['peer_group', 'family', 'type', 'remote_asn']:
                                    return { 'result': False, 'comment': "%s.%s.%s: invalid neighbor key" % (top_id, category, element) }

                elif category == 'options':
                    for option, value in contents.items():
                        if not isinstance(value, str) and not isinstance(value, int):
                            return { 'result': False, 'comment': "%s.%s.%s: invalid key or value" % (top_id, category, option) }

                elif top_id.startswith('_') and category == 'roles':
                    if not isinstance(contents, list):
                        return { 'result': False, 'comment': "%s: roles must be a list" % top_id }

                else:
                    return { 'result': False, 'comment': "%s.%s: invalid category found" % (top_id, category) }

        return { 'result': True, 'comment': "%s - all checks passed" % top_id }
