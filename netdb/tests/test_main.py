from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

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
