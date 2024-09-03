import logging

from config.settings import NetdbSettings
from models.types import COLUMN_TYPES
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

# Index used for overrides in override table
OVERRIDE_INDEX = [
    ('column_type', 1),
    ('set_id', 1),
    ('category', 1),
    ('family', 1),
    ('element_id', 1),
]


def initialize():
    """
    Code to be run at API start time. Currently limited to making sure
    that the required MongoDB collection indexes are in place.

    """

    # Load NetdbSettings
    NetdbSettings.initialize()

    # Get the loaded NetDB settings
    settings = NetdbSettings.get_settings()

    if not settings.read_only:
        for column in COLUMN_TYPES:
            logger.info("%s: Creating index for column %s", settings.db_name, column)

            # This call will be a no-op if index already exists.
            MongoAPI(settings.db_name, column).create_index(DEFAULT_INDEX)

    if settings.overrides_enabled:
        logger.info(
            "%s: Creating index for override table %s",
            settings.db_name,
            settings.override_table,
        )
        MongoAPI(settings.db_name, settings.override_table).create_index(OVERRIDE_INDEX)
