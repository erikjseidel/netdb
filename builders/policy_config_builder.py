
from builders.config_builder import configBuilder
from models.netdb_policy     import netdbPolicy
from models.netdb_device     import netdbDevice

class policyConfigBuilder(configBuilder):

    _DEV_AVAIL = True

    def __init__(self, device_id):
        self.device_id = device_id
        devices        = netdbDevice().fetch({ "id": device_id})['out']
        if device_id in devices:
            self.device    = netdbDevice().fetch({ "id": device_id})['out'][device_id]
        else:
            self._DEV_AVAIL = False
            return

        self.data      = netdbPolicy().fetch()['out']

        # build the cvars dict
        self.cvars = {}
        if 'cvars' in self.device:
            for cvar, value in self.device['cvars'].items():
                self.cvars.update({ "_cvar." + cvar : value })


    def build(self):

        if not self._DEV_AVAIL:
            return { 'result': False, 'comment': 'Device not found.' }

        config = {}

        device_id = self.device_id

        roles = []
        if 'roles' in self.device:
            roles = self.device['roles']

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

        # Set the cvars
        out = self._dict_replace_values(config, self.cvars) 

        return { 'result': True, 'comment': 'policy configuration generated', 'out': out }
