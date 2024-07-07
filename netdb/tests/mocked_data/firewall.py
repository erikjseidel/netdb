def mock_standard_firewall_data():
    """
    Standard firewall data which should successfully load into netdb.
    """
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


def mock_standard_firewall_documents():
    """
    Standard firewall data in MongoDB document format
    """
    return [
        {
            'category': 'policies',
            'data': {'default_action': 'accept'},
            'datasource': 'repo',
            'element_id': 'CORE-OUT',
            'family': 'ipv4',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'policies',
            'data': {
                'default_action': 'drop',
                'rules': [
                    {'action': 'accept', 'source': {'network_group': 'netops'}},
                    {
                        'action': 'accept',
                        'destination': {'port': [179]},
                        'protocol': 'tcp',
                    },
                    {'action': 'accept', 'destination': {'network_group': 'dmz'}},
                    {
                        'action': 'accept',
                        'protocol': 'tcp_udp',
                        'state': ['established'],
                    },
                    {'action': 'accept', 'protocol': 'tcp_udp', 'state': ['related']},
                    {'action': 'accept', 'protocol': 'icmp'},
                ],
            },
            'datasource': 'repo',
            'element_id': 'INTERNAL-LOCAL',
            'family': 'ipv4',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'policies',
            'data': {
                'default_action': 'drop',
                'rules': [
                    {'action': 'accept', 'source': {'network_group': 'netops'}},
                    {
                        'action': 'accept',
                        'destination': {'port': [179]},
                        'protocol': 'tcp',
                    },
                ],
            },
            'datasource': 'repo',
            'element_id': 'LOOPBACK-LOCAL',
            'family': 'ipv4',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'policies',
            'data': {'default_action': 'accept'},
            'datasource': 'repo',
            'element_id': 'CORE-OUT6',
            'family': 'ipv6',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'policies',
            'data': {
                'default_action': 'drop',
                'rules': [
                    {'action': 'accept', 'source': {'network_group': 'netops6'}},
                    {
                        'action': 'accept',
                        'destination': {'port': [179]},
                        'protocol': 'tcp',
                    },
                    {'action': 'accept', 'destination': {'network_group': 'dmz'}},
                    {
                        'action': 'accept',
                        'protocol': 'tcp_udp',
                        'state': ['established'],
                    },
                    {'action': 'accept', 'protocol': 'tcp_udp', 'state': ['related']},
                    {'action': 'accept', 'protocol': 'icmpv6'},
                ],
            },
            'datasource': 'repo',
            'element_id': '6-INTERNAL-LOCAL',
            'family': 'ipv6',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'policies',
            'data': {
                'default_action': 'drop',
                'rules': [
                    {'action': 'accept', 'source': {'network_group': 'netops6'}},
                    {
                        'action': 'accept',
                        'destination': {'port': [179]},
                        'protocol': 'tcp',
                    },
                ],
            },
            'datasource': 'repo',
            'element_id': '6-LOOPBACK-LOCAL',
            'family': 'ipv6',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'groups',
            'data': {'networks': ['192.0.2.10/32', '192.0.2.11/32'], 'type': 'network'},
            'datasource': 'repo',
            'element_id': 'dmz',
            'family': 'ipv4',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'groups',
            'data': {'networks': ['192.0.2.12/32'], 'type': 'network'},
            'datasource': 'repo',
            'element_id': 'netops',
            'family': 'ipv4',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'groups',
            'data': {
                'networks': ['192.0.2.13/32', '192.0.2.14/32', '192.0.2.15/32'],
                'type': 'network',
            },
            'datasource': 'repo',
            'element_id': 'ssh',
            'family': 'ipv4',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'groups',
            'data': {'networks': ['192.0.2.16/28'], 'type': 'network'},
            'datasource': 'repo',
            'element_id': 'trusted',
            'family': 'ipv4',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'groups',
            'data': {'networks': ['fd00:88::/64'], 'type': 'network'},
            'datasource': 'repo',
            'element_id': 'netops6',
            'family': 'ipv6',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'groups',
            'data': {
                'networks': ['fd00:cb00::/32', 'fd00:4700::/32'],
                'type': 'network',
            },
            'datasource': 'repo',
            'element_id': 'trusted6',
            'family': 'ipv6',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'data': {'established': 'accept', 'related': 'accept'},
            'datasource': 'repo',
            'element_id': 'state_policy',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'data': {'interfaces': ['tun0', 'bond0.950'], 'ipv4': 1280, 'ipv6': 1280},
            'datasource': 'repo',
            'element_id': 'mss_clamp',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'zone_policy',
            'data': {
                'default_action': 'drop',
                'from': [
                    {
                        'ipv4_ruleset': 'EDGE-OUT4',
                        'ipv6_ruleset': 'EDGE-OUT6',
                        'zone': 'EDGE',
                    }
                ],
                'interfaces': ['bond0.900', 'bond0.150'],
            },
            'datasource': 'repo',
            'element_id': 'CORE',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'category': 'zone_policy',
            'data': {
                'default_action': 'drop',
                'from': [
                    {
                        'ipv4_ruleset': 'CORE-OUT',
                        'ipv6_ruleset': 'CORE-OUT6',
                        'zone': 'CORE',
                    }
                ],
                'interfaces': ['bond0.100', 'tun0'],
            },
            'datasource': 'repo',
            'element_id': 'EDGE',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
        {
            'data': {
                'all-ping': 'enable',
                'broadcast-ping': 'disable',
                'config-trap': 'disable',
                'ip-src-route': 'enable',
                'ipv6-receive-redirects': 'disable',
                'ipv6-src-route': 'disable',
                'log-martians': 'enable',
                'receive-redirects': 'enable',
                'send-redirects': 'enable',
                'source-validation': 'disable',
                'syn-cookies': 'enable',
                'twa-hazards-protection': 'disable',
            },
            'datasource': 'repo',
            'element_id': 'options',
            'set_id': 'ROUTER1',
            'weight': 50,
        },
    ]


def mock_standard_firewall_column():
    """
    Standard firewall data column
    """
    return {
        'ROUTER1': {
            'groups': {
                'ipv4': {
                    'dmz': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'networks': ['192.0.2.10/32', '192.0.2.11/32'],
                        'type': 'network',
                    },
                    'netops': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'networks': ['192.0.2.12/32'],
                        'type': 'network',
                    },
                    'ssh': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'networks': ['192.0.2.13/32', '192.0.2.14/32', '192.0.2.15/32'],
                        'type': 'network',
                    },
                    'trusted': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'networks': ['192.0.2.16/28'],
                        'type': 'network',
                    },
                },
                'ipv6': {
                    'netops6': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'networks': ['fd00:88::/64'],
                        'type': 'network',
                    },
                    'trusted6': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'networks': ['fd00:cb00::/32', 'fd00:4700::/32'],
                        'type': 'network',
                    },
                },
            },
            'mss_clamp': {
                'interfaces': ['tun0', 'bond0.950'],
                'ipv4': 1280,
                'ipv6': 1280,
                'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
            },
            'options': {
                'all-ping': 'enable',
                'broadcast-ping': 'disable',
                'config-trap': 'disable',
                'ip-src-route': 'enable',
                'ipv6-receive-redirects': 'disable',
                'ipv6-src-route': 'disable',
                'log-martians': 'enable',
                'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                'receive-redirects': 'enable',
                'send-redirects': 'enable',
                'source-validation': 'disable',
                'syn-cookies': 'enable',
                'twa-hazards-protection': 'disable',
            },
            'policies': {
                'ipv4': {
                    'CORE-OUT': {
                        'default_action': 'accept',
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                    },
                    'INTERNAL-LOCAL': {
                        'default_action': 'drop',
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [
                            {'action': 'accept', 'source': {'network_group': 'netops'}},
                            {
                                'action': 'accept',
                                'destination': {'port': [179]},
                                'protocol': 'tcp',
                            },
                            {
                                'action': 'accept',
                                'destination': {'network_group': 'dmz'},
                            },
                            {
                                'action': 'accept',
                                'protocol': 'tcp_udp',
                                'state': ['established'],
                            },
                            {
                                'action': 'accept',
                                'protocol': 'tcp_udp',
                                'state': ['related'],
                            },
                            {'action': 'accept', 'protocol': 'icmp'},
                        ],
                    },
                    'LOOPBACK-LOCAL': {
                        'default_action': 'drop',
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [
                            {'action': 'accept', 'source': {'network_group': 'netops'}},
                            {
                                'action': 'accept',
                                'destination': {'port': [179]},
                                'protocol': 'tcp',
                            },
                        ],
                    },
                },
                'ipv6': {
                    '6-INTERNAL-LOCAL': {
                        'default_action': 'drop',
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [
                            {
                                'action': 'accept',
                                'source': {'network_group': 'netops6'},
                            },
                            {
                                'action': 'accept',
                                'destination': {'port': [179]},
                                'protocol': 'tcp',
                            },
                            {
                                'action': 'accept',
                                'destination': {'network_group': 'dmz'},
                            },
                            {
                                'action': 'accept',
                                'protocol': 'tcp_udp',
                                'state': ['established'],
                            },
                            {
                                'action': 'accept',
                                'protocol': 'tcp_udp',
                                'state': ['related'],
                            },
                            {'action': 'accept', 'protocol': 'icmpv6'},
                        ],
                    },
                    '6-LOOPBACK-LOCAL': {
                        'default_action': 'drop',
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [
                            {
                                'action': 'accept',
                                'source': {'network_group': 'netops6'},
                            },
                            {
                                'action': 'accept',
                                'destination': {'port': [179]},
                                'protocol': 'tcp',
                            },
                        ],
                    },
                    'CORE-OUT6': {
                        'default_action': 'accept',
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                    },
                },
            },
            'state_policy': {
                'established': 'accept',
                'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                'related': 'accept',
            },
            'zone_policy': {
                'CORE': {
                    'default_action': 'drop',
                    'from': [
                        {
                            'ipv4_ruleset': 'EDGE-OUT4',
                            'ipv6_ruleset': 'EDGE-OUT6',
                            'zone': 'EDGE',
                        }
                    ],
                    'interfaces': ['bond0.900', 'bond0.150'],
                    'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                },
                'EDGE': {
                    'default_action': 'drop',
                    'from': [
                        {
                            'ipv4_ruleset': 'CORE-OUT',
                            'ipv6_ruleset': 'CORE-OUT6',
                            'zone': 'CORE',
                        }
                    ],
                    'interfaces': ['bond0.100', 'tun0'],
                    'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                },
            },
        }
    }
