from typing import Union
from unittest.mock import MagicMock, patch
from pprint import pprint

import pytest

from mocked_data import device, interface, igp, bgp, firewall, policy
from fastapi.encoders import jsonable_encoder

from models.columns.device import DeviceContainer
from models.columns.interface import InterfaceContainer
from models.columns.igp import IGPContainer
from models.columns.bgp import BGPContainer
from models.columns.firewall import FirewallContainer
from models.columns.policy import PolicyContainer

from util.exception import NetDBException


class MockMongoAPI:

    def __init__(self, database: str, collection: str):
        self.column_type = collection
        self.filter = None
        self.documents = []

    def read(self, query: Union[dict, None] = None) -> list:
        """
        Mock MongoAPI read returns for valid column types.
        """
        match self.column_type:
            case 'device':
                return device.mock_standard_device_documents()
            case 'interface':
                return interface.mock_standard_interface_documents()
            case 'igp':
                return igp.mock_standard_igp_documents()
            case 'bgp':
                return bgp.mock_standard_bgp_documents()
            case 'firewall':
                return firewall.mock_standard_firewall_documents()
            case 'policy':
                return policy.mock_standard_policy_documents()

    def reload(self, documents: list, filt: dict) -> bool:
        """
        Mock MongoAPI reload
        """
        self.filter = filt
        self.documents = documents

        return True

    def replace_one(self, document: dict) -> bool:
        """
        Mock MongoAPI replace
        """
        self.documents.append(document)

        return True

    def delete_many(self, filt: dict) -> int:
        """
        Mock MongoAPI delete
        """
        self.filter = filt

        return 0


mock_defaults = MagicMock(DB_NAME='netdb', TRANSACTIONS=True, READ_ONLY=False)

with patch.dict(
    'sys.modules',
    {
        'util.mongo_api': MagicMock(MongoAPI=MockMongoAPI),
        'config.defaults': mock_defaults,
    },
):
    from odm import column_odm


@pytest.mark.parametrize(
    'column_type,container',
    [
        (
            'device',
            DeviceContainer(
                datasource='netbox',
                weight=150,
                column=device.mock_standard_device_data(),
            ),
        ),
        (
            'interface',
            InterfaceContainer(
                datasource='netbox',
                weight=150,
                column=interface.mock_standard_interface_data(),
            ),
        ),
        (
            'igp',
            IGPContainer(
                datasource='netbox', weight=150, column=igp.mock_standard_igp_data()
            ),
        ),
        (
            'bgp',
            BGPContainer(
                datasource='netbox',
                weight=150,
                column=bgp.mock_standard_bgp_data(source='netbox'),
            ),
        ),
        (
            'bgp',
            BGPContainer(
                datasource='peering_manager',
                weight=100,
                column=bgp.mock_standard_bgp_data(source='peering_manager'),
            ),
        ),
        (
            'bgp',
            BGPContainer(
                datasource='repo',
                weight=50,
                column=bgp.mock_standard_bgp_data(source='repo'),
            ),
        ),
        (
            'firewall',
            FirewallContainer(
                datasource='repo',
                weight=50,
                column=firewall.mock_standard_firewall_data(),
            ),
        ),
        (
            'policy',
            PolicyContainer(
                datasource='repo', weight=50, column=policy.mock_standard_policy_data()
            ),
        ),
    ],
)
def test_column_odm_container_init(column_type, container):
    """
    Test ColumnODM container load initialization for all column types.
    """
    odm = column_odm.ColumnODM(container=container)

    assert odm.column_type == column_type
    assert odm.column == jsonable_encoder(container.column, exclude_none=True)
    assert isinstance(odm.mongo, MockMongoAPI)


@pytest.mark.parametrize(
    'column_type',
    [('device'), ('interface'), ('igp'), ('bgp'), ('firewall'), ('policy')],
)
def test_column_odm_read_init(column_type):
    """
    Test ColumnODM container read initialization for all column types.
    """
    odm = column_odm.ColumnODM(column_type=column_type)

    assert odm.column_type == column_type
    assert isinstance(odm.mongo, MockMongoAPI)


