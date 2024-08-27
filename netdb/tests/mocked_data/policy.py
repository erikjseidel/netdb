from models.types import NetdbDocument


def mock_standard_policy_data():
    """
    Standard policy data which should successfully load into netbox.
    """
    return {
        "ROUTER1": {
            "prefix_lists": {
                "ipv4": {
                    "4-BIG-PREFIXES": {
                        "rules": [{"ge": 1, "le": 7, "prefix": "0.0.0.0/0"}]
                    },
                    "4-DEFAULT-ROUTE": {"rules": [{"prefix": "0.0.0.0/0"}]},
                    "4-MARTIAN-PREFIXES": {
                        "rules": [
                            {"le": 32, "prefix": "0.0.0.0/8"},
                            {"le": 32, "prefix": "10.0.0.0/8"},
                            {"le": 32, "prefix": "192.168.0.0/16"},
                            {"le": 32, "prefix": "172.16.0.0/12"},
                            {"le": 32, "prefix": "100.64.0.0/10"},
                            {"le": 32, "prefix": "127.0.0.0/8"},
                            {"le": 32, "prefix": "169.254.0.0/16"},
                            {"le": 32, "prefix": "192.0.0.0/24"},
                            {"le": 32, "prefix": "192.0.2.0/24"},
                            {"le": 32, "prefix": "198.18.0.0/15"},
                            {"le": 32, "prefix": "198.51.100.0/24"},
                            {"le": 32, "prefix": "203.0.113.0/24"},
                            {"le": 32, "prefix": "224.0.0.0/3"},
                        ]
                    },
                    "4-SMALL-PREFIXES": {
                        "rules": [{"ge": 25, "le": 32, "prefix": "0.0.0.0/0"}]
                    },
                    "4-65000-PREFIXES": {
                        "rules": [
                            {"le": 24, "prefix": "10.0.0.0/8"},
                        ]
                    },
                },
                "ipv6": {
                    "6-BIG-PREFIXES": {
                        "rules": [{"ge": 1, "le": 15, "prefix": "::/0"}]
                    },
                    "6-DEFAULT-ROUTE": {"rules": [{"prefix": "::/0"}]},
                    "6-MARTIAN-PREFIXES": {
                        "rules": [
                            {"le": 128, "prefix": "::/8"},
                            {"le": 128, "prefix": "200::/7"},
                            {"le": 128, "prefix": "2001::/32"},
                            {"le": 128, "prefix": "2001:db8::/32"},
                            {"le": 128, "prefix": "2002::/16"},
                            {"le": 128, "prefix": "3ffe::/16"},
                            {"le": 128, "prefix": "5f00::/8"},
                            {"le": 128, "prefix": "fc00::/7"},
                            {"le": 128, "prefix": "fe80::/10"},
                            {"le": 128, "prefix": "fec0::/10"},
                            {"le": 128, "prefix": "ff00::/8"},
                        ]
                    },
                    "6-SMALL-PREFIXES": {
                        "rules": [{"ge": 49, "le": 128, "prefix": "::/0"}]
                    },
                    "6-65000-PREFIXES": {
                        "rules": [{"le": 64, "prefix": "fd00:abcd::/48"}]
                    },
                },
            },
            "route_maps": {
                "ipv4": {
                    "ALLOW-ALL": {"rules": [{"action": "permit", "number": 99}]},
                    "REJECT-ALL": {"rules": [{"action": "deny", "number": 99}]},
                    "4-PEER-IN": {
                        "rules": [
                            {
                                "action": "permit",
                                "match": {"prefix_list": "4-DEFAULT-ROUTE"},
                                "number": 50,
                                "set": {"local_pref": 100},
                            },
                            {
                                "action": "permit",
                                "match": {"prefix_list": "4-65000-PREFIXES"},
                                "number": 60,
                                "set": {"local_pref": 100},
                            },
                            {"action": "deny", "number": 99},
                        ]
                    },
                    "4-PEER-OUT": {
                        "rules": [
                            {
                                "action": "permit",
                                "match": {"prefix_list": "4-65000-PREFIXES"},
                                "number": 50,
                            },
                            {"action": "deny", "number": 99},
                        ]
                    },
                },
                "ipv6": {
                    "6-PEER-IN": {
                        "rules": [
                            {
                                "action": "permit",
                                "match": {"prefix_list": "6-DEFAULT-ROUTE"},
                                "number": 50,
                                "set": {"local_pref": 100},
                            },
                            {
                                "action": "permit",
                                "match": {"prefix_list": "6-65000-PREFIXES"},
                                "number": 60,
                                "set": {"local_pref": 100},
                            },
                            {"action": "deny", "number": 99},
                        ]
                    },
                    "6-PEER-OUT": {
                        "rules": [
                            {
                                "action": "permit",
                                "match": {"prefix_list": "6-65000-PREFIXES"},
                                "number": 50,
                            },
                            {"action": "deny", "number": 99},
                        ]
                    },
                },
            },
        }
    }


