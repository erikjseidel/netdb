def mock_standard_igp_data():
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
            }
        }
    }


def mock_standard_igp_documents():
    """
    Standard IGP data in MongoDB document list format
    """
    return [
        {
            'data': {
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
                    }
                },
            },
            'datasource': 'netbox',
            'element_id': 'isis',
            'set_id': 'ROUTER1',
            'weight': 150,
        }
    ]


def mock_standard_igp_column():
    """
    Standard IGP data column
    """
    return {
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
            }
        }
    }