def test_column_odm_read_init_bad_column():
    """
    Test ColumnODM container read initialization for an invalid column type.
    """
    message = None
    code = None
    try:
        column_odm.ColumnODM(column_type='red_herring')
    except NetDBException as e:
        message = e.message
        code = e.code

    assert message == 'Column red_herring not available'
    assert code == 422


@pytest.mark.parametrize(
    'container, mongo_data',
    [
        (
            DeviceContainer(
                datasource='netbox',
                weight=150,
                column=device.mock_standard_device_data(),
            ),
            device.mock_standard_device_documents(),
        ),
        (
            InterfaceContainer(
                datasource='netbox',
                weight=150,
                column=interface.mock_standard_interface_data(),
            ),
            interface.mock_standard_interface_documents(),
        ),
        (
            IGPContainer(
                datasource='netbox',
                weight=150,
                column=igp.mock_standard_igp_data(),
            ),
            igp.mock_standard_igp_documents(),
        ),
        (
            BGPContainer(
                datasource='netbox',
                weight=150,
                column=bgp.mock_standard_bgp_data(source='netbox'),
            ),
            bgp.mock_standard_bgp_documents(source='netbox'),
        ),
        (
            BGPContainer(
                datasource='peering_manager',
                weight=100,
                column=bgp.mock_standard_bgp_data(source='peering_manager'),
            ),
            bgp.mock_standard_bgp_documents(source='peering_manager'),
        ),
        (
            BGPContainer(
                datasource='repo',
                weight=50,
                column=bgp.mock_standard_bgp_data(source='repo'),
            ),
            bgp.mock_standard_bgp_documents(source='repo'),
        ),
        (
            FirewallContainer(
                datasource='repo',
                weight=50,
                column=firewall.mock_standard_firewall_data(),
            ),
            firewall.mock_standard_firewall_documents(),
        ),
        (
            PolicyContainer(
                datasource='repo',
                weight=50,
                column=policy.mock_standard_policy_data(),
            ),
            policy.mock_standard_policy_documents(),
        ),
    ],
)
def test_column_odm_mongo_generation(container, mongo_data):
    """
    Test that ColumnODM container load initialization generates the correct
    MongoDB documents.
    """
    odm = column_odm.ColumnODM(container=container)

    # Show all mongo_data in case of failure.
    pprint(odm.mongo_data)

    assert odm.mongo_data == mongo_data


@pytest.mark.parametrize(
    'column_type,column',
    [
        ('device', device.mock_standard_device_column()),
        ('interface', interface.mock_standard_interface_column()),
        ('igp', igp.mock_standard_igp_column()),
        ('bgp', bgp.mock_standard_bgp_column()),
        ('firewall', firewall.mock_standard_firewall_column()),
        ('policy', policy.mock_standard_policy_column()),
    ],
)
def test_column_odm_fetch(column_type, column):
    """
    Test ColumnODM fetch for all column types.
    """
    out = column_odm.ColumnODM(column_type=column_type).fetch()

    # Show all mongo_data in case of failure.
    pprint(out)

    assert out == column


