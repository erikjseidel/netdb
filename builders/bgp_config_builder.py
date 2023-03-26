
from builders.config_builder import configBuilder
from models.netdb_bgp        import netdbBgp

class bgpConfigBuilder(configBuilder):

    def __init__(self, device_id):
        configBuilder.__init__(self, device_id)
        self.data = netdbBgp().filter(self._DATA_FILT).fetch()['out']
