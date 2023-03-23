
from models.netdb_column import netdbColumn
from util.mongo_api      import MongoAPI

class netdbDevice(netdbColumn):

    _COLUMN     = 'device'

    def __init__(self, data = {}):
        self.data = data
        self.mongo = MongoAPI( netdbColumn.DB_NAME, self._COLUMN )


    def to_mongo(self):
        out = []

        for device, elements in self.data.items():
            entry = { 'id' : device }
            entry.update(elements)

            out.append(entry)

        return out


    def from_mongo(self, data):
        out = {}

        for device in data:
            device_id  = device.pop('id')
            out[device_id] = device

        self.data = out


    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        devices = netdbDevice().fetch( filt = {} )['out']

        for top_id, device in self.data.items():
            if top_id.upper() in devices.keys():
                return { 'result': False, 'comment': "%s: already registered" % top_id }

            top_id = top_id.upper()

            if 'local_asn' not in device or not ( 1 <= int(device['local_asn']) <= 4000000000):
                return { 'result': False, 'comment': "%s - invalid local_asn" % top_id }

        return { 'result': True, 'comment': '%s - all checks passed' }

