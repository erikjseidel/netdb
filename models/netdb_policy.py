
from .netdb_column      import netdbColumn

class netdbPolicy(netdbColumn):

    _COLUMN     = 'policy'

    _COLUMN_CAT  = {
            'type_1'   :  [ 'prefix_lists', 'route_maps' ],
            'type_2'   :  [ 'aspath_lists', 'community_lists' ],
            'type_3'   :  [],
            }
