from models.types import OverrideDocument


def mock_override_documents():
    """
    Standard override data in document list format
    """
    return [
        OverrideDocument(
            column_type='bgp',
            set_id='ROUTER1',
            category='neighbors',
            family=None,
            element_id='169.254.169.254',
            data={
                'family': {
                    'ipv4': {
                        'nhs': True,
                        'route_map': {
                            'import': 'REJECT-ALL',
                            'export': '4-TRANSIT-OUT',
                        },
                    }
                },
            },
        ),
        OverrideDocument(
            column_type='firewall',
            set_id='ROUTER1',
            category='groups',
            family='ipv6',
            element_id='trusted6',
            data={
                'type': 'network',
                'networks': ['fd00:cb00::/32', 'fd00:4700::/32', 'fd00:4800::/32'],
            },
        ),
        OverrideDocument(
            column_type='interface',
            set_id='ROUTER1',
            category=None,
            family=None,
            element_id='bond0.100',
            data={
                'disabled': True,
            },
        ),
        OverrideDocument(
            column_type='policy',
            set_id='ROUTER1',
            category='route_maps',
            family='ipv4',
            element_id='4-PEER-OUT',
            data={
                'rules': [
                    {
                        'action': 'permit',
                        'match': {'prefix_list': '4-65000-PREFIXES'},
                        'number': 50,
                    },
                    {
                        'action': 'permit',
                        'match': {'prefix_list': '4-65005-PREFIXES'},
                        'number': 55,
                    },
                    {'action': 'deny', 'number': 99},
                ]
            },
        ),
        OverrideDocument(
            column_type='protocol',
            set_id='ROUTER1',
            category=None,
            family=None,
            element_id='lldp',
            data={
                'interfaces': ['bond0', 'eth6'],
            },
        ),
    ]
