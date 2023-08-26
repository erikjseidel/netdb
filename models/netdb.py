from .models import *

COLUMNS = {
        'device'     : DeviceColumn,
        'interface'  : InterfaceColumn,
        'igp'        : IgpColumn,
        'firewall'   : FirewallColumn,
        'bgp'        : BgpColumn,
        'policy'     : PolicyColumn,
        } 

def newColumn(column="device"):
    return COLUMNS[column]()
