from pprint import pprint
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

import pytest

from mocked_data import interface
from mocked_utils import mock_mongo_api

mock_defaults = MagicMock(DB_NAME='netdb', TRANSACTIONS=True, READ_ONLY=False)


def _container(column_type, datasource, weight, column):
    """
    Helper function to create NetDB data containers
    """
    return {
        'column_type': column_type,
        'datasource': datasource,
        'weight': weight,
        'column': column,
    }


with patch.dict(
    'sys.modules',
    {
        'util.mongo_api': mock_mongo_api,
        'config.defaults': mock_defaults,
    },
):
    import main


client = TestClient(main.app)


def test_get_root():
    """
    Test a GET request to API root.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'name': 'NetDB API version 2', 'status': 'up'}


def test_get_column_root():
    """
    Test a GET request to API '/column' endpoint.

    Expected result:
        A list of available columns

    """
    response = client.get("/column")
    assert response.status_code == 200
    assert response.json() == {
        'comment': 'Available NetDB columns.',
        'error': False,
        'out': ['device', 'firewall', 'policy', 'interface', 'bgp', 'igp'],
        'result': True,
    }


@pytest.mark.parametrize(
    'column,get_string,code,result',
    [
        (
            'bgp',
            'category=neighbors&datasource=netbox',
            200,
            {
                'comment': 'Column data for bgp column.',
                'error': False,
                'out': {
                    'ROUTER1': {
                        'neighbors': {
                            '10.0.66.88': {
                                'meta': {
                                    'netdb': {'datasource': 'netbox', 'weight': 150}
                                },
                                'peer_group': '4_AS65000',
                                'type': 'ebgp',
                            },
                            'fd00::66:88': {
                                'meta': {
                                    'netdb': {'datasource': 'netbox', 'weight': 150}
                                },
                                'peer_group': '6_AS65000',
                                'type': 'ebgp',
                            },
                        }
                    }
                },
                'result': True,
            },
        ),
        (
            'bgp',
            'category=neighbors&datasource=repo',
            200,
            {
                'comment': 'Column data for bgp column.',
                'error': False,
                'out': {
                    'ROUTER1': {
                        'neighbors': {
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
                        }
                    }
                },
                'result': True,
            },
        ),
        (
            'bgp',
            'datasource=red_herring',
            200,
            {
                'comment': 'Column data for bgp column.',
                'error': False,
                'out': {},
                'result': True,
            },
        ),
        (
            'interface',
            'set_id=ROUTER1&element_id=bond0',
            200,
            {
                'comment': 'Column data for interface column.',
                'error': False,
                'out': {
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
                        }
                    }
                },
                'result': True,
            },
        ),
        (
            'igp',
            '',
            200,
            {
                'comment': 'Column data for igp column.',
                'error': False,
                'out': {
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
                },
                'result': True,
            },
        ),
        (
            'device',
            'set_id=ROUTER1',
            200,
            {
                'comment': 'Column data for device column.',
                'error': False,
                'out': {
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
                                    {
                                        'end_address': '10.5.130.254',
                                        'start_address': '10.5.130.100',
                                    }
                                ],
                                'router_ip': '10.5.130.1',
                            },
                            {
                                'network': '192.0.2.128/26',
                                'ranges': [
                                    {
                                        'end_address': '192.0.2.190',
                                        'start_address': '192.0.2.138',
                                    }
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
                        'roles': [
                            'core_router',
                            'edge_router',
                            'firewall',
                            'internal_router',
                        ],
                    }
                },
                'result': True,
            },
        ),
        (
            'firewall',
            'category=zone_policy',
            200,
            {
                'comment': 'Column data for firewall column.',
                'error': False,
                'out': {
                    'ROUTER1': {
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
                        }
                    }
                },
                'result': True,
            },
        ),
        (
            'policy',
            'set_id=ROUTER1&category=route_maps&family=ipv4&element_id=4-PEER-OUT',
            200,
            {
                'comment': 'Column data for policy column.',
                'error': False,
                'out': {
                    'ROUTER1': {
                        'route_maps': {
                            'ipv4': {
                                '4-PEER-OUT': {
                                    'meta': {
                                        'netdb': {'datasource': 'repo', 'weight': 50}
                                    },
                                    'rules': [
                                        {
                                            'action': 'permit',
                                            'match': {
                                                'prefix_list': '4-65000-PREFIXES'
                                            },
                                            'number': 50,
                                        },
                                        {'action': 'deny', 'number': 99},
                                    ],
                                }
                            }
                        }
                    }
                },
                'result': True,
            },
        ),
    ],
)
def test_get_column(column, get_string, code, result):
    """
    Test a GET request to API '/column' endpoint.

    Expected result:
       All of the interfaces for ROUTER1 in column dictionary format

    """
    response = client.get(f"/column/{column}?{get_string}")

    pprint(response.json())

    assert response.status_code == code
    assert response.json() == result


@pytest.mark.parametrize(
    'column,get_string,code,result',
    [
        (
            'bgp',
            'datasource=netbox',
            200,
            {
                'comment': 'bgp column: 0 elements deleted.',
                'error': False,
                'out': None,
                'result': True,
            },
        ),
        (
            'bgp',
            'datasource=netbox&category=neighbors',
            200,
            {
                'comment': 'bgp column: 0 elements deleted.',
                'error': False,
                'out': None,
                'result': True,
            },
        ),
        (
            'bgp',
            '',
            422,
            {
                'comment': 'NetDB says: FastAPI returned a validation error.',
                'error': False,
                'out': {
                    'detail': [
                        {
                            'input': None,
                            'loc': ['query', 'datasource'],
                            'msg': 'Field required',
                            'type': 'missing',
                        }
                    ]
                },
                'result': False,
            },
        ),
        (
            'device',
            'datasource=netbox',
            200,
            {
                'comment': 'device column: 0 elements deleted.',
                'error': False,
                'out': None,
                'result': True,
            },
        ),
        (
            'interface',
            'datasource=netbox',
            200,
            {
                'comment': 'interface column: 0 elements deleted.',
                'error': False,
                'out': None,
                'result': True,
            },
        ),
        (
            'igp',
            'datasource=netbox',
            200,
            {
                'comment': 'igp column: 0 elements deleted.',
                'error': False,
                'out': None,
                'result': True,
            },
        ),
        (
            'policy',
            'datasource=repo',
            200,
            {
                'comment': 'policy column: 0 elements deleted.',
                'error': False,
                'out': None,
                'result': True,
            },
        ),
        (
            'firewall',
            'datasource=repo',
            200,
            {
                'comment': 'firewall column: 0 elements deleted.',
                'error': False,
                'out': None,
                'result': True,
            },
        ),
    ],
)
def test_delete_column(column, get_string, code, result):
    """
    Test a DELETE request to API '/column' endpoint.

    Expected result:
       All of the interfaces for ROUTER1 in column dictionary format

    """
    response = client.delete(f"/column/{column}?{get_string}")

    assert response.status_code == code
    assert response.json() == result


def test_get_column_set():
    """
    Test a GET request to API '/column/interface/router1' endpoint.

    Expected result:
       All of the interfaces for ROUTER1 in column dictionary format

    """
    response = client.get("/column/interface/router1")
    assert response.status_code == 200
    assert response.json() == {
        'comment': 'Column data for interface column.',
        'error': False,
        'out': interface.mock_standard_interface_column(),
        'result': True,
    }


def test_post_validate():
    """
    Test a POST request to API '/validate' endpoint.

    Expected result:
       A successful validation result

    """
    response = client.post(
        "/validate",
        json=_container(
            'interface', 'netbox', 150, interface.mock_standard_interface_data()
        ),
    )
    assert response.status_code == 200
    assert response.json() == {
        'comment': 'Validation successful.',
        'error': False,
        'out': None,
        'result': True,
    }


def test_post_validate_fail():
    """
    Test a POST request to API '/validate' endpoint.

    Expected result:
       A validation failure for no such device / router found

    """
    response = client.post(
        "/validate",
        json=_container(
            'interface',
            'netbox',
            150,
            interface.mock_nonexistent_device_interface_data(),
        ),
    )
    assert response.status_code == 422
    assert response.json() == {
        'comment': 'ROUTER3: device not registered.',
        'error': True,
        'result': False,
    }


def test_post_validate_pydantic_fail():
    """
    Test a POST request to API '/validate' endpoint.

    Expected result:
       A pydantic validation failure for invalid input data

    """
    response = client.post(
        "/validate",
        json=_container(
            'interface',
            'netbox',
            150,
            interface.mock_invalid_interface_data(),
        ),
    )
    assert response.status_code == 422
    assert response.json() == interface.mock_invalid_interface_pydantic_return()


def test_post_column():
    """
    Test a POST request to API '/column' endpoint.

    Expected result:
       A successful column reload result

    """
    response = client.post(
        "/column",
        json=_container(
            'interface', 'netbox', 150, interface.mock_standard_interface_data()
        ),
    )
    assert response.status_code == 200
    assert response.json() == {
        'comment': 'Column reload successful.',
        'error': False,
        'out': interface.mock_standard_interface_pydantic_return(),
        'result': True,
    }


def test_post_column_fail():
    """
    Test a POST request to API '/column' endpoint.

    Expected result:
       A validation failure for no such device / router found

    """
    response = client.post(
        "/column",
        json=_container(
            'interface',
            'netbox',
            150,
            interface.mock_nonexistent_device_interface_data(),
        ),
    )
    assert response.status_code == 422
    assert response.json() == {
        'comment': 'ROUTER3: device not registered.',
        'error': True,
        'result': False,
    }


def test_post_column_pydantic_fail():
    """
    Test a POST request to API '/column' endpoint.

    Expected result:
       A pydantic validation failure for invalid input data

    """
    response = client.post(
        "/column",
        json=_container(
            'interface',
            'netbox',
            150,
            interface.mock_invalid_interface_data(),
        ),
    )
    assert response.status_code == 422
    assert response.json() == interface.mock_invalid_interface_pydantic_return()


def test_put_column():
    """
    Test a PUT request to API '/column' endpoint.

    Expected result:
       A successful column replace result with number of documents replaced

    """

    response = client.put(
        "/column",
        json=_container(
            'interface', 'netbox', 150, interface.mock_standard_interface_data()
        ),
    )
    assert response.status_code == 200
    assert response.json() == {
        'result': True,
        'error': False,
        'out': None,
        'comment': 'interface column: 7 elements successfully replaced.',
    }


def test_put_column_fail():
    """
    Test a PUT request to API '/column' endpoint.

    Expected result:
       A validation failure for no such device / router found

    """
    response = client.put(
        "/column",
        json=_container(
            'interface',
            'netbox',
            150,
            interface.mock_nonexistent_device_interface_data(),
        ),
    )
    assert response.status_code == 422
    assert response.json() == {
        'comment': 'ROUTER3: device not registered.',
        'error': True,
        'result': False,
    }


def test_put_column_pydantic_fail():
    """
    Test a PUT request to API '/column' endpoint.

    Expected result:
       A pydantic validation failure for invalid input data

    """
    response = client.put(
        "/column",
        json=_container(
            'interface',
            'netbox',
            150,
            interface.mock_invalid_interface_data(),
        ),
    )
    assert response.status_code == 422
    assert response.json() == interface.mock_invalid_interface_pydantic_return()
