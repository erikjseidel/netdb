
from .netdb_column      import netdbColumn
from schema.policy      import *

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

            try:
                policySchema().load(categories)
            except ValidationError as error:
                return { 'result': False, 'comment': '%s: invalid data' % top_id, 'out': error.messages }

        return { 'result': True, 'comment': "%s: all checks passed" % top_id }