@pytest.mark.parametrize(
    'container,datasource,documents',
    [
        (
            DeviceContainer(
                datasource='netbox',
                weight=150,
                column=device.mock_standard_device_data(),
            ),
            'netbox',
            device.mock_standard_device_documents(),
        ),
        (
            InterfaceContainer(
                datasource='netbox',
                weight=150,
                column=interface.mock_standard_interface_data(),
            ),
            'netbox',
            interface.mock_standard_interface_documents(),
        ),
        (
            IGPContainer(
                datasource='netbox',
                weight=150,
                column=igp.mock_standard_igp_data(),
            ),
            'netbox',
            igp.mock_standard_igp_documents(),
        ),
        (
            BGPContainer(
                datasource='netbox',
                weight=150,
                column=bgp.mock_standard_bgp_data(source='netbox'),
            ),
            'netbox',
            bgp.mock_standard_bgp_documents(source='netbox'),
        ),
        (
            BGPContainer(
                datasource='peering_manager',
                weight=100,
                column=bgp.mock_standard_bgp_data(source='peering_manager'),
            ),
            'peering_manager',
            bgp.mock_standard_bgp_documents(source='peering_manager'),
        ),
        (
            BGPContainer(
                datasource='repo',
                weight=50,
                column=bgp.mock_standard_bgp_data(source='repo'),
            ),
            'repo',
            bgp.mock_standard_bgp_documents(source='repo'),
        ),
        (
            FirewallContainer(
                datasource='repo',
                weight=50,
                column=firewall.mock_standard_firewall_data(),
            ),
            'repo',
            firewall.mock_standard_firewall_documents(),
        ),
        (
            PolicyContainer(
                datasource='repo',
                weight=50,
                column=policy.mock_standard_policy_data(),
            ),
            'repo',
            policy.mock_standard_policy_documents(),
        ),
    ],
)
def test_column_odm_reload(container, datasource, documents):
    """
    Test ColumnODM reload for all column types.
    """
    odm = column_odm.ColumnODM(container=container)
    odm.reload()

    assert odm.mongo.filter == {'datasource': datasource}  # pylint: disable=E1101
    assert odm.mongo.documents == documents  # pylint: disable=E1101


@pytest.mark.parametrize(
    'container,error_code,error_message',
    [
        (
            InterfaceContainer(
                datasource='netbox',
                weight=150,
                column=interface.mock_nonexistent_device_interface_data(),
            ),
            422,
            'ROUTER3: device not registered.',
        )
    ],
)
def test_column_odm_reload_validation_fail(container, error_code, error_message):
    """
    Test that ColumnODM reload validation fails on non-existent device.
    """
    odm = column_odm.ColumnODM(container=container)

    message = None
    code = None
    try:
        odm.reload()
    except NetDBException as e:
        message = e.message
        code = e.code

    assert message == error_message
    assert code == error_code


@pytest.mark.parametrize(
    'container,documents,count',
    [
        (
            DeviceContainer(
                datasource='netbox',
                weight=150,
                column=device.mock_standard_device_data(),
            ),
            device.mock_standard_device_documents(),
            1,
        ),
        (
            InterfaceContainer(
                datasource='netbox',
                weight=150,
                column=interface.mock_standard_interface_data(),
            ),
            interface.mock_standard_interface_documents(),
            7,
        ),
        (
            IGPContainer(
                datasource='netbox',
                weight=150,
                column=igp.mock_standard_igp_data(),
            ),
            igp.mock_standard_igp_documents(),
            1,
        ),
        (
            BGPContainer(
                datasource='netbox',
                weight=150,
                column=bgp.mock_standard_bgp_data(source='netbox'),
            ),
            bgp.mock_standard_bgp_documents(source='netbox'),
            2,
        ),
        (
            BGPContainer(
                datasource='peering_manager',
                weight=100,
                column=bgp.mock_standard_bgp_data(source='peering_manager'),
            ),
            bgp.mock_standard_bgp_documents(source='peering_manager'),
            2,
        ),
        (
            BGPContainer(
                datasource='repo',
                weight=50,
                column=bgp.mock_standard_bgp_data(source='repo'),
            ),
            bgp.mock_standard_bgp_documents(source='repo'),
            7,
        ),
        (
            FirewallContainer(
                datasource='repo',
                weight=50,
                column=firewall.mock_standard_firewall_data(),
            ),
            firewall.mock_standard_firewall_documents(),
            17,
        ),
        (
            PolicyContainer(
                datasource='repo',
                weight=50,
                column=policy.mock_standard_policy_data(),
            ),
            policy.mock_standard_policy_documents(),
            16,
        ),
    ],
)
def test_column_odm_replace(container, documents, count):
    """
    Test ColumnODM reload for all column types.
    """
    odm = column_odm.ColumnODM(container=container)
    out = odm.replace()

    assert odm.mongo.documents == documents  # pylint: disable=E1101
    assert out == count


