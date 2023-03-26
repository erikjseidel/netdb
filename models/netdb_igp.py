
from .netdb_column      import netdbColumn

class netdbIgp(netdbColumn):

    _COLUMN     = 'igp'

    _COLUMN_CAT  = {
            'type_1'   :  [],
            'type_2'   :  [],
            'type_3'   :  [ 'isis' ],
            }
