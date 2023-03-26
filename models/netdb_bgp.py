
from .netdb_column      import netdbColumn

class netdbBgp(netdbColumn):

    _COLUMN     = 'bgp'

    _COLUMN_CAT  = {
            'type_1'   :  [ 'address_family' ],
            'type_2'   :  [ 'peer_groups', 'neighbors' ],
            'type_3'   :  [ 'options' ],
            }
