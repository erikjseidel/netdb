from .column import Column

class BgpColumn(Column):
    COLUMN = 'bgp'

    CATEGORIES = ['peer_groups', 'neighbors']


class DeviceColumn(Column):
    COLUMN = 'device'

    FLAT = True


class FirewallColumn(Column):
    COLUMN = 'firewall'

    CATEGORIES = ['policies', 'groups', 'zone_policy']


class IgpColumn(Column):
    COLUMN = 'igp'


class InterfaceColumn(Column):
    COLUMN = 'interface'

    ELEMENTS_ONLY = True


class PolicyColumn(Column):
    COLUMN = 'policy'

    CATEGORIES = ['prefix_lists', 'route_maps', 'aspath_lists', 'community_lists']
