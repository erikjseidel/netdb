
from .netdb_column      import netdbColumn

class netdbDevice(netdbColumn):

    _COLUMN     = 'device'

    def filter(self, filt):
        if not filt:
            pass

        elif isinstance(filt, dict):
            self._FILT = filt

        else:
            self._FILT = { 'id': filt }

        return self


    def _to_mongo(self, data):
        out = []

        for device, elements in data.items():
            entry = { 'id' : device }
            entry.update(elements)

            out.append(entry)

        return out


    def _from_mongo(self, data):
        out = {}

        for device in data:
            device_id  = device.pop('id')
            out[device_id] = device

        return out


    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        devices = netdbDevice().fetch()['out']

        for top_id, device in self.data.items():
            if top_id.upper() in devices.keys():
                return { 'result': False, 'comment': "%s: already registered" % top_id }

            top_id = top_id.upper()

            if 'local_asn' not in device or not ( 1 <= int(device['local_asn']) <= 4000000000):
                return { 'result': False, 'comment': "%s - invalid local_asn" % top_id }

        return { 'result': True, 'comment': '%s - all checks passed' }

