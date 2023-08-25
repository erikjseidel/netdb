from schema.device import *
from schema.interface import *
from util.decorators import netdb_internal
from .column import netdbColumn

class netdbBgp(netdbColumn):
    CATEGORIES = ['peer_groups', 'neighbors']

    _COLUMN     = 'bgp'


class netdbDevice(netdbColumn):
    _COLUMN     = 'device'

    FLAT = True


class netdbFirewall(netdbColumn):
    _COLUMN     = 'firewall'

    CATEGORIES = ['policies', 'groups', 'zone_policy']


class netdbIgp(netdbColumn):
    _COLUMN     = 'igp'


class netdbInterface(netdbColumn):
    _COLUMN     = 'interface'

    ELEMENTS_ONLY = True


class netdbPolicy(netdbColumn):
    _COLUMN = 'policy'

    CATEGORIES = ['prefix_lists', 'route_maps', 'aspath_lists', 'community_lists']
