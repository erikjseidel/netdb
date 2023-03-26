
from builders.config_builder import configBuilder
from models.netdb_interface  import netdbInterface

class interfaceConfigBuilder(configBuilder):

    def __init__(self, device_id, group = 'all'):
        configBuilder.__init__(self, device_id)

        filt = {
                'all'      :    { 'set_id': device_id },
                'tunnel'   :    { 'set_id': device_id, 'type': { '$in':  [ "gre", "l2gre" ] } },
                'ethernet' :    { 'set_id': device_id, 'type': { '$in':  [ "ethernet", "bond", "vlan" ] } },
                'loopback' :    { 'set_id': device_id, 'type': 'dummy' },
               }

        self.data = netdbInterface().filter(filt[group]).fetch()['out']
