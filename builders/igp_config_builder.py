
from builders.config_builder import configBuilder
from models.netdb_igp        import netdbIgp

class igpConfigBuilder(configBuilder):

    def __init__(self, device_id):
        configBuilder.__init__(self, device_id)
        self.data = netdbIgp().fetch(self._DATA_FILT)['out']
