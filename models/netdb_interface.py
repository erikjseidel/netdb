
from .netdb_column      import netdbColumn
from schema.interface   import *
from util.decorators    import netdb_internal

class netdbInterface(netdbColumn):
    _COLUMN     = 'interface'

    def _to_mongo(self, data):
        out = []

        for device_id, interfaces in data.items():
            for interface, contents in interfaces.items():
                entry = {
                        'set_id'     : device_id,
                        'element_id' : interface,
                        }
                entry.update(contents)
                out.append(entry)
        return out


    def _from_mongo(self, data):
        out = {}

        for element in data:
            config_set = element.pop('set_id')
            if config_set not in out:
                out[config_set] = {}

            elem = element.pop('element_id')
            out[config_set][elem] = element
        return out


    @netdb_internal
    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return False, None, 'invalid dataset'

        for device_id, device in self.data.items():
            for interface, contents in device.items():
                try:
                    interfaceSchema().load(contents)
                except ValidationError as error:
                    return False, error.messages, '%s: invalid data' % top_id

        return True, None, '%s - all checks passed'
