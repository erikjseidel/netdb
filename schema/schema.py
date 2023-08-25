from .igp import igpSchema
from .bgp import bgpSchema
from .firewall import firewallSchema
from .policy import policySchema
from .interface import interfaceSchema
from .device import deviceSchema

SCHEMAS = {
        'igp'        : igpSchema,
        'bgp'        : bgpSchema,
        'firewall'   : firewallSchema,
        'policy'     : policySchema,
        'interface'  : interfaceSchema,
        'device'     : deviceSchema,
        } 

def newSchema(column):
    return SCHEMAS[column]()
