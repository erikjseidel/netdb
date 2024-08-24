from odm.document_models import NetdbDocument


def mock_standard_device_data():
    """
    Standard device data from an SoT like Netbox that should successfully load into netdb.
    """
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


def mock_standard_device_documents():
    """
    Standard device data in MongoDB document list format
    """
    return [
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=True,
            category=None,
            family=None,
            element_id=None,
            data={
                'location': 'New York, New York',
                'providers': ['big-isp'],
                'roles': ['core_router', 'edge_router', 'firewall', 'internal_router'],
                'node_name': 'EXAMPLE3',
                'meta': {
                    'netbox': {
                        'id': 2,
                        'url': 'https://netbox.example.net/dcim/devices/1/',
                        'status': 'ACTIVE',
                        'last_updated': '2024-06-22T02:31:23.554719+00:00',
                    }
                },
                'cvars': {
                    'ibgp_ipv4': '10.0.16.10',
                    'ibgp_ipv6': 'fd00:10::16:10',
                    'iso': '49.0001.0192.0000.0210.00',
                    'router_id': '192.0.2.10',
                    'local_asn': 65090,
                    'primary_ipv4': '192.0.2.10',
                    'primary_ipv6': '2001:db8::10',
                    'dns_servers': ['1.0.0.1', '1.1.1.1'],
                    'znsl_prefixes': ['192.0.2.0/24', '2001:db8::/32'],
                    'primary_contact': 'contact@help.us',
                    'lldp_interfaces': [
                        'bond0',
                        'bond1',
                        'bond0.100',
                        'bond1.100',
                        'eth0',
                        'eth1',
                        'eth2',
                        'eth3',
                    ],
                },
                'dhcp_servers': [
                    {
                        'router_ip': '10.5.130.1',
                        'network': '10.5.130.0/24',
                        'ranges': [
                            {
                                'start_address': '10.5.130.100',
                                'end_address': '10.5.130.254',
                            }
                        ],
                    },
                    {
                        'router_ip': '192.0.2.129',
                        'network': '192.0.2.128/26',
                        'ranges': [
                            {
                                'start_address': '192.0.2.138',
                                'end_address': '192.0.2.190',
                            }
                        ],
                    },
                ],
            },
        ),
    ]


def mock_standard_device_column():
    """
    Standard device data column
    """
    return {
        'ROUTER1': {
            'cvars': {
                'dns_servers': ['1.0.0.1', '1.1.1.1'],
                'ibgp_ipv4': '10.0.16.10',
                'ibgp_ipv6': 'fd00:10::16:10',
                'iso': '49.0001.0192.0000.0210.00',
                'lldp_interfaces': [
                    'bond0',
                    'bond1',
                    'bond0.100',
                    'bond1.100',
                    'eth0',
                    'eth1',
                    'eth2',
                    'eth3',
                ],
                'local_asn': 65090,
                'primary_contact': 'contact@help.us',
                'primary_ipv4': '192.0.2.10',
                'primary_ipv6': '2001:db8::10',
                'router_id': '192.0.2.10',
                'znsl_prefixes': ['192.0.2.0/24', '2001:db8::/32'],
            },
            'dhcp_servers': [
                {
                    'network': '10.5.130.0/24',
                    'ranges': [
                        {'end_address': '10.5.130.254', 'start_address': '10.5.130.100'}
                    ],
                    'router_ip': '10.5.130.1',
                },
                {
                    'network': '192.0.2.128/26',
                    'ranges': [
                        {'end_address': '192.0.2.190', 'start_address': '192.0.2.138'}
                    ],
                    'router_ip': '192.0.2.129',
                },
            ],
            'location': 'New York, New York',
            'meta': {
                'netbox': {
                    'id': 2,
                    'last_updated': '2024-06-22T02:31:23.554719+00:00',
                    'status': 'ACTIVE',
                    'url': 'https://netbox.example.net/dcim/devices/1/',
                },
                'netdb': {'datasource': 'netbox', 'weight': 150},
            },
            'node_name': 'EXAMPLE3',
            'providers': ['big-isp'],
            'roles': ['core_router', 'edge_router', 'firewall', 'internal_router'],
        }
    }
