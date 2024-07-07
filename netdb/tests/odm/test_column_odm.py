import sys
import pytest
from unittest.mock import MagicMock, patch

from fastapi.encoders import jsonable_encoder

from models.columns.device import DeviceContainer
from models.columns.interface import InterfaceContainer
from models.columns.igp import IGPContainer
from models.columns.bgp import BGPContainer
from models.columns.firewall import FirewallContainer
from models.columns.policy import PolicyContainer
from models.root import RootContainer

mock_defaults = MagicMock(DB_NAME='netdb', TRANSACTIONS=True, READ_ONLY=False)
mock_mongo_api = MagicMock(MongoAPI=MagicMock())


def mock_devices():
    return {
        "ROUTER1": {
            "location": "New York, New York",
            "roles": ["core_router", "edge_router", "firewall", "internal_router"],
            "providers": ["big-isp"],
            "node_name": "EXAMPLE3",
            "dhcp_servers": [
                {
                    "network": "10.5.130.0/24",
                    "router_ip": "10.5.130.1",
                    "ranges": [
                        {"start_address": "10.5.130.100", "end_address": "10.5.130.254"}
                    ],
                },
                {
                    "network": "192.0.2.128/26",
                    "router_ip": "192.0.2.129",
                    "ranges": [
                        {
                            "start_address": "192.0.2.138",
                            "end_address": "192.0.2.190",
                        }
                    ],
                },
            ],
            "meta": {
                "netbox": {
                    "id": 2,
                    "url": "https://netbox.example.net/dcim/devices/1/",
                    "status": "ACTIVE",
                    "last_updated": "2024-06-22T02:31:23.554719+00:00",
                }
            },
            "cvars": {
                "ibgp_ipv4": "10.0.16.10",
                "ibgp_ipv6": "fd00:10::16:10",
                "iso": "49.0001.0192.0000.0210.00",
                "router_id": "192.0.2.10",
                "local_asn": 65090,
                "primary_ipv4": "192.0.2.10",
                "primary_ipv6": "2001:db8::10",
                "primary_contact": "contact@help.us",
                "lldp_interfaces": [
                    "bond0",
                    "bond1",
                    "bond0.100",
                    "bond1.100",
                    "eth0",
                    "eth1",
                    "eth2",
                    "eth3",
                ],
                "znsl_prefixes": [
                    "192.0.2.0/24",
                    "2001:db8::/32",
                ],
                "dns_servers": ["1.0.0.1", "1.1.1.1"],
            },
        }
    }


