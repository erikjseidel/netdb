
from builders.config_builder import configBuilder
from models.netdb_igp        import netdbIgp
from models.netdb_device     import netdbDevice

class igpConfigBuilder(configBuilder):

    def __init__(self, device_id):
        self.device_id = device_id
        self.device    = netdbDevice().fetch({ "id": device_id})['out']
        self.igp       = netdbIgp().fetch()['out']


    def build(self):
        config = {}

        device_id = self.device_id

        if device_id not in self.device.keys():
            return { 'result': False, 'comment': 'Device not found.' }

        if 'iso' not in self.device[device_id].keys():
            return { 'result': False, 'comment': 'No ISO address found for this router.' }


        if 'roles' in self.device[device_id]:
            roles = self.device[device_id]['roles']

            for igp_set, set_data in self.igp.items():
                if not igp_set.startswith('_'):
                    continue

                for role in set_data['roles']:
                    if role in roles:
                        config.update(set_data)
                        break

        if device_id in self.igp:
            config.update(self.igp[device_id])

        config['iso'] = self.device[device_id]['iso']

        config.pop('id', None)

        out = {}
        out[self.device_id] = config

        return { 'result': True, 'comment': 'igp configuration generated', 'out': out }
                
