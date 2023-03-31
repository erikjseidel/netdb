from .netdb_device    import netdbDevice
from .netdb_interface import netdbInterface
from .netdb_igp       import netdbIgp
from .netdb_firewall  import netdbFirewall
from .netdb_policy    import netdbPolicy
from .netdb_bgp       import netdbBgp

COLUMNS = {
        'device'     : netdbDevice,
        'interface'  : netdbInterface,
        'igp'        : netdbIgp,
        'firewall'   : netdbFirewall,
        'bgp'        : netdbBgp,
        'policy'     : netdbPolicy,
        } 

def newColumn(column = "device"):
    return COLUMNS[column]()
