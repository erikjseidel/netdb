from typing import Optional, Self
from beartype.typing import List
from beartype import beartype
from fastapi.encoders import jsonable_encoder

from config.defaults import DB_NAME, OVERRIDE_TABLE
from util.mongo_api import MongoAPI
from util.exception import NetDBException
from models.types import OverrideDocument

from .column_odm import ColumnODM


@beartype
class OverrideHandler:

    overrides: List[OverrideDocument] = None

    def __init__(self, override: OverrideDocument = None):
        """
        Initialize a new OverrideHandler instance and its database connection.

        """
        self.mongo = MongoAPI(DB_NAME, OVERRIDE_TABLE)

    @property
    def pruned_overrides(self):
        """
        Return a list of "pruned overrides", which is simply the overrides themselves
        in dict formart and with empty keys removed.

        """
        return jsonable_encoder(self.overrides, exclude_none=True)

    def fetch(self, filt: Optional[dict] = None) -> Self:
        """
        Pull override documents from MongoDB and place them into self.overrides.

        filt: ``None``
            Filter the query using a MongoDB compatable dict based filter

        """

        filt = filt or {}

        self.overrides = self.mongo.read(filt)

        return self

    def upsert(self, override: OverrideDocument) -> dict:
        """
        Upsert existing override (if exists) with new ones. If none already
        exist then a new one is created. Before insertion, override is validated to
        ensure that (1) underlying configuration exists and (2) that the overriden
        configuration is valid.

        override:
           An override document to be added.

        """
        filt = {
            'set_id': override.set_id,
            'category': override.category,
            'family': override.family,
            'element_id': override.element_id,
        }

        column = ColumnODM(column_type=override.column_type).fetch(
            filt, enable_overrides=False
        )

        if not column.documents:
            raise NetDBException(
                code=404, message="No matching column data found. Nothing to override."
            )

        #
        # Try to recompose and validate a column from  overriden column data. A
        # validation NetDBException thrown if errors are found.
        #
        column.set_overrides([override]).generate_column()

        if column.overrides_applied != 1:
            #
            # Overrides applied should be exactly one. If zero, then the override
            # doesn't actually match a discrete document / column element and thus
            # could not be applied.
            #
            raise NetDBException(
                code=422,
                message="Invalid override. Does not match a discrete column element.",
                out=override,
            )

        # Validation passed. Store the override.
        self.mongo.replace_one(override)

        # Return the overridden column data to caller.
        return column.pruned_column

    def delete(self, filt: dict) -> int:
        """
        Delete documents from MongoDB filtered by filter. Documents should already be
        loaded into self.documents by self._generate_mongo_documents().

        """
        return self.mongo.delete_many(filt)
