
from .igp_config_builder       import igpConfigBuilder
from .bgp_config_builder       import bgpConfigBuilder
from .firewall_config_builder  import firewallConfigBuilder
from .policy_config_builder    import policyConfigBuilder
from .interface_config_builder import interfaceConfigBuilder

BUILDERS = {
        'interface'  : interfaceConfigBuilder,
        'igp'        : igpConfigBuilder,
        'firewall'   : firewallConfigBuilder,
        'bgp'        : bgpConfigBuilder,
        'policy'     : policyConfigBuilder,
        } 

def newBuilder(column, device_id):
    return BUILDERS[column](device_id)

