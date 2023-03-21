
from models.netdb_device     import netdbDevice

class configBuilder:

    _DEV_AVAIL = True

    def __init__(self, device_id):

        self._DATA_FILT = { 
                '$or': [ 
                    { 'id':     device_id }, 
                    { 'set_id': { '$regex': '^_' } }, 
                    { 'roles':  { '$exists': True } } 
                    ] 
                }

        self.device_id = device_id
        devices        = netdbDevice().fetch({ "id": device_id})['out']

        if device_id in devices:
            self.device    = netdbDevice().fetch({ "id": device_id})['out'][device_id]
        else:
            self._DEV_AVAIL = False
            return

        # build the cvars dict
        self.cvars = {}
        if 'cvars' in self.device:
            for cvar, value in self.device['cvars'].items():
                self.cvars.update({ "_cvar." + cvar : value })


    def _dict_replace_values(self, d: dict, r: dict) -> dict:
        x = {}
        for k, v in d.items():
            if isinstance(v, dict):
                v = self._dict_replace_values(v, r)
            elif isinstance(v, list):
                v = self._list_replace_values(v, r)
            elif isinstance(v, str):
                for w in r.keys():
                    if v == w:
                        v = r[w]
            x[k] = v
        return x


    def _list_replace_values(self, l: list, r: dict) -> list:
        x = []
        for e in l:
            if isinstance(e, list):
                e = self._list_replace_values(e, r)
            elif isinstance(e, dict):
                e = self._dict_replace_values(e, r)
            elif isinstance(e, str):
                for w in r.keys():
                    if e == w:
                        e = r[w]
            x.append(e)
        return x


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

        return { 'result': True, 'comment': 'config column generated for %s' % device_id, 'out': out }
