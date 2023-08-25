from .column import netdbColumn

class netdbBgp(netdbColumn):
    COLUMN = 'bgp'

    CATEGORIES = ['peer_groups', 'neighbors']


class netdbDevice(netdbColumn):
    COLUMN = 'device'

    FLAT = True


class netdbFirewall(netdbColumn):
    COLUMN = 'firewall'

    CATEGORIES = ['policies', 'groups', 'zone_policy']


class netdbIgp(netdbColumn):
    COLUMN = 'igp'


class netdbInterface(netdbColumn):
    COLUMN = 'interface'

    ELEMENTS_ONLY = True


class netdbPolicy(netdbColumn):
    COLUMN = 'policy'

    CATEGORIES = ['prefix_lists', 'route_maps', 'aspath_lists', 'community_lists']
