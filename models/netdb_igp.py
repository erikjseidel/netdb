
from models.netdb_column import netdbColumn
from models.netdb_device import netdbDevice
from util.mongo_api      import MongoAPI

class netdbIgp(netdbColumn):

    _COLUMN     = 'igp'

    _COLUMN_CAT  = {
            'type_1'   :  [],
            'type_2'   :  [],
            'type_3'   :  [ 'isis' ],
            }

    _MONGO_CAT  = {
            'type_1'   :  [],
            'type_2'   :  [],
            'type_3'   :  [ 'isis' ],
            }

    _TO_MONGO = {
            'isis' : 'isis',
            }

    _FROM_MONGO = {
            'isis' : 'isis',
            '_roles'     : 'roles',
            }

    def __init__(self, data = {}):
        self.data = data
        self.mongo = MongoAPI( netdbColumn.DB_NAME, self._COLUMN )


    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        devices     = netdbDevice().fetch( filt = {} )['out']
        config_sets = netdbIgp().fetch( filt = {} )['out']

        for top_id, config_data in self.data.items():
            if top_id in config_sets.keys():
                return { 'result': False, 'comment': "%s: config set already exists" % top_id }

            if top_id.startswith('_'):
                if 'roles' not in config_data:
                    return { 'result': False, 'comment': "%s: roles required for shared config set" % top_id }

            elif top_id not in devices.keys():
                return { 'result': False, 'comment': "%s: device not registered" % top_id }

        return { 'result': True, 'comment': '%s - all checks passed' % top_id }


