
from .config_builder         import configBuilder
from models.netdb_firewall   import netdbFirewall

class firewallConfigBuilder(configBuilder, netdbFirewall):

    def __init__(self, device_id):
        configBuilder.__init__(self, device_id)
        self.data = netdbFirewall().filter(self._DATA_FILT).fetch()['out']
