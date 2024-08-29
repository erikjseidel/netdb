from models.types import NetdbDocument


def mock_standard_protocol_data():
    """
    Standard IGP input data that should successfully load into netdb
    """
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
            },
            "lldp": {
                "meta": {"netdb": {"datasource": "netbox", "weight": 150}},
                "interfaces": ["bond0", "eth6", "eth7"],
            },
            "services": {
                "dhcp_server": {
                    "meta": {
                        "netbox": {
                            "id": 1,
                            "url": "https://netbox.example.net/ipam/services/1/",
                            "last_updated": "2024-06-23T01:57:29.635963+00:00",
                        },
                        "netdb": {"datasource": "netbox", "weight": 150},
                    },
                    "networks": [
                        {
                            "router_ip": "10.10.10.1",
                            "network": "10.10.10.0/24",
                            "ranges": [
                                {
                                    "start_address": "10.10.10.100",
                                    "end_address": "10.10.10.254",
                                }
                            ],
                        },
                        {
                            "router_ip": "192.168.1.129",
                            "network": "192.168.1.128/26",
                            "ranges": [
                                {
                                    "start_address": "192.168.1.138",
                                    "end_address": "192.168.1.190",
                                }
                            ],
                        },
                    ],
                }
            },
        }
    }


def mock_standard_protocol_documents():
    """
    Standard IGP data in MongoDB document list format
    """
    return [
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=False,
            category=None,
            family=None,
            element_id='isis',
            data={
                'meta': {
                    'netbox': {
                        'name': 'isis_internal',
                        'last_updated': '2024-06-21T01:15:08.943182+00:00',
                    }
                },
                'level': 2,
                'lsp_mtu': 1497,
                'iso': '49.0001.0192.0000.2012.00',
                'interfaces': [
                    {'name': 'bond0.959', 'passive': False},
                    {'name': 'lo', 'passive': True},
                ],
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=False,
            category=None,
            family=None,
            element_id='lldp',
            data={
                'meta': {'netdb': {'datasource': 'netbox', 'weight': 150}},
                'interfaces': ['bond0', 'eth6', 'eth7'],
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=False,
            category='services',
            family=None,
            element_id='dhcp_server',
            data={
                'meta': {
                    'netbox': {
                        'id': 1,
                        'url': 'https://netbox.example.net/ipam/services/1/',
                        'last_updated': '2024-06-23T01:57:29.635963+00:00',
                    },
                    'netdb': {'datasource': 'netbox', 'weight': 150},
                },
                'networks': [
                    {
                        'router_ip': '10.10.10.1',
                        'network': '10.10.10.0/24',
                        'ranges': [
                            {
                                'start_address': '10.10.10.100',
                                'end_address': '10.10.10.254',
                            }
                        ],
                    },
                    {
                        'router_ip': '192.168.1.129',
                        'network': '192.168.1.128/26',
                        'ranges': [
                            {
                                'start_address': '192.168.1.138',
                                'end_address': '192.168.1.190',
                            }
                        ],
                    },
                ],
            },
        ),
    ]


def mock_standard_protocol_column(check_override=False):
    """
    Standard protocol data column
    """
    ret = {
        'ROUTER1': {
            'isis': {
                'interfaces': [
                    {'name': 'bond0.959', 'passive': False},
                    {'name': 'lo', 'passive': True},
                ],
                'iso': '49.0001.0192.0000.2012.00',
                'level': 2,
                'lsp_mtu': 1497,
                'meta': {
                    'netbox': {
                        'last_updated': '2024-06-21T01:15:08.943182+00:00',
                        'name': 'isis_internal',
                    },
                    'netdb': {'datasource': 'netbox', 'weight': 150},
                },
            },
            'lldp': {
                'interfaces': [
                    'bond0',
                    'eth6',
                    'eth7',
                ],
                'meta': {
                    'netdb': {
                        'datasource': 'netbox',
                        'weight': 150,
                    },
                },
            },
            'services': {
                'dhcp_server': {
                    'meta': {
                        'netbox': {
                            'id': 1,
                            'last_updated': '2024-06-23T01:57:29.635963+00:00',
                            'url': 'https://netbox.example.net/ipam/services/1/',
                        },
                        'netdb': {
                            'datasource': 'netbox',
                            'weight': 150,
                        },
                    },
                    'networks': [
                        {
                            'network': '10.10.10.0/24',
                            'ranges': [
                                {
                                    'end_address': '10.10.10.254',
                                    'start_address': '10.10.10.100',
                                },
                            ],
                            'router_ip': '10.10.10.1',
                        },
                        {
                            'network': '192.168.1.128/26',
                            'ranges': [
                                {
                                    'end_address': '192.168.1.190',
                                    'start_address': '192.168.1.138',
                                },
                            ],
                            'router_ip': '192.168.1.129',
                        },
                    ],
                },
            },
        }
    }

    if check_override:
        ret['ROUTER1']['lldp']['interfaces'] = [
            'bond0',
            'eth6',
        ]

        ret['ROUTER1']['lldp']['meta']['netdb']['override'] = True

    return ret
