
from builders.config_builder import configBuilder
from models.netdb_igp        import netdbIgp

class igpConfigBuilder(configBuilder, netdbIgp):

    def __init__(self, device_id):
        configBuilder.__init__(self, device_id)
        self.data = netdbIgp().filter(self._DATA_FILT).fetch()['out']
