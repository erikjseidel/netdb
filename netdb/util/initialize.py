from config.defaults import DB_NAME
from .mongo_api import MongoAPI

DEFAULT_INDEX = [
    ('set_id', 1),
    ('category', 1),
    ('family', 1),
    ('element_id', 1),
    ('datasource', 1),
]

INDEXES = {
    'device': DEFAULT_INDEX,
    'interface': DEFAULT_INDEX,
    'firewall': DEFAULT_INDEX,
    'policy': DEFAULT_INDEX,
    'igp': DEFAULT_INDEX,
    'bgp': DEFAULT_INDEX,
}

def initialize():
    for column, index in INDEXES.items():
        MongoAPI(DB_NAME, column).create_index(index)

        # Needs proper logging.