def mock_interfaces():
    return {
        "ROUTER1": {
            "bond0": {
                "meta": {
                    "netbox": {
                        "id": 1,
                        "url": "https://netbox.example.net/dcim/interfaces/1/",
                        "last_updated": "2024-06-20T03:44:22.604999+00:00",
                    }
                },
                "description": "Trunk Interface",
                "type": "lacp",
                "lacp": {
                    "rate": "fast",
                    "min_links": 1,
                    "hash_policy": "layer3+4",
                    "members": ["eth1", "eth2"],
                },
            },
            "bond0.100": {
                "meta": {
                    "netbox": {
                        "id": 2,
                        "url": "https://netbox.example.net/dcim/interfaces/2/",
                        "last_updated": "2024-06-19T03:12:43.399690+00:00",
                    }
                },
                "mtu": 1500,
                "description": "Private VLAN",
                "policy": {"ipv4": "POLICY1"},
                "address": {
                    "10.5.130.1/24": {
                        "meta": {
                            "netbox": {
                                "id": 1,
                                "url": "https://netbox.example.net/ipam/ip-addresses/1/",
                                "last_updated": "2023-05-19T17:22:30.257562+00:00",
                            },
                            "tags": ["lan"],
                        }
                    }
                },
                "type": "vlan",
                "vlan": {"id": 100, "parent": "bond0"},
            },
            "bond0.900": {
                "meta": {
                    "netbox": {
                        "id": 4,
                        "url": "https://netbox.example.net/dcim/interfaces/4/",
                        "last_updated": "2024-06-19T00:16:02.386717+00:00",
                    }
                },
                "mtu": 1500,
                "description": "Management VLAN",
                "address": {
                    "192.168.21.12/24": {
                        "meta": {
                            "netbox": {
                                "id": 2,
                                "url": "https://netbox.example.net/ipam/ip-addresses/2/",
                                "last_updated": "2024-06-19T03:10:41.527393+00:00",
                            },
                            "tags": ["lan"],
                            "dns": {"ptr": "router1-vlan900.as36198.net"},
                        }
                    },
                    "fd00::900:12/64": {
                        "meta": {
                            "netbox": {
                                "id": 3,
                                "url": "https://netbox.example.net/ipam/ip-addresses/3/",
                                "last_updated": "2024-06-19T03:11:21.316473+00:00",
                            },
                            "tags": ["lan"],
                        }
                    },
                },
                "type": "vlan",
                "vlan": {"id": 900, "parent": "bond0"},
            },
            "dum0": {
                "meta": {
                    "netbox": {
                        "id": 5,
                        "url": "https://netbox.example.net/dcim/interfaces/5/",
                        "last_updated": "2024-06-19T00:21:39.796437+00:00",
                    }
                },
                "description": "Internal Loopback",
                "address": {
                    "10.0.10.12/32": {
                        "meta": {
                            "netbox": {
                                "id": 4,
                                "url": "https://netbox.example.net/ipam/ip-addresses/4/",
                                "last_updated": "2024-06-18T20:56:37.439262+00:00",
                            },
                            "tags": [],
                            "dns": {"ptr": "router1.loopbacks.example.net"},
                        }
                    },
                    "fd00:1010::12/128": {
                        "meta": {
                            "netbox": {
                                "id": 5,
                                "url": "https://netbox.example.net/ipam/ip-addresses/5/",
                                "last_updated": "2024-06-18T20:58:05.215580+00:00",
                            },
                            "tags": [],
                            "dns": {"ptr": "router1.loopbacks.example.net"},
                        }
                    },
                },
                "type": "dummy",
                "firewall": {
                    "local": {"ipv4": "LOOPBACK-LOCAL", "ipv6": "6-LOOPBACK-LOCAL"}
                },
            },
            "eth1": {
                "meta": {
                    "netbox": {
                        "id": 6,
                        "url": "https://netbox.example.net/dcim/interfaces/6/",
                        "last_updated": "2024-06-19T03:07:18.111849+00:00",
                    }
                },
                "description": "LACP Member: bond0",
                "type": "ethernet",
                "mac_address": "00:00:12:23:45:67",
                "offload": True,
            },
            "eth2": {
                "meta": {
                    "netbox": {
                        "id": 7,
                        "url": "https://netbox.example.net/dcim/interfaces/7/",
                        "last_updated": "2023-08-03T14:26:24.265454+00:00",
                    }
                },
                "description": "LACP Member: bond0",
                "type": "ethernet",
                "mac_address": "00:00:12:23:45:68",
                "offload": True,
            },
            "tun0": {
                "meta": {
                    "netbox": {
                        "id": 8,
                        "url": "https://netbox.example.net/dcim/interfaces/8/",
                        "last_updated": "2024-06-19T02:30:32.012882+00:00",
                    }
                },
                "mtu": 1450,
                "description": "router1:tun0:router2:tun0",
                "address": {
                    "10.10.10.10/31": {
                        "meta": {
                            "netbox": {
                                "id": 7,
                                "url": "https://netbox.as36198.net/ipam/ip-addresses/7/",
                                "last_updated": "2024-06-19T00:20:45.310283+00:00",
                            },
                            "tags": ["l3ptp"],
                            "dns": {"ptr": "router1-tun0-router2-tun0.ptp.example.net"},
                        }
                    },
                    "fd00:10:10:10::10/127": {
                        "meta": {
                            "netbox": {
                                "id": 8,
                                "url": "https://netbox.as36198.net/ipam/ip-addresses/8/",
                                "last_updated": "2024-06-19T00:20:48.204999+00:00",
                            },
                            "tags": ["l3ptp"],
                            "dns": {"ptr": "router1-tun0-router2-tun0.ptp.example.net"},
                        }
                    },
                },
                "type": "gre",
                "ttl": 255,
                "source": "10.5.130.1",
                "interface": "bond0.100",
                "remote": "192.0.2.160",
            },
        }
    }


