from unittest.mock import patch
from pprint import pprint

import pytest

from mocked_data import device, interface, protocol, bgp, firewall, policy
from fastapi.encoders import jsonable_encoder

from models.columns.device import DeviceContainer
from models.columns.interface import InterfaceContainer
from models.columns.protocol import ProtocolContainer
from models.columns.bgp import BGPContainer
from models.columns.firewall import FirewallContainer
from models.columns.policy import PolicyContainer

from util.exception import NetDBException

from mocked_utils import mock_mongo_api

with patch.dict(
    'sys.modules',
    {
        'util.mongo_api': mock_mongo_api,
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
            'protocol',
            ProtocolContainer(
                datasource='netbox',
                weight=150,
                column=protocol.mock_standard_protocol_data(),
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
    assert odm.pruned_column == jsonable_encoder(container.column, exclude_none=True)
    assert isinstance(odm.mongo, mock_mongo_api.MongoAPI)


@pytest.mark.parametrize(
    'column_type',
    [('device'), ('interface'), ('protocol'), ('bgp'), ('firewall'), ('policy')],
)
def test_column_odm_read_init(column_type):
    """
    Test ColumnODM container read initialization for all column types.
    """
    odm = column_odm.ColumnODM(column_type=column_type)

    assert odm.column_type == column_type
    assert isinstance(odm.mongo, mock_mongo_api.MongoAPI)


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
    'container, documents',
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
            ProtocolContainer(
                datasource='netbox',
                weight=150,
                column=protocol.mock_standard_protocol_data(),
            ),
            protocol.mock_standard_protocol_documents(),
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
def test_column_odm_document_generation(container, documents):
    """
    Test that ColumnODM container load initialization generates the correct
    MongoDB documents.
    """
    odm = column_odm.ColumnODM(container=container)

    # Show all NetdbDocument documents in case of failure.
    pprint(odm.documents)

    assert odm.documents == documents


@pytest.mark.parametrize(
    'column_type,column',
    [
        ('device', device.mock_standard_device_column()),
        ('interface', interface.mock_standard_interface_column()),
        ('protocol', protocol.mock_standard_protocol_column()),
        ('bgp', bgp.mock_standard_bgp_column()),
        ('firewall', firewall.mock_standard_firewall_column()),
        ('policy', policy.mock_standard_policy_column()),
    ],
)
def test_column_odm_fetch_generate_column(column_type, column):
    """
    Test ColumnODM fetch and generate for all column types.
    """

    #
    # We run this test with overrides disabled.
    #
    out = (
        column_odm.ColumnODM(column_type=column_type)
        .fetch(enable_overrides=False)
        .generate_column()
        .pruned_column
    )

    assert out == column


@pytest.mark.parametrize(
    'column_type,column',
    [
        ('interface', interface.mock_standard_interface_column(check_override=True)),
        ('protocol', protocol.mock_standard_protocol_column(check_override=True)),
        ('bgp', bgp.mock_standard_bgp_column(check_override=True)),
        ('firewall', firewall.mock_standard_firewall_column(check_override=True)),
        ('policy', policy.mock_standard_policy_column(check_override=True)),
    ],
)
def test_column_odm_fetch_with_overrides(column_type, column):
    """
    Test ColumnODM fetch and generate for all column types with overrides enabled.
    """

    #
    # We run this test with overrides enabled.
    #
    out = (
        column_odm.ColumnODM(column_type=column_type)
        .fetch(enable_overrides=True)
        .generate_column()
        .pruned_column
    )

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
            ProtocolContainer(
                datasource='netbox',
                weight=150,
                column=protocol.mock_standard_protocol_data(),
            ),
            'netbox',
            protocol.mock_standard_protocol_documents(),
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
            ProtocolContainer(
                datasource='netbox',
                weight=150,
                column=protocol.mock_standard_protocol_data(),
            ),
            protocol.mock_standard_protocol_documents(),
            3,
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
        ('protocol', {'set_id': 'ROUTER1'}),
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
            ProtocolContainer(
                datasource='netbox',
                weight=150,
                column=protocol.mock_standard_protocol_data(),
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
