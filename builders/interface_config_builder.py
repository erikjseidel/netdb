
from builders.config_builder import configBuilder
from models.netdb_interface  import netdbInterface

class interfaceConfigBuilder(configBuilder):

    def __init__(self, device_id, group = 'all'):
        configBuilder.__init__(self, device_id)

        filt = {
                'all'      :    { 'id': device_id },
                'tunnel'   :    { 'id': device_id, 'type': { '$in':  [ "gre", "l2gre" ] } },
                'ethernet' :    { 'id': device_id, 'type': { '$in':  [ "ethernet", "bond", "vlan" ] } },
                'loopback' :    { 'id': device_id, 'type': 'dummy' },
               }

        self.data = netdbInterface().fetch(filt[group])['out']