def mock_igp():
    return {
        "ROUTER1": {
            "isis": {
                "meta": {
                    "netbox": {
                        "name": "isis_internal",
                        "last_updated": "2024-06-21T01:15:08.943182+00:00",
                    }
                },
                "level": 2,
                "lsp_mtu": 1497,
                "interfaces": [{"name": "bond0.959"}, {"name": "lo", "passive": True}],
                "iso": "49.0001.0192.0000.2012.00",
            }
        }
    }


def mock_bgp_netbox():
    return {
        "ROUTER1": {
            "neighbors": {
                "10.0.66.88": {"peer_group": "4_AS65000"},
                "fd00::66:88": {"peer_group": "6_AS65000"},
            }
        },
    }


def mock_bgp_pm():
    return {
        "ROUTER1": {
            "neighbors": {
                "169.254.169.254": {
                    "remote_asn": 64500,
                    "multihop": 2,
                    "password": "red_herring",
                    "source": "192.0.2.12",
                    "type": "ebgp",
                    "meta": {
                        "peering_manager": {
                            "url": "https://pm.example.net/api/peering/direct-peering-sessions/1/",
                            "status": "enabled",
                            "type": "transit-session",
                        }
                    },
                    "family": {
                        "ipv4": {
                            "nhs": True,
                            "route_map": {
                                "import": "4-TRANSIT-IN",
                                "export": "4-TRANSIT-OUT",
                            },
                        }
                    },
                },
                "fd00:1ff0:ffff::1": {
                    "remote_asn": 64500,
                    "multihop": 2,
                    "password": "red_herring",
                    "source": "fd00::1234:5678:9abc",
                    "type": "ebgp",
                    "meta": {
                        "peering_manager": {
                            "url": "https://pm.example.net/api/peering/direct-peering-sessions/2/",
                            "status": "enabled",
                            "type": "transit-session",
                        }
                    },
                    "family": {
                        "ipv6": {
                            "nhs": True,
                            "route_map": {
                                "import": "6-TRANSIT-IN",
                                "export": "6-TRANSIT-OUT",
                            },
                        }
                    },
                },
            },
        }
    }


def mock_bgp_repo():
    return {
        "ROUTER1": {
            "address_family": {
                "ipv4": {"redistribute": ["static"]},
                "ipv6": {"redistribute": ["static"]},
            },
            "options": {
                "asn": "65000",
                "hold_time": 30,
                "keepalive_time": 10,
                "log_neighbor_changes": True,
                "router_id": "192.0.2.12",
            },
            "neighbors": {
                "fd00:88::10": {"peer_group": "6_RR"},
                "fd00:88::11": {"peer_group": "6_RR"},
            },
            "peer_groups": {
                "4_PG_65001": {
                    "family": {
                        "ipv4": {
                            "nhs": True,
                            "route_map": {
                                "export": "4-PG-OUT",
                                "import": "4-PG-IN",
                            },
                        }
                    },
                    "remote_asn": 65001,
                },
                "6_PG_65001": {
                    "family": {
                        "ipv6": {
                            "nhs": True,
                            "route_map": {
                                "export": "6-PG-OUT",
                                "import": "6-PG-IN",
                            },
                        }
                    },
                    "remote_asn": 65001,
                },
                "6_RR": {
                    "family": {
                        "ipv4": {
                            "route_map": {"export": "4-RR-OUT", "import": "4-RR-IN"}
                        },
                        "ipv6": {
                            "route_map": {"export": "6-RR-OUT", "import": "6-RR-IN"}
                        },
                    },
                    "source": "fd00:88::12",
                    "type": "ibgp",
                },
            },
        },
    }


