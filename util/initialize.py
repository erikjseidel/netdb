from .mongo_api import mongoAPI
from config.defaults import DB_NAME

DEFAULT_INDEX = [
    ('set_id.0', 1),
    ('set_id.1', 1),
    ('set_id.2', 1),
    ('set_id.3', 1),
    ('datasource', 1),
    ]

INDEXES = {
    'device'     : [('id', 1), ('datasource', 1)],
    'interface'  : DEFAULT_INDEX,
    'firewall'   : DEFAULT_INDEX,
    'policy'     : DEFAULT_INDEX,
    'igp'        : DEFAULT_INDEX,
    'bgp'        : DEFAULT_INDEX,
    }

WARNING = "Incompatible index found. Recommend removing this index manually."

def initialize():
    for column, index in INDEXES.items():
        result, _, comment = mongoAPI('netdb', column).create_index(index)

        # Needs to be replaced with proper logging.
        if result:
            print(f'{column}: created index {comment}')
        else:
            print(f'{column}: {WARNING}')
