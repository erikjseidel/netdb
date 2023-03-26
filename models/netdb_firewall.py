
from .netdb_column      import netdbColumn
from schema.firewall    import *

class netdbFirewall(netdbColumn):

    _COLUMN     = 'firewall'

    _COLUMN_CAT  = {
            'type_1'   :  [ 'policies', 'groups' ],
            'type_2'   :  [ 'zone_policy' ],
            'type_3'   :  [ 'options', 'state_policy', 'mss_clamp' ],
            }


    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        for top_id, categories in self.data.items():

            if top_id.startswith('_'):
                if 'roles' not in categories.keys():
                    return { 'result': False, 'comment': "%s: roles required for shared config set" % top_id }
            try:
                firewallSchema().load(categories)
            except ValidationError as error:
                return { 'result': False, 'comment': '%s: invalid data' % top_id, 'out': error.messages }

        return { 'result': True, 'comment': '%s - all checks passed' }

