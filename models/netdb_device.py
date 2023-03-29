
from .netdb_column      import netdbColumn
from schema.device      import *

class netdbDevice(netdbColumn):

    _COLUMN     = 'device'

    def filter(self, filt):
        if not filt:
            pass

        elif isinstance(filt, list):
            if len(filt) == 4:
                if filt[0]:
                    self._FILT = { 'id': filt[0] }

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

        for top_id, device in self.data.items():
            try:
                deviceSchema().load(device)
            except ValidationError as error:
                return { 'result': False, 'comment': '%s: invalid data' % top_id, 'out': error.messages }

        return { 'result': True, 'comment': '%s - all checks passed' }
