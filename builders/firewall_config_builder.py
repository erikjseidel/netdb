
from builders.config_builder import configBuilder
from models.netdb_firewall   import netdbFirewall
from models.netdb_device     import netdbDevice

class firewallConfigBuilder(configBuilder):

    def __init__(self, device_id):
        self.device_id = device_id
        self.device    = netdbDevice().fetch({ "id": device_id})['out']
        self.data      = netdbFirewall().fetch()['out']


    def build(self):
        config = {}

        device_id = self.device_id

        if device_id not in self.device.keys():
            return { 'result': False, 'comment': 'Device not found.' }

        roles = []
        if 'roles' in self.device[device_id]:
            roles = self.device[device_id]['roles']

        for config_set, set_data in self.data.items():
            if not config_set.startswith('_'):
                continue

            for role in set_data['roles']:
                if role in roles or role == '*':
                    config.update({ config_set: set_data })
                    break

        if device_id in self.data:
            config.update({ device_id: self.data[device_id] })

        config.pop('id', None)

        out = config

        return { 'result': True, 'comment': 'firewall configuration generated', 'out': out }
                
