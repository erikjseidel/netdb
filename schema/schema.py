from .igp import igpSchema
from .bgp import bgpSchema
from .firewall import firewallSchema
from .policy import policySchema
from .interface import interfaceSchema

SCHEMAS = {
        'igp'        : igpSchema,
        'bgp'        : bgpSchema,
        'firewall'   : firewallSchema,
        'policy'     : policySchema,
        'interface'  : interfaceSchema,
        } 

def newSchema(column):
    return SCHEMAS[column]()

