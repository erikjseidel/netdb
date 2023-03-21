
from builders.config_builder import configBuilder
from models.netdb_policy     import netdbPolicy

class policyConfigBuilder(configBuilder):

    def __init__(self, device_id):
        configBuilder.__init__(self, device_id)
        self.data = netdbPolicy().fetch(self._DATA_FILT)['out']
