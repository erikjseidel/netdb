from schema.device import *
from schema.interface import *
from util.decorators import netdb_internal
from .column import netdbColumn

class netdbBgp(netdbColumn):
    _COLUMN     = 'bgp'

    _COLUMN_CAT  = {
            'type_1'   :  [ 'address_family' ],
            'type_2'   :  [ 'peer_groups', 'neighbors' ],
            'type_3'   :  [ 'options' ],
            }


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
            if device_id in out:
                if out[device_id].get('weight', 0) > device.get('weight', 0):
                    continue

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


class netdbFirewall(netdbColumn):
    _COLUMN     = 'firewall'

    _COLUMN_CAT  = {
            'type_1'   :  [ 'policies', 'groups' ],
            'type_2'   :  [ 'zone_policy' ],
            'type_3'   :  [ 'options', 'state_policy', 'mss_clamp' ],
            }


class netdbIgp(netdbColumn):
    _COLUMN     = 'igp'

    _COLUMN_CAT  = {
            'type_1'   :  [],
            'type_2'   :  [],
            'type_3'   :  [ 'isis' ],
            }


class netdbInterface(netdbColumn):
    _COLUMN     = 'interface'

    def _to_mongo(self, data):
        out = []

        for device_id, interfaces in data.items():
            for interface, contents in interfaces.items():
                entry = {
                        'set_id'     : [ device_id, interface ],
                        }
                entry.update(contents)
                out.append(entry)
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
                    return False, error.messages, '%s: invalid data' % device_id

        return True, None, '%s - all checks passed'


class netdbPolicy(netdbColumn):
    _COLUMN = 'policy'

    _COLUMN_CAT  = {
            'type_1'   :  [ 'prefix_lists', 'route_maps' ],
            'type_2'   :  [ 'aspath_lists', 'community_lists' ],
            'type_3'   :  [],
            }
