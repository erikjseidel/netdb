
from models.netdb_column import netdbColumn
from models.netdb_device import netdbDevice
from util.mongo_api      import MongoAPI

class netdbIgp(netdbColumn):

    _COLUMN     = 'igp'
    _ELEMENT_ID = netdbColumn.ELEMENT_ID[_COLUMN]

    def __init__(self, data = {}):
        self.data = data
        self.mongo = MongoAPI( netdbColumn.DB_NAME, self._COLUMN )


    def to_mongo(self):
        out = []

        for config_set, elements in self.data.items():
            entry = { self._ELEMENT_ID : config_set }
            if not config_set.startswith('_'):
                entry.update({ 'id' : config_set })
            entry.update(elements)

            out.append(entry)

        return out


    def from_mongo(self, data):
        out = {}

        for config_set in data:
            set_id  = config_set.pop(self._ELEMENT_ID)
            out[set_id] = config_set

        self.data = out


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


