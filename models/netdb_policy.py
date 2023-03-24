
from .netdb_column      import netdbColumn
#from .netdb_device      import netdbDevice

class netdbPolicy(netdbColumn):

    _COLUMN     = 'policy'

    _COLUMN_CAT  = {
            'type_1'   :  [ 'prefix_lists', 'route_maps' ],
            'type_2'   :  [ 'aspath_lists', 'community_lists' ],
            'type_3'   :  [],
            }

    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        for top_id, categories in self.data.items():

            if top_id.startswith('_'):
                if 'roles' not in categories.keys():
                    return { 'result': False, 'comment': "%s: roles required for shared config set" % top_id }

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