def mock_standard_policy_documents():
    """
    Standard policy data in MongoDB document format
    """
    return [
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='prefix_lists',
            family='ipv4',
            element_id='4-BIG-PREFIXES',
            data={'rules': [{'le': 7, 'ge': 1, 'prefix': '0.0.0.0/0'}]},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='prefix_lists',
            family='ipv4',
            element_id='4-DEFAULT-ROUTE',
            data={'rules': [{'prefix': '0.0.0.0/0'}]},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='prefix_lists',
            family='ipv4',
            element_id='4-MARTIAN-PREFIXES',
            data={
                'rules': [
                    {'le': 32, 'prefix': '0.0.0.0/8'},
                    {'le': 32, 'prefix': '10.0.0.0/8'},
                    {'le': 32, 'prefix': '192.168.0.0/16'},
                    {'le': 32, 'prefix': '172.16.0.0/12'},
                    {'le': 32, 'prefix': '100.64.0.0/10'},
                    {'le': 32, 'prefix': '127.0.0.0/8'},
                    {'le': 32, 'prefix': '169.254.0.0/16'},
                    {'le': 32, 'prefix': '192.0.0.0/24'},
                    {'le': 32, 'prefix': '192.0.2.0/24'},
                    {'le': 32, 'prefix': '198.18.0.0/15'},
                    {'le': 32, 'prefix': '198.51.100.0/24'},
                    {'le': 32, 'prefix': '203.0.113.0/24'},
                    {'le': 32, 'prefix': '224.0.0.0/3'},
                ]
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='prefix_lists',
            family='ipv4',
            element_id='4-SMALL-PREFIXES',
            data={'rules': [{'le': 32, 'ge': 25, 'prefix': '0.0.0.0/0'}]},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='prefix_lists',
            family='ipv4',
            element_id='4-65000-PREFIXES',
            data={'rules': [{'le': 24, 'prefix': '10.0.0.0/8'}]},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='prefix_lists',
            family='ipv6',
            element_id='6-BIG-PREFIXES',
            data={'rules': [{'le': 15, 'ge': 1, 'prefix': '::/0'}]},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='prefix_lists',
            family='ipv6',
            element_id='6-DEFAULT-ROUTE',
            data={'rules': [{'prefix': '::/0'}]},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='prefix_lists',
            family='ipv6',
            element_id='6-MARTIAN-PREFIXES',
            data={
                'rules': [
                    {'le': 128, 'prefix': '::/8'},
                    {'le': 128, 'prefix': '200::/7'},
                    {'le': 128, 'prefix': '2001::/32'},
                    {'le': 128, 'prefix': '2001:db8::/32'},
                    {'le': 128, 'prefix': '2002::/16'},
                    {'le': 128, 'prefix': '3ffe::/16'},
                    {'le': 128, 'prefix': '5f00::/8'},
                    {'le': 128, 'prefix': 'fc00::/7'},
                    {'le': 128, 'prefix': 'fe80::/10'},
                    {'le': 128, 'prefix': 'fec0::/10'},
                    {'le': 128, 'prefix': 'ff00::/8'},
                ]
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='prefix_lists',
            family='ipv6',
            element_id='6-SMALL-PREFIXES',
            data={'rules': [{'le': 128, 'ge': 49, 'prefix': '::/0'}]},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='prefix_lists',
            family='ipv6',
            element_id='6-65000-PREFIXES',
            data={'rules': [{'le': 64, 'prefix': 'fd00:abcd::/48'}]},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='route_maps',
            family='ipv4',
            element_id='ALLOW-ALL',
            data={'rules': [{'action': 'permit', 'number': 99}]},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='route_maps',
            family='ipv4',
            element_id='REJECT-ALL',
            data={'rules': [{'action': 'deny', 'number': 99}]},
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='route_maps',
            family='ipv4',
            element_id='4-PEER-IN',
            data={
                'rules': [
                    {
                        'action': 'permit',
                        'match': {'prefix_list': '4-DEFAULT-ROUTE'},
                        'set': {'local_pref': 100},
                        'number': 50,
                    },
                    {
                        'action': 'permit',
                        'match': {'prefix_list': '4-65000-PREFIXES'},
                        'set': {'local_pref': 100},
                        'number': 60,
                    },
                    {'action': 'deny', 'number': 99},
                ]
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
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
                    {'action': 'deny', 'number': 99},
                ]
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='route_maps',
            family='ipv6',
            element_id='6-PEER-IN',
            data={
                'rules': [
                    {
                        'action': 'permit',
                        'match': {'prefix_list': '6-DEFAULT-ROUTE'},
                        'set': {'local_pref': 100},
                        'number': 50,
                    },
                    {
                        'action': 'permit',
                        'match': {'prefix_list': '6-65000-PREFIXES'},
                        'set': {'local_pref': 100},
                        'number': 60,
                    },
                    {'action': 'deny', 'number': 99},
                ]
            },
        ),
        NetdbDocument(
            set_id='ROUTER1',
            datasource='repo',
            weight=50,
            flat=False,
            category='route_maps',
            family='ipv6',
            element_id='6-PEER-OUT',
            data={
                'rules': [
                    {
                        'action': 'permit',
                        'match': {'prefix_list': '6-65000-PREFIXES'},
                        'number': 50,
                    },
                    {'action': 'deny', 'number': 99},
                ]
            },
        ),
    ]


def mock_standard_policy_column(check_override=False):
    """
    Standard policy data column
    """
    ret = {
        'ROUTER1': {
            'prefix_lists': {
                'ipv4': {
                    '4-65000-PREFIXES': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [{'le': 24, 'prefix': '10.0.0.0/8'}],
                    },
                    '4-BIG-PREFIXES': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [{'ge': 1, 'le': 7, 'prefix': '0.0.0.0/0'}],
                    },
                    '4-DEFAULT-ROUTE': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [{'prefix': '0.0.0.0/0'}],
                    },
                    '4-MARTIAN-PREFIXES': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [
                            {'le': 32, 'prefix': '0.0.0.0/8'},
                            {'le': 32, 'prefix': '10.0.0.0/8'},
                            {'le': 32, 'prefix': '192.168.0.0/16'},
                            {'le': 32, 'prefix': '172.16.0.0/12'},
                            {'le': 32, 'prefix': '100.64.0.0/10'},
                            {'le': 32, 'prefix': '127.0.0.0/8'},
                            {'le': 32, 'prefix': '169.254.0.0/16'},
                            {'le': 32, 'prefix': '192.0.0.0/24'},
                            {'le': 32, 'prefix': '192.0.2.0/24'},
                            {'le': 32, 'prefix': '198.18.0.0/15'},
                            {'le': 32, 'prefix': '198.51.100.0/24'},
                            {'le': 32, 'prefix': '203.0.113.0/24'},
                            {'le': 32, 'prefix': '224.0.0.0/3'},
                        ],
                    },
                    '4-SMALL-PREFIXES': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [{'ge': 25, 'le': 32, 'prefix': '0.0.0.0/0'}],
                    },
                },
                'ipv6': {
                    '6-65000-PREFIXES': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [{'le': 64, 'prefix': 'fd00:abcd::/48'}],
                    },
                    '6-BIG-PREFIXES': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [{'ge': 1, 'le': 15, 'prefix': '::/0'}],
                    },
                    '6-DEFAULT-ROUTE': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [{'prefix': '::/0'}],
                    },
                    '6-MARTIAN-PREFIXES': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [
                            {'le': 128, 'prefix': '::/8'},
                            {'le': 128, 'prefix': '200::/7'},
                            {'le': 128, 'prefix': '2001::/32'},
                            {'le': 128, 'prefix': '2001:db8::/32'},
                            {'le': 128, 'prefix': '2002::/16'},
                            {'le': 128, 'prefix': '3ffe::/16'},
                            {'le': 128, 'prefix': '5f00::/8'},
                            {'le': 128, 'prefix': 'fc00::/7'},
                            {'le': 128, 'prefix': 'fe80::/10'},
                            {'le': 128, 'prefix': 'fec0::/10'},
                            {'le': 128, 'prefix': 'ff00::/8'},
                        ],
                    },
                    '6-SMALL-PREFIXES': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [{'ge': 49, 'le': 128, 'prefix': '::/0'}],
                    },
                },
            },
            'route_maps': {
                'ipv4': {
                    '4-PEER-IN': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [
                            {
                                'action': 'permit',
                                'match': {'prefix_list': '4-DEFAULT-ROUTE'},
                                'number': 50,
                                'set': {'local_pref': 100},
                            },
                            {
                                'action': 'permit',
                                'match': {'prefix_list': '4-65000-PREFIXES'},
                                'number': 60,
                                'set': {'local_pref': 100},
                            },
                            {'action': 'deny', 'number': 99},
                        ],
                    },
                    '4-PEER-OUT': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [
                            {
                                'action': 'permit',
                                'match': {'prefix_list': '4-65000-PREFIXES'},
                                'number': 50,
                            },
                            {'action': 'deny', 'number': 99},
                        ],
                    },
                    'ALLOW-ALL': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [{'action': 'permit', 'number': 99}],
                    },
                    'REJECT-ALL': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [{'action': 'deny', 'number': 99}],
                    },
                },
                'ipv6': {
                    '6-PEER-IN': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [
                            {
                                'action': 'permit',
                                'match': {'prefix_list': '6-DEFAULT-ROUTE'},
                                'number': 50,
                                'set': {'local_pref': 100},
                            },
                            {
                                'action': 'permit',
                                'match': {'prefix_list': '6-65000-PREFIXES'},
                                'number': 60,
                                'set': {'local_pref': 100},
                            },
                            {'action': 'deny', 'number': 99},
                        ],
                    },
                    '6-PEER-OUT': {
                        'meta': {'netdb': {'datasource': 'repo', 'weight': 50}},
                        'rules': [
                            {
                                'action': 'permit',
                                'match': {'prefix_list': '6-65000-PREFIXES'},
                                'number': 50,
                            },
                            {'action': 'deny', 'number': 99},
                        ],
                    },
                },
            },
        }
    }

    if check_override:
        ret['ROUTER1']['route_maps']['ipv4']['4-PEER-OUT']['rules'] = [
            {
                'action': 'permit',
                'match': {
                    'prefix_list': '4-65000-PREFIXES',
                },
                'number': 50,
            },
            {
                'action': 'permit',
                'match': {
                    'prefix_list': '4-65005-PREFIXES',
                },
                'number': 55,
            },
            {
                'action': 'deny',
                'number': 99,
            },
        ]

        ret['ROUTER1']['route_maps']['ipv4']['4-PEER-OUT']['meta']['netdb'][
            'override'
        ] = True

    return ret