def mock_firewall():
    return {
        "ROUTER1": {
            "groups": {
                "ipv4": {
                    "dmz": {
                        "networks": ["192.0.2.10/32", "192.0.2.11/32"],
                        "type": "network",
                    },
                    "netops": {
                        "networks": [
                            "192.0.2.12/32",
                        ],
                        "type": "network",
                    },
                    "ssh": {
                        "networks": [
                            "192.0.2.13/32",
                            "192.0.2.14/32",
                            "192.0.2.15/32",
                        ],
                        "type": "network",
                    },
                    "trusted": {
                        "networks": [
                            "192.0.2.16/28",
                        ],
                        "type": "network",
                    },
                },
                "ipv6": {
                    "netops6": {
                        "networks": ["fd00:88::/64"],
                        "type": "network",
                    },
                    "trusted6": {
                        "networks": [
                            "fd00:cb00::/32",
                            "fd00:4700::/32",
                        ],
                        "type": "network",
                    },
                },
            },
            "options": {
                "all-ping": "enable",
                "broadcast-ping": "disable",
                "config-trap": "disable",
                "ipv6-receive-redirects": "disable",
                "ipv6-src-route": "disable",
                "log-martians": "enable",
                "send-redirects": "enable",
                "source-validation": "disable",
                "syn-cookies": "enable",
                "twa-hazards-protection": "disable",
                "ip-src-route": "enable",
                "receive-redirects": "enable",
            },
            "policies": {
                "ipv4": {
                    "CORE-OUT": {"default_action": "accept"},
                    "INTERNAL-LOCAL": {
                        "default_action": "drop",
                        "rules": [
                            {"action": "accept", "source": {"network_group": "netops"}},
                            {
                                "action": "accept",
                                "destination": {"port": [179]},
                                "protocol": "tcp",
                            },
                            {
                                "action": "accept",
                                "destination": {"network_group": "dmz"},
                            },
                            {
                                "action": "accept",
                                "protocol": "tcp_udp",
                                "state": ["established"],
                            },
                            {
                                "action": "accept",
                                "protocol": "tcp_udp",
                                "state": ["related"],
                            },
                            {"action": "accept", "protocol": "icmp"},
                        ],
                    },
                    "LOOPBACK-LOCAL": {
                        "default_action": "drop",
                        "rules": [
                            {"action": "accept", "source": {"network_group": "netops"}},
                            {
                                "action": "accept",
                                "destination": {"port": [179]},
                                "protocol": "tcp",
                            },
                        ],
                    },
                },
                "ipv6": {
                    "CORE-OUT6": {"default_action": "accept"},
                    "6-INTERNAL-LOCAL": {
                        "default_action": "drop",
                        "rules": [
                            {
                                "action": "accept",
                                "source": {"network_group": "netops6"},
                            },
                            {
                                "action": "accept",
                                "destination": {"port": [179]},
                                "protocol": "tcp",
                            },
                            {
                                "action": "accept",
                                "destination": {"network_group": "dmz"},
                            },
                            {
                                "action": "accept",
                                "protocol": "tcp_udp",
                                "state": ["established"],
                            },
                            {
                                "action": "accept",
                                "protocol": "tcp_udp",
                                "state": ["related"],
                            },
                            {"action": "accept", "protocol": "icmpv6"},
                        ],
                    },
                    "6-LOOPBACK-LOCAL": {
                        "default_action": "drop",
                        "rules": [
                            {
                                "action": "accept",
                                "source": {"network_group": "netops6"},
                            },
                            {
                                "action": "accept",
                                "destination": {"port": [179]},
                                "protocol": "tcp",
                            },
                        ],
                    },
                },
            },
            "state_policy": {"established": "accept", "related": "accept"},
            "zone_policy": {
                "CORE": {
                    "default_action": "drop",
                    "from": [
                        {
                            "ipv4_ruleset": "EDGE-OUT4",
                            "ipv6_ruleset": "EDGE-OUT6",
                            "zone": "EDGE",
                        }
                    ],
                    "interfaces": ["bond0.900", "bond0.150"],
                },
                "EDGE": {
                    "default_action": "drop",
                    "from": [
                        {
                            "ipv4_ruleset": "CORE-OUT",
                            "ipv6_ruleset": "CORE-OUT6",
                            "zone": "CORE",
                        }
                    ],
                    "interfaces": ["bond0.100", "tun0"],
                },
            },
            "mss_clamp": {
                "interfaces": ["tun0", "bond0.950"],
                "ipv4": 1280,
                "ipv6": 1280,
            },
        },
    }


