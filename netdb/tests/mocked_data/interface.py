from models.types import NetdbDocument


def mock_standard_interface_data():
    """
    Standard interface data that should successfully load into netdb.
    """
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


def mock_standard_interface_documents():
    """
    Standard interface data in MongoDB document list format
    """
    return [
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=False,
            category=None,
            family=None,
            element_id='bond0',
            data={
                'type': 'lacp',
                'disabled': False,
                'offload': False,
                'use_dhcp': False,
                'ipv6_autoconf': False,
                'description': 'Trunk Interface',
                'lacp': {
                    'hash_policy': 'layer3+4',
                    'rate': 'fast',
                    'min_links': 1,
                    'members': ['eth1', 'eth2'],
                },
                'meta': {
                    'netbox': {
                        'id': 1,
                        'url': 'https://netbox.example.net/dcim/interfaces/1/',
                        'last_updated': '2024-06-20T03:44:22.604999+00:00',
                    }
                },
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=False,
            category=None,
            family=None,
            element_id='bond0.100',
            data={
                'type': 'vlan',
                'disabled': False,
                'offload': False,
                'use_dhcp': False,
                'ipv6_autoconf': False,
                'description': 'Private VLAN',
                'mtu': 1500,
                'address': {
                    '10.5.130.1/24': {
                        'meta': {
                            'netbox': {
                                'id': 1,
                                'url': 'https://netbox.example.net/ipam/ip-addresses/1/',
                                'last_updated': '2023-05-19T17:22:30.257562+00:00',
                            },
                            'tags': ['lan'],
                        }
                    }
                },
                'vlan': {'id': 100, 'parent': 'bond0'},
                'policy': {'ipv4': 'POLICY1'},
                'meta': {
                    'netbox': {
                        'id': 2,
                        'url': 'https://netbox.example.net/dcim/interfaces/2/',
                        'last_updated': '2024-06-19T03:12:43.399690+00:00',
                    }
                },
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=False,
            category=None,
            family=None,
            element_id='bond0.900',
            data={
                'type': 'vlan',
                'disabled': False,
                'offload': False,
                'use_dhcp': False,
                'ipv6_autoconf': False,
                'description': 'Management VLAN',
                'mtu': 1500,
                'address': {
                    '192.168.21.12/24': {
                        'meta': {
                            'netbox': {
                                'id': 2,
                                'url': 'https://netbox.example.net/ipam/ip-addresses/2/',
                                'last_updated': '2024-06-19T03:10:41.527393+00:00',
                            },
                            'tags': ['lan'],
                            'dns': {'ptr': 'router1-vlan900.as36198.net'},
                        }
                    },
                    'fd00::900:12/64': {
                        'meta': {
                            'netbox': {
                                'id': 3,
                                'url': 'https://netbox.example.net/ipam/ip-addresses/3/',
                                'last_updated': '2024-06-19T03:11:21.316473+00:00',
                            },
                            'tags': ['lan'],
                        }
                    },
                },
                'vlan': {'id': 900, 'parent': 'bond0'},
                'meta': {
                    'netbox': {
                        'id': 4,
                        'url': 'https://netbox.example.net/dcim/interfaces/4/',
                        'last_updated': '2024-06-19T00:16:02.386717+00:00',
                    }
                },
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=False,
            category=None,
            family=None,
            element_id='dum0',
            data={
                'type': 'dummy',
                'disabled': False,
                'offload': False,
                'use_dhcp': False,
                'ipv6_autoconf': False,
                'description': 'Internal Loopback',
                'address': {
                    '10.0.10.12/32': {
                        'meta': {
                            'netbox': {
                                'id': 4,
                                'url': 'https://netbox.example.net/ipam/ip-addresses/4/',
                                'last_updated': '2024-06-18T20:56:37.439262+00:00',
                            },
                            'tags': [],
                            'dns': {'ptr': 'router1.loopbacks.example.net'},
                        }
                    },
                    'fd00:1010::12/128': {
                        'meta': {
                            'netbox': {
                                'id': 5,
                                'url': 'https://netbox.example.net/ipam/ip-addresses/5/',
                                'last_updated': '2024-06-18T20:58:05.215580+00:00',
                            },
                            'tags': [],
                            'dns': {'ptr': 'router1.loopbacks.example.net'},
                        }
                    },
                },
                'firewall': {
                    'local': {'ipv4': 'LOOPBACK-LOCAL', 'ipv6': '6-LOOPBACK-LOCAL'}
                },
                'meta': {
                    'netbox': {
                        'id': 5,
                        'url': 'https://netbox.example.net/dcim/interfaces/5/',
                        'last_updated': '2024-06-19T00:21:39.796437+00:00',
                    }
                },
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=False,
            category=None,
            family=None,
            element_id='eth1',
            data={
                'type': 'ethernet',
                'disabled': False,
                'offload': True,
                'use_dhcp': False,
                'ipv6_autoconf': False,
                'description': 'LACP Member: bond0',
                'mac_address': '00:00:12:23:45:67',
                'meta': {
                    'netbox': {
                        'id': 6,
                        'url': 'https://netbox.example.net/dcim/interfaces/6/',
                        'last_updated': '2024-06-19T03:07:18.111849+00:00',
                    }
                },
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=False,
            category=None,
            family=None,
            element_id='eth2',
            data={
                'type': 'ethernet',
                'disabled': False,
                'offload': True,
                'use_dhcp': False,
                'ipv6_autoconf': False,
                'description': 'LACP Member: bond0',
                'mac_address': '00:00:12:23:45:68',
                'meta': {
                    'netbox': {
                        'id': 7,
                        'url': 'https://netbox.example.net/dcim/interfaces/7/',
                        'last_updated': '2023-08-03T14:26:24.265454+00:00',
                    }
                },
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=False,
            category=None,
            family=None,
            element_id='tun0',
            data={
                'type': 'gre',
                'disabled': False,
                'offload': False,
                'use_dhcp': False,
                'ipv6_autoconf': False,
                'description': 'router1:tun0:router2:tun0',
                'interface': 'bond0.100',
                'mtu': 1450,
                'ttl': 255,
                'remote': '192.0.2.160',
                'source': '10.5.130.1',
                'address': {
                    '10.10.10.10/31': {
                        'meta': {
                            'netbox': {
                                'id': 7,
                                'url': 'https://netbox.as36198.net/ipam/ip-addresses/7/',
                                'last_updated': '2024-06-19T00:20:45.310283+00:00',
                            },
                            'tags': ['l3ptp'],
                            'dns': {'ptr': 'router1-tun0-router2-tun0.ptp.example.net'},
                        }
                    },
                    'fd00:10:10:10::10/127': {
                        'meta': {
                            'netbox': {
                                'id': 8,
                                'url': 'https://netbox.as36198.net/ipam/ip-addresses/8/',
                                'last_updated': '2024-06-19T00:20:48.204999+00:00',
                            },
                            'tags': ['l3ptp'],
                            'dns': {'ptr': 'router1-tun0-router2-tun0.ptp.example.net'},
                        }
                    },
                },
                'meta': {
                    'netbox': {
                        'id': 8,
                        'url': 'https://netbox.example.net/dcim/interfaces/8/',
                        'last_updated': '2024-06-19T02:30:32.012882+00:00',
                    }
                },
            },
        ),
    ]


def mock_standard_interface_column(check_override=False):
    """
    Standard interface data column
    """
    ret = {
        'ROUTER1': {
            'bond0': {
                'description': 'Trunk Interface',
                'disabled': False,
                'ipv6_autoconf': False,
                'lacp': {
                    'hash_policy': 'layer3+4',
                    'members': ['eth1', 'eth2'],
                    'min_links': 1,
                    'rate': 'fast',
                },
                'meta': {
                    'netbox': {
                        'id': 1,
                        'last_updated': '2024-06-20T03:44:22.604999+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/1/',
                    },
                    'netdb': {'datasource': 'netbox', 'weight': 150},
                },
                'offload': False,
                'type': 'lacp',
                'use_dhcp': False,
            },
            'bond0.100': {
                'address': {
                    '10.5.130.1/24': {
                        'meta': {
                            'netbox': {
                                'id': 1,
                                'last_updated': '2023-05-19T17:22:30.257562+00:00',
                                'url': 'https://netbox.example.net/ipam/ip-addresses/1/',
                            },
                            'tags': ['lan'],
                        }
                    }
                },
                'description': 'Private VLAN',
                'disabled': check_override,
                'ipv6_autoconf': False,
                'meta': {
                    'netbox': {
                        'id': 2,
                        'last_updated': '2024-06-19T03:12:43.399690+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/2/',
                    },
                    'netdb': {'datasource': 'netbox', 'weight': 150},
                },
                'mtu': 1500,
                'offload': False,
                'policy': {'ipv4': 'POLICY1'},
                'type': 'vlan',
                'use_dhcp': False,
                'vlan': {'id': 100, 'parent': 'bond0'},
            },
            'bond0.900': {
                'address': {
                    '192.168.21.12/24': {
                        'meta': {
                            'dns': {'ptr': 'router1-vlan900.as36198.net'},
                            'netbox': {
                                'id': 2,
                                'last_updated': '2024-06-19T03:10:41.527393+00:00',
                                'url': 'https://netbox.example.net/ipam/ip-addresses/2/',
                            },
                            'tags': ['lan'],
                        }
                    },
                    'fd00::900:12/64': {
                        'meta': {
                            'netbox': {
                                'id': 3,
                                'last_updated': '2024-06-19T03:11:21.316473+00:00',
                                'url': 'https://netbox.example.net/ipam/ip-addresses/3/',
                            },
                            'tags': ['lan'],
                        }
                    },
                },
                'description': 'Management VLAN',
                'disabled': False,
                'ipv6_autoconf': False,
                'meta': {
                    'netbox': {
                        'id': 4,
                        'last_updated': '2024-06-19T00:16:02.386717+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/4/',
                    },
                    'netdb': {'datasource': 'netbox', 'weight': 150},
                },
                'mtu': 1500,
                'offload': False,
                'type': 'vlan',
                'use_dhcp': False,
                'vlan': {'id': 900, 'parent': 'bond0'},
            },
            'dum0': {
                'address': {
                    '10.0.10.12/32': {
                        'meta': {
                            'dns': {'ptr': 'router1.loopbacks.example.net'},
                            'netbox': {
                                'id': 4,
                                'last_updated': '2024-06-18T20:56:37.439262+00:00',
                                'url': 'https://netbox.example.net/ipam/ip-addresses/4/',
                            },
                            'tags': [],
                        }
                    },
                    'fd00:1010::12/128': {
                        'meta': {
                            'dns': {'ptr': 'router1.loopbacks.example.net'},
                            'netbox': {
                                'id': 5,
                                'last_updated': '2024-06-18T20:58:05.215580+00:00',
                                'url': 'https://netbox.example.net/ipam/ip-addresses/5/',
                            },
                            'tags': [],
                        }
                    },
                },
                'description': 'Internal Loopback',
                'disabled': False,
                'firewall': {
                    'local': {'ipv4': 'LOOPBACK-LOCAL', 'ipv6': '6-LOOPBACK-LOCAL'}
                },
                'ipv6_autoconf': False,
                'meta': {
                    'netbox': {
                        'id': 5,
                        'last_updated': '2024-06-19T00:21:39.796437+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/5/',
                    },
                    'netdb': {'datasource': 'netbox', 'weight': 150},
                },
                'offload': False,
                'type': 'dummy',
                'use_dhcp': False,
            },
            'eth1': {
                'description': 'LACP Member: bond0',
                'disabled': False,
                'ipv6_autoconf': False,
                'mac_address': '00:00:12:23:45:67',
                'meta': {
                    'netbox': {
                        'id': 6,
                        'last_updated': '2024-06-19T03:07:18.111849+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/6/',
                    },
                    'netdb': {'datasource': 'netbox', 'weight': 150},
                },
                'offload': True,
                'type': 'ethernet',
                'use_dhcp': False,
            },
            'eth2': {
                'description': 'LACP Member: bond0',
                'disabled': False,
                'ipv6_autoconf': False,
                'mac_address': '00:00:12:23:45:68',
                'meta': {
                    'netbox': {
                        'id': 7,
                        'last_updated': '2023-08-03T14:26:24.265454+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/7/',
                    },
                    'netdb': {'datasource': 'netbox', 'weight': 150},
                },
                'offload': True,
                'type': 'ethernet',
                'use_dhcp': False,
            },
            'tun0': {
                'address': {
                    '10.10.10.10/31': {
                        'meta': {
                            'dns': {'ptr': 'router1-tun0-router2-tun0.ptp.example.net'},
                            'netbox': {
                                'id': 7,
                                'last_updated': '2024-06-19T00:20:45.310283+00:00',
                                'url': 'https://netbox.as36198.net/ipam/ip-addresses/7/',
                            },
                            'tags': ['l3ptp'],
                        }
                    },
                    'fd00:10:10:10::10/127': {
                        'meta': {
                            'dns': {'ptr': 'router1-tun0-router2-tun0.ptp.example.net'},
                            'netbox': {
                                'id': 8,
                                'last_updated': '2024-06-19T00:20:48.204999+00:00',
                                'url': 'https://netbox.as36198.net/ipam/ip-addresses/8/',
                            },
                            'tags': ['l3ptp'],
                        }
                    },
                },
                'description': 'router1:tun0:router2:tun0',
                'disabled': False,
                'ipv6_autoconf': False,
                'interface': 'bond0.100',
                'meta': {
                    'netbox': {
                        'id': 8,
                        'last_updated': '2024-06-19T02:30:32.012882+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/8/',
                    },
                    'netdb': {'datasource': 'netbox', 'weight': 150},
                },
                'mtu': 1450,
                'offload': False,
                'remote': '192.0.2.160',
                'source': '10.5.130.1',
                'ttl': 255,
                'type': 'gre',
                'use_dhcp': False,
            },
        }
    }

    if check_override:
        ret['ROUTER1']['bond0.100']['meta']['netdb']['override'] = True

    return ret


def mock_standard_interface_pydantic_return():
    """
    Pydantic will add missing keys to inputted data with their default values. This
    function mocks such additions to standard_interface_data in its return.
    """
    return {
        'ROUTER1': {
            'bond0': {
                'description': 'Trunk Interface',
                'disabled': False,
                'ipv6_autoconf': False,
                'lacp': {
                    'hash_policy': 'layer3+4',
                    'members': [
                        'eth1',
                        'eth2',
                    ],
                    'min_links': 1,
                    'rate': 'fast',
                },
                'meta': {
                    'netbox': {
                        'id': 1,
                        'last_updated': '2024-06-20T03:44:22.604999+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/1/',
                    },
                },
                'offload': False,
                'type': 'lacp',
                'use_dhcp': False,
            },
            'bond0.100': {
                'address': {
                    '10.5.130.1/24': {
                        'meta': {
                            'netbox': {
                                'id': 1,
                                'last_updated': '2023-05-19T17:22:30.257562+00:00',
                                'url': 'https://netbox.example.net/ipam/ip-addresses/1/',
                            },
                            'tags': [
                                'lan',
                            ],
                        },
                    },
                },
                'description': 'Private VLAN',
                'disabled': False,
                'ipv6_autoconf': False,
                'meta': {
                    'netbox': {
                        'id': 2,
                        'last_updated': '2024-06-19T03:12:43.399690+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/2/',
                    },
                },
                'mtu': 1500,
                'offload': False,
                'policy': {
                    'ipv4': 'POLICY1',
                },
                'type': 'vlan',
                'use_dhcp': False,
                'vlan': {
                    'id': 100,
                    'parent': 'bond0',
                },
            },
            'bond0.900': {
                'address': {
                    '192.168.21.12/24': {
                        'meta': {
                            'dns': {
                                'ptr': 'router1-vlan900.as36198.net',
                            },
                            'netbox': {
                                'id': 2,
                                'last_updated': '2024-06-19T03:10:41.527393+00:00',
                                'url': 'https://netbox.example.net/ipam/ip-addresses/2/',
                            },
                            'tags': [
                                'lan',
                            ],
                        },
                    },
                    'fd00::900:12/64': {
                        'meta': {
                            'netbox': {
                                'id': 3,
                                'last_updated': '2024-06-19T03:11:21.316473+00:00',
                                'url': 'https://netbox.example.net/ipam/ip-addresses/3/',
                            },
                            'tags': [
                                'lan',
                            ],
                        },
                    },
                },
                'description': 'Management VLAN',
                'disabled': False,
                'ipv6_autoconf': False,
                'meta': {
                    'netbox': {
                        'id': 4,
                        'last_updated': '2024-06-19T00:16:02.386717+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/4/',
                    },
                },
                'mtu': 1500,
                'offload': False,
                'type': 'vlan',
                'use_dhcp': False,
                'vlan': {
                    'id': 900,
                    'parent': 'bond0',
                },
            },
            'dum0': {
                'address': {
                    '10.0.10.12/32': {
                        'meta': {
                            'dns': {
                                'ptr': 'router1.loopbacks.example.net',
                            },
                            'netbox': {
                                'id': 4,
                                'last_updated': '2024-06-18T20:56:37.439262+00:00',
                                'url': 'https://netbox.example.net/ipam/ip-addresses/4/',
                            },
                            'tags': [],
                        },
                    },
                    'fd00:1010::12/128': {
                        'meta': {
                            'dns': {
                                'ptr': 'router1.loopbacks.example.net',
                            },
                            'netbox': {
                                'id': 5,
                                'last_updated': '2024-06-18T20:58:05.215580+00:00',
                                'url': 'https://netbox.example.net/ipam/ip-addresses/5/',
                            },
                            'tags': [],
                        },
                    },
                },
                'description': 'Internal Loopback',
                'disabled': False,
                'firewall': {
                    'local': {
                        'ipv4': 'LOOPBACK-LOCAL',
                        'ipv6': '6-LOOPBACK-LOCAL',
                    },
                },
                'ipv6_autoconf': False,
                'meta': {
                    'netbox': {
                        'id': 5,
                        'last_updated': '2024-06-19T00:21:39.796437+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/5/',
                    },
                },
                'offload': False,
                'type': 'dummy',
                'use_dhcp': False,
            },
            'eth1': {
                'description': 'LACP Member: bond0',
                'disabled': False,
                'ipv6_autoconf': False,
                'mac_address': '00:00:12:23:45:67',
                'meta': {
                    'netbox': {
                        'id': 6,
                        'last_updated': '2024-06-19T03:07:18.111849+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/6/',
                    },
                },
                'offload': True,
                'type': 'ethernet',
                'use_dhcp': False,
            },
            'eth2': {
                'description': 'LACP Member: bond0',
                'disabled': False,
                'ipv6_autoconf': False,
                'mac_address': '00:00:12:23:45:68',
                'meta': {
                    'netbox': {
                        'id': 7,
                        'last_updated': '2023-08-03T14:26:24.265454+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/7/',
                    },
                },
                'offload': True,
                'type': 'ethernet',
                'use_dhcp': False,
            },
            'tun0': {
                'address': {
                    '10.10.10.10/31': {
                        'meta': {
                            'dns': {
                                'ptr': 'router1-tun0-router2-tun0.ptp.example.net',
                            },
                            'netbox': {
                                'id': 7,
                                'last_updated': '2024-06-19T00:20:45.310283+00:00',
                                'url': 'https://netbox.as36198.net/ipam/ip-addresses/7/',
                            },
                            'tags': [
                                'l3ptp',
                            ],
                        },
                    },
                    'fd00:10:10:10::10/127': {
                        'meta': {
                            'dns': {
                                'ptr': 'router1-tun0-router2-tun0.ptp.example.net',
                            },
                            'netbox': {
                                'id': 8,
                                'last_updated': '2024-06-19T00:20:48.204999+00:00',
                                'url': 'https://netbox.as36198.net/ipam/ip-addresses/8/',
                            },
                            'tags': [
                                'l3ptp',
                            ],
                        },
                    },
                },
                'description': 'router1:tun0:router2:tun0',
                'disabled': False,
                'interface': 'bond0.100',
                'ipv6_autoconf': False,
                'meta': {
                    'netbox': {
                        'id': 8,
                        'last_updated': '2024-06-19T02:30:32.012882+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/8/',
                    },
                },
                'mtu': 1450,
                'offload': False,
                'remote': '192.0.2.160',
                'source': '10.5.130.1',
                'ttl': 255,
                'type': 'gre',
                'use_dhcp': False,
            },
        },
    }


def mock_nonexistent_device_interface_data():
    """
    Interface data for non-existant router that should trigger a validation failure.
    """
    return {
        "ROUTER3": {
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
        }
    }


def mock_invalid_interface_data():
    """
    Interface data for non-existant router that should trigger a validation failure.
    """
    return {
        "ROUTER3": {
            "bond0": {
                "meta": {
                    "netbox": {
                        "id": 1,
                        "url": "https://netbox.example.net/dcim/interfaces/1/",
                        "last_updated": "2024-06-20T03:44:22.604999+00:00",
                    }
                },
                "description": "Trunk Interface",
                "type": "lcp",
                "lacp": {
                    "rate": "fast",
                    "min_links": 1,
                    "hash_policy": "ayer3+4",
                    "members": ["eth1", "eth2"],
                },
            },
            'tun0': {
                'address': {
                    '10.10.10/31': {
                        'meta': {
                            'dns': {'ptr': 'router1-tun0-router2-tun0.ptp.example.net'},
                            'netbox': {
                                'id': 7,
                                'last_updated': '2024-06-19T00:20:45.310283+00:00',
                                'url': 'https://netbox.as36198.net/ipam/ip-addresses/7/',
                            },
                            'tags': ['l3ptp'],
                        }
                    },
                    'fd00:10::10::10/127': {
                        'meta': {
                            'dns': {'ptr': 'router1-tun0-router2-tun0.ptp.example.net'},
                            'netbox': {
                                'id': 8,
                                'last_updated': '2024-06-19T00:20:48.204999+00:00',
                                'url': 'https://netbox.as36198.net/ipam/ip-addresses/8/',
                            },
                            'tags': ['l3ptp'],
                        }
                    },
                },
                'description': 'router1:tun0:router2:tun0',
                'disabled': False,
                'interface': 'bond0.100',
                'ipv6_autoconf': False,
                'meta': {
                    'netbox': {
                        'id': 8,
                        'last_updated': '2024-06-19T02:30:32.012882+00:00',
                        'url': 'https://netbox.example.net/dcim/interfaces/8/',
                    },
                    'netdb': {'datasource': 'netbox', 'weight': 150},
                },
                'mtu': 1450,
                'offload': 'true',
                'remote': '192.0.2.160',
                'source': '10.5.130.1',
                'ttl': 255,
                'type': 'gre',
                'use_dhcp': False,
            },
        }
    }


def mock_invalid_interface_pydantic_return():
    """
    Returns the expected pydantic error return for mock_invalid_interface_data()
    """
    return {
        'comment': 'NetDB says: FastAPI returned a validation error.',
        'error': False,
        'out': {
            'detail': [
                {
                    'ctx': {
                        'expected': "'ethernet', 'vlan', 'lacp', 'dummy', 'gre' or 'l2gre'",
                    },
                    'input': 'lcp',
                    'loc': [
                        'body',
                        'interface',
                        'column',
                        'ROUTER3',
                        'bond0',
                        'type',
                    ],
                    'msg': "Input should be 'ethernet', 'vlan', 'lacp', 'dummy', 'gre' or "
                    "'l2gre'",
                    'type': 'literal_error',
                },
                {
                    'ctx': {
                        'expected': "'layer2+3' or 'layer3+4'",
                    },
                    'input': 'ayer3+4',
                    'loc': [
                        'body',
                        'interface',
                        'column',
                        'ROUTER3',
                        'bond0',
                        'lacp',
                        'hash_policy',
                    ],
                    'msg': "Input should be 'layer2+3' or 'layer3+4'",
                    'type': 'literal_error',
                },
                {
                    'input': '10.10.10/31',
                    'loc': [
                        'body',
                        'interface',
                        'column',
                        'ROUTER3',
                        'tun0',
                        'address',
                        '10.10.10/31',
                        '[key]',
                    ],
                    'msg': 'value is not a valid IPv4 or IPv6 interface',
                    'type': 'ip_any_interface',
                },
                {
                    'input': 'fd00:10::10::10/127',
                    'loc': [
                        'body',
                        'interface',
                        'column',
                        'ROUTER3',
                        'tun0',
                        'address',
                        'fd00:10::10::10/127',
                        '[key]',
                    ],
                    'msg': 'value is not a valid IPv4 or IPv6 interface',
                    'type': 'ip_any_interface',
                },
            ],
        },
        'result': False,
    }