@pytest.mark.parametrize(
    'container,error_code,error_message',
    [
        (
            InterfaceContainer(
                datasource='netbox',
                weight=150,
                column=interface.mock_nonexistent_device_interface_data(),
            ),
            422,
            'ROUTER3: device not registered.',
        )
    ],
)
def test_column_odm_replace_fail(container, error_code, error_message):
    """
    Test that ColumnODM replace fails on non-existent device.
    """
    odm = column_odm.ColumnODM(container=container)

    message = None
    code = None
    try:
        odm.replace()
    except NetDBException as e:
        message = e.message
        code = e.code

    assert message == error_message
    assert code == error_code


@pytest.mark.parametrize(
    'column_type, filt',
    [
        ('device', {'set_id': 'ROUTER1'}),
        ('interface', {'set_id': 'ROUTER1', 'element_id': 'bond0'}),
        ('igp', {'set_id': 'ROUTER1'}),
        ('bgp', {'set_id': 'ROUTER1', 'category': 'peer_group', 'element_id': '6_RR'}),
        (
            'firewall',
            {
                'set_id': 'ROUTER1',
                'category': 'group',
                'family': 'ipv4',
                'element_id': 'DMZ4',
            },
        ),
        (
            'policy',
            {
                'set_id': 'ROUTER1',
                'category': 'route_map',
                'family': 'ipv4',
                'element_id': '4-TRANSIT',
            },
        ),
    ],
)
def test_column_odm_delete(column_type, filt):
    """
    Test ColumnODM delete
    """
    odm = column_odm.ColumnODM(column_type=column_type)
    odm.delete(filt)

    assert odm.mongo.filter == filt  # pylint: disable=E1101


def test_column_odm_delete_no_filt_fail():
    """
    Test that ColumnODM delete fails when no filter is set.
    """
    odm = column_odm.ColumnODM(column_type='device')

    message = None
    code = None
    try:
        odm.delete(filt={})
    except NetDBException as e:
        message = e.message
        code = e.code

    assert message == 'Invalid filter.'
    assert code == 422


@pytest.mark.parametrize(
    'container',
    [
        (
            DeviceContainer(
                datasource='netbox',
                weight=150,
                column=device.mock_standard_device_data(),
            )
        ),
        (
            InterfaceContainer(
                datasource='netbox',
                weight=150,
                column=interface.mock_standard_interface_data(),
            )
        ),
        (
            IGPContainer(
                datasource='netbox',
                weight=150,
                column=igp.mock_standard_igp_data(),
            )
        ),
        (
            BGPContainer(
                datasource='netbox',
                weight=150,
                column=bgp.mock_standard_bgp_data(source='netbox'),
            )
        ),
        (
            BGPContainer(
                datasource='peering_manager',
                weight=100,
                column=bgp.mock_standard_bgp_data(source='peering_manager'),
            )
        ),
        (
            BGPContainer(
                datasource='repo',
                weight=50,
                column=bgp.mock_standard_bgp_data(source='repo'),
            )
        ),
        (
            FirewallContainer(
                datasource='repo',
                weight=50,
                column=firewall.mock_standard_firewall_data(),
            )
        ),
        (
            PolicyContainer(
                datasource='repo',
                weight=50,
                column=policy.mock_standard_policy_data(),
            )
        ),
    ],
)
def test_column_odm_validate(container):
    """
    Test ColumnODM validate for all column types.
    """
    odm = column_odm.ColumnODM(container=container)

    odm.validate()  # Should not throw an exception.


@pytest.mark.parametrize(
    'container,error_code,error_message',
    [
        (
            InterfaceContainer(
                datasource='netbox',
                weight=150,
                column=interface.mock_nonexistent_device_interface_data(),
            ),
            422,
            'ROUTER3: device not registered.',
        )
    ],
)
def test_column_odm_validate_fail(container, error_code, error_message):
    """
    Test that ColumnODM validate fails on non-existent device.
    """
    odm = column_odm.ColumnODM(container=container)

    message = None
    code = None
    try:
        odm.validate()
    except NetDBException as e:
        message = e.message
        code = e.code

    assert message == error_message
    assert code == error_code