def mock_policy():
    return {
        "ROUTER1": {
            "prefix_lists": {
                "ipv4": {
                    "4-BIG-PREFIXES": {
                        "rules": [{"ge": 1, "le": 7, "prefix": "0.0.0.0/0"}]
                    },
                    "4-DEFAULT-ROUTE": {"rules": [{"prefix": "0.0.0.0/0"}]},
                    "4-MARTIAN-PREFIXES": {
                        "rules": [
                            {"le": 32, "prefix": "0.0.0.0/8"},
                            {"le": 32, "prefix": "10.0.0.0/8"},
                            {"le": 32, "prefix": "192.168.0.0/16"},
                            {"le": 32, "prefix": "172.16.0.0/12"},
                            {"le": 32, "prefix": "100.64.0.0/10"},
                            {"le": 32, "prefix": "127.0.0.0/8"},
                            {"le": 32, "prefix": "169.254.0.0/16"},
                            {"le": 32, "prefix": "192.0.0.0/24"},
                            {"le": 32, "prefix": "192.0.2.0/24"},
                            {"le": 32, "prefix": "198.18.0.0/15"},
                            {"le": 32, "prefix": "198.51.100.0/24"},
                            {"le": 32, "prefix": "203.0.113.0/24"},
                            {"le": 32, "prefix": "224.0.0.0/3"},
                        ]
                    },
                    "4-SMALL-PREFIXES": {
                        "rules": [{"ge": 25, "le": 32, "prefix": "0.0.0.0/0"}]
                    },
                    "4-65000-PREFIXES": {
                        "rules": [
                            {"le": 24, "prefix": "10.0.0.0/8"},
                        ]
                    },
                },
                "ipv6": {
                    "6-BIG-PREFIXES": {
                        "rules": [{"ge": 1, "le": 15, "prefix": "::/0"}]
                    },
                    "6-DEFAULT-ROUTE": {"rules": [{"prefix": "::/0"}]},
                    "6-MARTIAN-PREFIXES": {
                        "rules": [
                            {"le": 128, "prefix": "::/8"},
                            {"le": 128, "prefix": "200::/7"},
                            {"le": 128, "prefix": "2001::/32"},
                            {"le": 128, "prefix": "2001:db8::/32"},
                            {"le": 128, "prefix": "2002::/16"},
                            {"le": 128, "prefix": "3ffe::/16"},
                            {"le": 128, "prefix": "5f00::/8"},
                            {"le": 128, "prefix": "fc00::/7"},
                            {"le": 128, "prefix": "fe80::/10"},
                            {"le": 128, "prefix": "fec0::/10"},
                            {"le": 128, "prefix": "ff00::/8"},
                        ]
                    },
                    "6-SMALL-PREFIXES": {
                        "rules": [{"ge": 49, "le": 128, "prefix": "::/0"}]
                    },
                    "6-65000-PREFIXES": {
                        "rules": [{"le": 64, "prefix": "fd00:abcd::/48"}]
                    },
                },
            },
            "route_maps": {
                "ipv4": {
                    "ALLOW-ALL": {"rules": [{"action": "permit", "number": 99}]},
                    "REJECT-ALL": {"rules": [{"action": "deny", "number": 99}]},
                    "4-PEER-IN": {
                        "rules": [
                            {
                                "action": "permit",
                                "match": {"prefix_list": "4-DEFAULT-ROUTE"},
                                "number": 50,
                                "set": {"local_pref": 100},
                            },
                            {
                                "action": "permit",
                                "match": {"prefix_list": "4-65000-PREFIXES"},
                                "number": 60,
                                "set": {"local_pref": 100},
                            },
                            {"action": "deny", "number": 99},
                        ]
                    },
                    "4-PEER-OUT": {
                        "rules": [
                            {
                                "action": "permit",
                                "match": {"prefix_list": "4-65000-PREFIXES"},
                                "number": 50,
                            },
                            {"action": "deny", "number": 99},
                        ]
                    },
                },
                "ipv6": {
                    "6-PEER-IN": {
                        "rules": [
                            {
                                "action": "permit",
                                "match": {"prefix_list": "6-DEFAULT-ROUTE"},
                                "number": 50,
                                "set": {"local_pref": 100},
                            },
                            {
                                "action": "permit",
                                "match": {"prefix_list": "6-65000-PREFIXES"},
                                "number": 60,
                                "set": {"local_pref": 100},
                            },
                            {"action": "deny", "number": 99},
                        ]
                    },
                    "6-PEER-OUT": {
                        "rules": [
                            {
                                "action": "permit",
                                "match": {"prefix_list": "6-65000-PREFIXES"},
                                "number": 50,
                            },
                            {"action": "deny", "number": 99},
                        ]
                    },
                },
            },
        }
    }


