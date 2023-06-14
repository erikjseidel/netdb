from models.models import netdbDevice
from util.decorators import netdb_provider

class configBuilder:

    _DEV_AVAIL = True

    def __init__(self, device_id):
        self._DATA_FILT = { 
                '$or': [ 
                    { 'set_id':     device_id }, 
                    { 'set_id': { '$regex': '^_' } }, 
                    { 'roles':  { '$exists': True } } 
                    ] 
                }

        self.device_id = device_id
        netdb_answer = netdbDevice().filter(device_id).fetch()

        devices = {}
        if netdb_answer['result']:
            devices = netdb_answer['out']

        if device_id in devices:
            self.device    = devices[device_id]
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


    @netdb_provider
    def build(self):
        if not self._DEV_AVAIL:
            return False, None, 'Device not found.'

        device_id = self.device_id
        config = {}
        out = None

        roles = []
        if 'roles' in self.device:
            roles = self.device['roles']


        def merge_config(data):
            for category, contents in data.items():
                if category in self._COLUMN_CAT['type_1']:
                    for family in ['ipv4', 'ipv6']:
                        if family in contents:
                            for element, elem_data in contents[family].items():
                                unwind = config
                                for i in [ category, family ]:
                                    if not unwind.get(i):
                                        unwind[i] = {}
                                    unwind = unwind[i]
                                config[category][family][element] = elem_data

                elif category in self._COLUMN_CAT['type_2']:
                    for element, elem_data in contents.items():
                        if category not in config:
                            config[category] = {}

                        config[category][element] = elem_data

                # type_3 categories are merged.
                elif category in self._COLUMN_CAT['type_3']:
                    if category in config:
                        config[category].update(contents)
                    else:
                        config[category] = contents


        if self.data:
            for config_set, set_data in self.data.items():
                if not config_set.startswith('_'):
                    continue

                for role in set_data['roles']:
                    if role in roles or role == '*':
                        set_data.pop('roles', None)
                        merge_config(set_data)
                        break

            if device_id in self.data:
                merge_config(self.data[device_id])

            # Set the cvars
            out = self._dict_replace_values(config, self.cvars)

        if not out:
            return False, None, 'No column data found for %s' % device_id

        return True, { device_id : out }, 'config column generated for %s' % device_id
