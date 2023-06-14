from .models import *

BUILDERS = {
        'igp'        : igpConfigBuilder,
        'firewall'   : firewallConfigBuilder,
        'bgp'        : bgpConfigBuilder,
        'policy'     : policyConfigBuilder,
        } 

def newBuilder(column, device_id):
    return BUILDERS[column](device_id)
