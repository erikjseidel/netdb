from models.types import NetdbDocument


def mock_standard_bgp_data(source):
    """
    Standard bgp data which should sucessfully load into netdb.

    source:
       Mock BGP data from an SoT; can be 'netbox', 'pm' or 'repo'

    """
    match source:
        case 'netbox':
            return {
                "ROUTER1": {
                    "neighbors": {
                        "10.0.66.88": {"peer_group": "4_AS65000"},
                        "fd00::66:88": {"peer_group": "6_AS65000"},
                    }
                },
            }

        case 'peering_manager':
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

        case 'repo':
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
                                    "route_map": {
                                        "export": "4-RR-OUT",
                                        "import": "4-RR-IN",
                                    }
                                },
                                "ipv6": {
                                    "route_map": {
                                        "export": "6-RR-OUT",
                                        "import": "6-RR-IN",
                                    }
                                },
                            },
                            "source": "fd00:88::12",
                            "type": "ibgp",
                        },
                    },
                },
            }


def mock_standard_bgp_documents(source=None):
    """
    Standard bgp data as appears in Mongo document format.

    source:
       Mock BGP data from an SoT; can be 'netbox', 'pm' or 'repo'

    """
    documents = [
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category=None,
            family=None,
            element_id='options',
            data={
                'asn': 65000,
                'hold_time': 30,
                'keepalive_time': 10,
                'log_neighbor_changes': True,
                'router_id': '192.0.2.12',
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category=None,
            family=None,
            element_id='address_family',
            data={
                'ipv4': {'redistribute': ['static']},
                'ipv6': {'redistribute': ['static']},
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='peer_groups',
            family=None,
            element_id='4_PG_65001',
            data={
                'type': 'ebgp',
                'family': {
                    'ipv4': {
                        'nhs': True,
                        'route_map': {'import': '4-PG-IN', 'export': '4-PG-OUT'},
                    }
                },
                'remote_asn': 65001,
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='peer_groups',
            family=None,
            element_id='6_PG_65001',
            data={
                'type': 'ebgp',
                'family': {
                    'ipv6': {
                        'nhs': True,
                        'route_map': {'import': '6-PG-IN', 'export': '6-PG-OUT'},
                    }
                },
                'remote_asn': 65001,
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='peer_groups',
            family=None,
            element_id='6_RR',
            data={
                'type': 'ibgp',
                'source': 'fd00:88::12',
                'family': {
                    'ipv4': {'route_map': {'import': '4-RR-IN', 'export': '4-RR-OUT'}},
                    'ipv6': {'route_map': {'import': '6-RR-IN', 'export': '6-RR-OUT'}},
                },
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='neighbors',
            family=None,
            element_id='fd00:88::10',
            data={'type': 'ebgp', 'peer_group': '6_RR'},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='neighbors',
            family=None,
            element_id='fd00:88::11',
            data={'type': 'ebgp', 'peer_group': '6_RR'},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=False,
            category='neighbors',
            family=None,
            element_id='10.0.66.88',
            data={'type': 'ebgp', 'peer_group': '4_AS65000'},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='netbox',
            weight=150,
            flat=False,
            category='neighbors',
            family=None,
            element_id='fd00::66:88',
            data={'type': 'ebgp', 'peer_group': '6_AS65000'},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='peering_manager',
            weight=100,
            flat=False,
            category='neighbors',
            family=None,
            element_id='169.254.169.254',
            data={
                'type': 'ebgp',
                'source': '192.0.2.12',
                'family': {
                    'ipv4': {
                        'nhs': True,
                        'route_map': {
                            'import': '4-TRANSIT-IN',
                            'export': '4-TRANSIT-OUT',
                        },
                    }
                },
                'multihop': 2,
                'password': 'red_herring',
                'remote_asn': 64500,
                'meta': {
                    'peering_manager': {
                        'url': 'https://pm.example.net/api/peering/direct-peering-sessions/1/',
                        'status': 'enabled',
                        'type': 'transit-session',
                    }
                },
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='peering_manager',
            weight=100,
            flat=False,
            category='neighbors',
            family=None,
            element_id='fd00:1ff0:ffff::1',
            data={
                'type': 'ebgp',
                'source': 'fd00::1234:5678:9abc',
                'family': {
                    'ipv6': {
                        'nhs': True,
                        'route_map': {
                            'import': '6-TRANSIT-IN',
                            'export': '6-TRANSIT-OUT',
                        },
                    }
                },
                'multihop': 2,
                'password': 'red_herring',
                'remote_asn': 64500,
                'meta': {
                    'peering_manager': {
                        'url': 'https://pm.example.net/api/peering/direct-peering-sessions/2/',
                        'status': 'enabled',
                        'type': 'transit-session',
                    }
                },
            },
        ),
    ]

    if source:
        return [document for document in documents if document.datasource == source]

    return documents


def mock_standard_bgp_column(check_override=False):
    """
    Standard bgp data column

    """
    ret = {
        'ROUTER1': {
            'address_family': {
                'ipv4': {'redistribute': ['static']},
                'ipv6': {'redistribute': ['static']},
                'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
            },
            'neighbors': {
                '10.0.66.88': {
                    'meta': {'netdb': {'datasource': 'netbox', 'weight': 150}},
                    'peer_group': '4_AS65000',
                    'type': 'ebgp',
                },
                '169.254.169.254': {
                    'family': {
                        'ipv4': {
                            'nhs': True,
                            'route_map': {
                                'export': '4-TRANSIT-OUT',
                                'import': (
                                    'REJECT-ALL' if check_override else '4-TRANSIT-IN'
                                ),
                            },
                        }
                    },
                    'meta': {
                        'netdb': {'datasource': 'peering_manager', 'weight': 100},
                        'peering_manager': {
                            'status': 'enabled',
                            'type': 'transit-session',
                            'url': 'https://pm.example.net/api/peering/direct-peering-sessions/1/',
                        },
                    },
                    'multihop': 2,
                    'password': 'red_herring',
                    'remote_asn': 64500,
                    'source': '192.0.2.12',
                    'type': 'ebgp',
                },
                'fd00:1ff0:ffff::1': {
                    'family': {
                        'ipv6': {
                            'nhs': True,
                            'route_map': {
                                'export': '6-TRANSIT-OUT',
                                'import': '6-TRANSIT-IN',
                            },
                        }
                    },
                    'meta': {
                        'netdb': {'datasource': 'peering_manager', 'weight': 100},
                        'peering_manager': {
                            'status': 'enabled',
                            'type': 'transit-session',
                            'url': 'https://pm.example.net/api/peering/direct-peering-sessions/2/',
                        },
                    },
                    'multihop': 2,
                    'password': 'red_herring',
                    'remote_asn': 64500,
                    'source': 'fd00::1234:5678:9abc',
                    'type': 'ebgp',
                },
                'fd00:88::10': {
                    'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                    'peer_group': '6_RR',
                    'type': 'ebgp',
                },
                'fd00:88::11': {
                    'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                    'peer_group': '6_RR',
                    'type': 'ebgp',
                },
                'fd00::66:88': {
                    'meta': {'netdb': {'datasource': 'netbox', 'weight': 150}},
                    'peer_group': '6_AS65000',
                    'type': 'ebgp',
                },
            },
            'options': {
                'asn': 65000,
                'hold_time': 30,
                'keepalive_time': 10,
                'log_neighbor_changes': True,
                'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                'router_id': '192.0.2.12',
            },
            'peer_groups': {
                '4_PG_65001': {
                    'family': {
                        'ipv4': {
                            'nhs': True,
                            'route_map': {'export': '4-PG-OUT', 'import': '4-PG-IN'},
                        }
                    },
                    'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                    'remote_asn': 65001,
                    'type': 'ebgp',
                },
                '6_PG_65001': {
                    'family': {
                        'ipv6': {
                            'nhs': True,
                            'route_map': {'export': '6-PG-OUT', 'import': '6-PG-IN'},
                        }
                    },
                    'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                    'remote_asn': 65001,
                    'type': 'ebgp',
                },
                '6_RR': {
                    'family': {
                        'ipv4': {
                            'route_map': {'export': '4-RR-OUT', 'import': '4-RR-IN'}
                        },
                        'ipv6': {
                            'route_map': {'export': '6-RR-OUT', 'import': '6-RR-IN'}
                        },
                    },
                    'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                    'source': 'fd00:88::12',
                    'type': 'ibgp',
                },
            },
        }
    }

    if check_override:
        ret['ROUTER1']['neighbors']['169.254.169.254']['meta']['netdb'][
            'override'
        ] = True

    return ret
