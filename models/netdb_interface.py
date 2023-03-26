
from .netdb_column      import netdbColumn
from schema.interface   import *

class netdbInterface(netdbColumn):

    _COLUMN     = 'interface'

    _COLUMN_CAT  = {
            'type_1'   :  [],
            'type_2'   :  [ 'interfaces' ],
            'type_3'   :  [],
            }


    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        for top_id, interfaces in self.data.items():
            if top_id.startswith('_'):
                if 'roles' not in config_data:
                    return { 'result': False, 'comment': "%s: roles required for shared config set" % top_id }
            try:
                interfacesSchema().load(interfaces)
            except ValidationError as error:
                return { 'result': False, 'comment': '%s: invalid data' % top_id, 'out': error.messages }

        return { 'result': True, 'comment': '%s: all checks passed' % top_id }
