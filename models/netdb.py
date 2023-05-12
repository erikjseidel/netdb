from .models import *

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
