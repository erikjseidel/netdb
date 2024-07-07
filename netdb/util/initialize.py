from config.defaults import DB_NAME
from .mongo_api import MongoAPI

# The default compound index type.
DEFAULT_INDEX = [
    ('set_id', 1),
    ('category', 1),
    ('family', 1),
    ('element_id', 1),
    ('datasource', 1),
]

# Column indexes. We're currently using default for all column types
# as mongodb will allow / ignore non-existent keys when indexing.
INDEXES = {
    'device': DEFAULT_INDEX,
    'interface': DEFAULT_INDEX,
    'firewall': DEFAULT_INDEX,
    'policy': DEFAULT_INDEX,
    'igp': DEFAULT_INDEX,
    'bgp': DEFAULT_INDEX,
}


def initialize():
    """
    Code to be run at API start time. Currently limited to making sure
    that the required MongoDB collection indexes are in place.

    """
    for column, index in INDEXES.items():
        # This call will be a no-op if index already exists.
        MongoAPI(DB_NAME, column).create_index(index)

        # Needs proper logging.
