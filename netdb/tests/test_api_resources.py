import pytest

from util import api_resources


@pytest.mark.parametrize(
    'datasource,set_id,category,family,element_id,kwargs,result',
    [
        ('netbox', None, None, None, None, {}, {'datasource': 'netbox'}),
        (
            'netbox',
            'ROUTER1',
            None,
            None,
            None,
            {},
            {'datasource': 'netbox', 'set_id': 'ROUTER1'},
        ),
        (
            'netbox',
            None,
            'peer_groups',
            None,
            None,
            {},
            {'category': 'peer_groups', 'datasource': 'netbox'},
        ),
        (
            'netbox',
            None,
            None,
            'ipv4',
            None,
            {},
            {'datasource': 'netbox', 'family': 'ipv4'},
        ),
        (
            'netbox',
            None,
            None,
            None,
            '192.168.1.1',
            {},
            {'datasource': 'netbox', 'element_id': '192.168.1.1'},
        ),
        (
            'netbox',
            'ROUTER1',
            None,
            None,
            None,
            {'element_id': '192.168.1.1'},
            {'datasource': 'netbox', 'element_id': '192.168.1.1', 'set_id': 'ROUTER1'},
        ),
        (
            'netbox',
            'ROUTER1',
            None,
            None,
            None,
            {'set_id': 'ROUTER2'},
            {'datasource': 'netbox', 'set_id': 'ROUTER2'},
        ),
    ],
)
def test_generate_filter(
    datasource, set_id, category, family, element_id, kwargs, result
):
    """
    Test generate_filter() helper function
    """
    ret = api_resources.generate_filter(
        datasource, set_id, category, family, element_id, **kwargs
    )

    assert ret == result


@pytest.mark.parametrize(
    'kwargs',
    [
        ({'datasource': 'netbox'}),
        ({'datasource': 'netbox', 'set_id': 'ROUTER1'}),
        ({'category': 'peer_groups', 'datasource': 'netbox'}),
        ({'datasource': 'netbox', 'family': 'ipv4'}),
        ({'datasource': 'netbox', 'element_id': '192.168.1.1'}),
    ],
)
def test_generate_filter_kwargs_only(kwargs):
    """
    Test generate_filter() helper function with only kwargs
    """
    assert api_resources.generate_filter(**kwargs) == kwargs
