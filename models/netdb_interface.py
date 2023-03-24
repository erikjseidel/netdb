
from .netdb_column      import netdbColumn
from .netdb_device      import netdbDevice

class netdbInterface(netdbColumn):

    _COLUMN     = 'interface'

    _COLUMN_CAT  = {
            'type_1'   :  [],
            'type_2'   :  [ 'interfaces' ],
            'type_3'   :  [],
            }

    IFACE_TYPES = ['ethernet', 'vlan', 'lacp', 'dummy', 'gre', 'l2gre']

    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return { 'result': False, 'comment': 'invalid dataset' }

        for top_id, interfaces in self.data.items():
            if 'interfaces' not in interfaces:
                return { 'result': False, 'comment': "%s: interfaces set not found" % top_id }

            for iface, ifd in interfaces['interfaces'].items():
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