with patch.dict(
    'sys.modules', {'util.mongo_api': mock_mongo_api, 'config.defaults': mock_defaults}
):
    from odm import column_odm


@pytest.mark.parametrize(
    'column_type,flat,categories,datasource,weight,container',
    [
        (
            'device',
            True,
            [],
            'netbox',
            150,
            DeviceContainer(datasource='netbox', weight=150, column=mock_devices()),
        ),
        (
            'interface',
            False,
            [],
            'netbox',
            150,
            InterfaceContainer(
                datasource='netbox', weight=150, column=mock_interfaces()
            ),
        ),
        (
            'igp',
            False,
            [],
            'netbox',
            150,
            IGPContainer(datasource='netbox', weight=150, column=mock_igp()),
        ),
        (
            'bgp',
            False,
            ['peer_groups', 'neighbors'],
            'netbox',
            150,
            BGPContainer(datasource='netbox', weight=150, column=mock_bgp_netbox()),
        ),
        (
            'bgp',
            False,
            ['peer_groups', 'neighbors'],
            'peering_manager',
            100,
            BGPContainer(
                datasource='peering_manager', weight=100, column=mock_bgp_pm()
            ),
        ),
        (
            'bgp',
            False,
            ['peer_groups', 'neighbors'],
            'repo',
            50,
            BGPContainer(datasource='repo', weight=50, column=mock_bgp_repo()),
        ),
        (
            'firewall',
            False,
            ['policies', 'groups', 'zone_policy'],
            'repo',
            50,
            FirewallContainer(datasource='repo', weight=50, column=mock_firewall()),
        ),
        (
            'policy',
            False,
            ['prefix_lists', 'route_maps', 'aspath_lists', 'community_lists'],
            'repo',
            50,
            PolicyContainer(datasource='repo', weight=50, column=mock_policy()),
        ),
    ],
)
def test_column_odm_container_init(
    column_type, flat, categories, datasource, weight, container
):

    odm = column_odm.ColumnODM(container=container)

    assert odm.column_type == column_type
    assert odm.flat == flat
    assert odm.categories == categories
    assert odm.datasource == datasource
    assert odm.weight == weight
    assert odm.column == jsonable_encoder(container.column, exclude_none=True)
