
from .netdb_column      import netdbColumn
from schema.device      import *
from util.decorators    import netdb_internal

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


    @netdb_internal
    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return False, None, 'invalid dataset'

        for top_id, device in self.data.items():
            try:
                deviceSchema().load(device)
            except ValidationError as error:
                return False, error.messages, '%s: invalid data' % top_id

        return True, None, '%s - all checks passed'
