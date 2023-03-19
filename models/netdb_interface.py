
from models.netdb_column import netdbColumn
from models.netdb_device import netdbDevice
from util.mongo_api      import MongoAPI

class netdbInterface(netdbColumn):

    _COLUMN     = 'interface'
    _ELEMENT_ID = netdbColumn.ELEMENT_ID[_COLUMN]

    IFACE_TYPES = ['ethernet', 'vlan', 'lacp', 'dummy', 'gre', 'l2gre']

    def __init__(self, data = {}):
        self.data = data
        self.mongo = MongoAPI( netdbColumn.DB_NAME, self._COLUMN )


    def to_mongo(self):
        out = []

        for device, elements in self.data.items():
            for element, contents in elements.items():
                entry = { 'id' : device, self._ELEMENT_ID : element }
                entry.update(contents)

                out.append(entry)

        return out


    def from_mongo(self, data):
        out = {}

        for entry in data:
            element_id  = entry.pop(self._ELEMENT_ID)
            device_id   = entry.pop('id')

            if device_id not in out:
                out[device_id] = {}

            out[device_id][element_id] = entry

        self.data = out


    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        devices = netdbDevice().fetch()['out']
        current_ifaces = netdbInterface().fetch()['out']

        for top_id, interfaces in self.data.items():
            if top_id.upper() not in devices.keys():
                return { 'result': False, 'comment': "id %s not a registered device" % top_id }

            for iface, ifd in interfaces.items():
                if top_id in current_ifaces and iface in current_ifaces[top_id].keys():
                    return { 'result': False, 'comment': "%s - already exists" % iface }

                if 'type' not in ifd or ifd['type'] not in self.IFACE_TYPES:
                    return { 'result': False, 'comment': "%s - invalid type" % iface }

                if ifd['type'] in ['gre', 'l2gre'] and not iface.startswith('tun'):
                    return { 'result': False, 'comment': "%s - tunnel iface invalid name" % iface }

                if ifd['type'] in ['ethernet'] and not iface.startswith('eth'):
                    return { 'result': False, 'comment': "%s - ethernet iface invalid name" % iface }

                if ifd['type'] in ['dummy'] and not iface.startswith('dum'):
                    return { 'result': False, 'comment': "%s - loopback iface invalid name" % iface }

                if ifd['type'] in ['lacp'] and not iface.startswith('bond'):
                    return { 'result': False, 'comment': "%s - lacp bundle invalid name" % iface }

                if ifd['type'] == 'vlan':
                    if 'vlan' not in ifd or 'id' not in ifd['vlan'] or 'parent' not in ifd['vlan']:
                        return { 'result': False, 'comment': "%s requires a vlan id and parent" % iface }

                if ifd['type'] == 'lacp':
                    if 'lacp' not in ifd:
                        return { 'result': False, 'comment': "%s is missing lacp settings" }
                    if 'hash_policy' not in ifd['lacp'] or ifd['lacp']['hash_policy'] not in ['layer3+4' or 'layer2+3']:
                        return { 'result': False, 'comment': "%s - invalid hash policy " }
                    if 'rate' not in ifd['lacp'] or ifd['lacp']['rate'] not in ['fast' or 'slow']:
                        return { 'result': False, 'comment': "%s - invalid hash policy" }
                    if 'members' not in ifd['lacp']:
                        return { 'result': False, 'comment': "%s - no lacp members found" }

        return { 'result': True, 'comment': '%s - all checks passed' }

