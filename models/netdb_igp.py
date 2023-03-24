
from .netdb_column      import netdbColumn
from .netdb_device      import netdbDevice

class netdbIgp(netdbColumn):

    _COLUMN     = 'igp'

    _COLUMN_CAT  = {
            'type_1'   :  [],
            'type_2'   :  [],
            'type_3'   :  [ 'isis' ],
            }

    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        for top_id, config_data in self.data.items():
            if top_id.startswith('_'):
                if 'roles' not in config_data:
                    return { 'result': False, 'comment': "%s: roles required for shared config set" % top_id }

        return { 'result': True, 'comment': '%s - all checks passed' % top_id }


