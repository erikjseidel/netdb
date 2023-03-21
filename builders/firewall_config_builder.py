
from builders.config_builder import configBuilder
from models.netdb_firewall   import netdbFirewall
from models.netdb_device     import netdbDevice

class firewallConfigBuilder(configBuilder):

    def __init__(self, device_id):
        configBuilder.__init__(self, device_id)
        self.data = netdbFirewall().fetch(self._DATA_FILT)['out']
