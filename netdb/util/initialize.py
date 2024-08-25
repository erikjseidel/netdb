import logging

from config.defaults import DB_NAME
from models.root import COLUMN_TYPES
from .mongo_api import MongoAPI

logger = logging.getLogger(__name__)

# Column default index. We're currently using default for all column types
# as mongodb will allow / ignore non-existent keys when indexing.
DEFAULT_INDEX = [
    ('set_id', 1),
    ('category', 1),
    ('family', 1),
    ('element_id', 1),
    ('datasource', 1),
]


def initialize():
    """
    Code to be run at API start time. Currently limited to making sure
    that the required MongoDB collection indexes are in place.

    """
    for column in COLUMN_TYPES:
        logger.info("%s: Creating index for column %s", DB_NAME, column)

        # This call will be a no-op if index already exists.
        MongoAPI(DB_NAME, column).create_index(DEFAULT_INDEX)
