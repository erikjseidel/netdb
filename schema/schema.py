
from .igp       import *
from .bgp       import *
from .firewall  import *
from .policy    import *
from .interface import *

SCHEMAS = {
        'interface'  : interfacesSchema,
        'igp'        : igpSchema,
        'firewall'   : firewallSchema,
        'bgp'        : bgpSchema,
        'policy'     : policySchema,
        } 

def newSchema(column):
    return SCHEMAS[column]()

