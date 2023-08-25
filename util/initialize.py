from .mongo_api import mongoAPI
from config.defaults import DB_NAME

DEFAULT_INDEX = [
    ('set_id', 1),
    ('category', 1),
    ('family', 1),
    ('element_id', 1),
    ('datasource', 1),
    ]

INDEXES = {
    'device'     : DEFAULT_INDEX,
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
