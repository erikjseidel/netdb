from builders.config_builder import configBuilder
from models.models import netdbBgp, netdbFirewall, netdbIgp, netdbPolicy

class bgpConfigBuilder(configBuilder, netdbBgp):

    def __init__(self, device_id):
        configBuilder.__init__(self, device_id)
        self.data = netdbBgp().filter(self._DATA_FILT).fetch().get('out')


class firewallConfigBuilder(configBuilder, netdbFirewall):

    def __init__(self, device_id):
        configBuilder.__init__(self, device_id)
        self.data = netdbFirewall().filter(self._DATA_FILT).fetch().get('out')


class igpConfigBuilder(configBuilder, netdbIgp):

    def __init__(self, device_id):
        configBuilder.__init__(self, device_id)
        self.data = netdbIgp().filter(self._DATA_FILT).fetch().get('out')


class policyConfigBuilder(configBuilder, netdbPolicy):

    def __init__(self, device_id):
        configBuilder.__init__(self, device_id)
        self.data = netdbPolicy().filter(self._DATA_FILT).fetch().get('out')
