
from .netdb_column      import netdbColumn

class netdbFirewall(netdbColumn):

    _COLUMN     = 'firewall'

    _COLUMN_CAT  = {
            'type_1'   :  [ 'policies', 'groups' ],
            'type_2'   :  [ 'zone_policy' ],
            'type_3'   :  [ 'options', 'state_policy', 'mss_clamp' ],
            }
