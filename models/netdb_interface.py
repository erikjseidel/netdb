
from .netdb_column      import netdbColumn

class netdbInterface(netdbColumn):

    _COLUMN     = 'interface'

    _COLUMN_CAT  = {
            'type_1'   :  [],
            'type_2'   :  [ 'interfaces' ],
            'type_3'   :  [],
            }
