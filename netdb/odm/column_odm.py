from typing import List, Union, Optional, Self
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from config.defaults import DB_NAME, OVERRIDE_TABLE
from models.types import (
    RootContainer,
    NetdbDocument,
    OverrideDocument,
    COLUMN_TYPES,
    COLUMN_FACTORY,
)
from util.mongo_api import MongoAPI
from util.exception import NetDBException


class ColumnODM:

    # If set then elements with weight < 1 are presented as well
    __provide_all__ = False

    # NetDB documents placed here pending column generation.
    documents: Optional[List[NetdbDocument]] = None

    # Override documents placed here by fetch() when overrides enabled.
    override_documents: Optional[List[OverrideDocument]] = None

    def __init__(self, container: RootContainer = None, column_type: str = None):
        """
        Initialize the ColumnODM object to MongoDB document mapper. This object converts
        column data (in Pydantic column model format) into MongoDB documents, which are
        then loaded into MongoDB and vice versa.

        container: ``None``
            Pydantic column model data to be converted into document format and loaded
            into MongoDB.

        type: ``None``
            String containing the column type to be queried in cases where we are loading
            documents from MongoDB and converting to Pydantic column format.

        """

        # NetdbDocument documents stored here pending load into MongoDB.

        self.column_type = None

        if container:
            self.container = container
            self.column_type = container.column_type
            self._generate_netdb_documents()

        elif column_type:
            self.column_type = column_type

        if not self.column_type or self.column_type not in COLUMN_TYPES:
            raise NetDBException(
                code=422,
                message=f'Column {self.column_type} not available',
            )

        if self.column_type == OVERRIDE_TABLE:
            raise NetDBException(
                code=422,
                message=f'Column {self.column_type} confict with override table. Please rename.',
            )

        # Initialize the MongoDB driver
        self.mongo = MongoAPI(DB_NAME, self.column_type)

    @property
    def pruned_column(self) -> dict:
        """
        Return a "pruned column", which is simply the column data itself absent the encap-
        sulating container, in dict formart and with empty keys removed.
        """
        return jsonable_encoder(self.container.column, exclude_none=True)

    def _generate_netdb_documents(self) -> None:
        """
        Convert Pydantic serialized column dict formated data into NetdbDocument format
        which can then be loaded into MongoDB.
        """
        out = []

        datasource = self.container.datasource
        weight = self.container.weight

        for set_id, set_data in self.pruned_column.items():
            if self.container.flat:
                #
                # In case of flat columns (where each set identified by set_id is stored
                # in a single document) their is not need for further looping within the
                # set. The entire set will be stored in a document and we then continue
                # to the next set.
                #
                entry = NetdbDocument(
                    set_id=set_id,
                    datasource=datasource,
                    weight=weight,
                    flat=True,
                    data=set_data,
                )
                out.append(entry)

                continue

            for set_element_id, set_element_data in set_data.items():
                if set_element_id in self.container.categories:
                    #
                    # Column types with categories further divide their set data
                    # into a number of categories (e.g. 'neighbors' and 'peer_groups'
                    # within the 'bgp' column), each of which can have a number of
                    # elements each occupying one document.
                    #
                    for element_id, element_data in set_element_data.items():
                        if element_id in ['ipv4', 'ipv6']:
                            #
                            # Finally, categories can optionally be divided into 'ipv4'
                            # and 'ipv6' families, each of which contain the elements,
                            # again, on a one document per element basis.
                            #
                            for (
                                family_element_id,
                                family_element_data,
                            ) in element_data.items():
                                entry = NetdbDocument(
                                    set_id=set_id,
                                    category=set_element_id,
                                    family=element_id,
                                    element_id=family_element_id,
                                    flat=False,
                                    datasource=datasource,
                                    weight=weight,
                                    data=family_element_data,
                                )
                                out.append(entry)
                        else:
                            entry = NetdbDocument(
                                set_id=set_id,
                                category=set_element_id,
                                element_id=element_id,
                                flat=False,
                                datasource=datasource,
                                weight=weight,
                                data=element_data,
                            )
                            out.append(entry)
                else:
                    #
                    # In cases of columns with no categories (e.g. 'interface' column)
                    # the set is simply deviced into elements(e.g. one element for each
                    # interface).
                    #
                    entry = NetdbDocument(
                        set_id=set_id,
                        element_id=set_element_id,
                        datasource=datasource,
                        weight=weight,
                        flat=False,
                        data=set_element_data,
                    )
                    out.append(entry)

        self.documents = out

    def generate_column(self) -> Self:
        """
        Convert MongoDB documents into column formated dict data.
        """
        out = {}

        override_map = None
        if self.override_documents:
            #
            # If overrides are to be included. Then we read overrides for this column and
            # generate a tuple keyed dict for them that can be used for fast lookups.
            #
            override_map = {
                (
                    document.set_id,
                    document.category,
                    document.family,
                    document.element_id,
                ): document.data
                for document in self.override_documents
            }

        for document in self.documents:

            element = document.model_dump()

            if element['weight'] < 1 and not self.__provide_all__:
                #
                # By default elements with weight less than 1 are not returned as such
                # elements are informational only (e.g. current state data 'mined' from
                # the devices themselves as opposed to 'intent' based elements loaded
                # from an SoT) and thus not intended to be loaded onto devices.
                #
                continue

            unwind = out
            element_data = element.pop('data')

            if element.pop('flat', False):
                #
                # In the case of flat sets the entirety of the set will all be in the
                # same document and no nested dictionaries will need to be loaded from
                # other documents. In these cases the set and the element are one and
                # the same.
                #
                element_id = element.pop('set_id')
            else:
                #
                # Otherwise the element will be a nested dict somewhere within the set
                # dict (to be determined below).
                #
                element_id = element.pop('element_id')

                #
                # This is where, in the case of flat==False, we determine where in the
                # column dict to place this particular element's nested dict.
                #
                for level in ['set_id', 'category', 'family']:
                    if name := element.get(level):
                        unwind = unwind.setdefault(name, {})

            element_data.setdefault('meta', {})

            element_data['meta']['netdb'] = {
                'datasource': element['datasource'],
                'weight': element['weight'],
            }

            if unwind.get(element_id):
                #
                # If the element (or set in case of flat columns) is already in the dict
                # (i.e. placed their by a previous iteration of the main loop) then the
                # element (or set in case of flat columns) with the higher weight should
                # win. Columndb at this time will only present the element with the
                # highest weight to its consumer (e.g. saltstack).
                #
                # In order to 'find' elements with lower weights set one would need to
                # filter by datasource. For example, if we are stashing saltstack 'mine'
                # (i.e. device state)  data in netdb with datasource set to 'mine' then
                # we would filter for 'mine' datasource data to get this device state
                # (as represented from the mine) as opposed to SoT intent.
                #
                if unwind[element_id]['meta']['netdb'].get('weight', 0) > element.get(
                    'weight', 0
                ):
                    continue

            if override_map:
                #
                # If overrides includes enabled and overrides exist then merge the override
                # data into the config data.
                #
                override_tuple = (
                    document.set_id,
                    document.category,
                    document.family,
                    document.element_id,
                )

                # Update with override data if any found.
                if override_data := override_map.get(override_tuple):
                    element_data.update(override_data)
                    element_data['meta']['netdb']['override'] = True

            unwind[element_id] = element_data

        try:
            self.container = COLUMN_FACTORY[self.column_type](
                datasource="netdb", column_type=self.column_type, weight=0, column=out
            )
        except ValidationError as e:
            raise NetDBException(
                code=422,
                message=f"Stored documents for {self.column_type} column failed validation.",
                out=e.errors(),
            ) from e

        return self

    def _is_registered(self) -> bool:
        """
        This method enforces one particular constraint, namely that set_ids in all
        columns except for the device column should align with a set (i.e. device)
        within in the device column. That is to say set_ids are expected to be device
        names and the device should already be 'registered' in the device column.

        """
        devices = [device.set_id for device in MongoAPI(DB_NAME, 'device').read()]

        for set_id in self.container.column.keys():
            if set_id not in devices:
                raise NetDBException(
                    code=422,
                    message=f'{set_id}: device not registered.',
                )

        return True

    def fetch(
        self,
        filt: Union[dict, None] = None,
        show_hidden: bool = False,
        enable_overrides: bool = True,
    ) -> Self:
        """
        Pull column ducuments from MongoDB and convert them into a column formatted
        structured dict data and return it to caller.

        filt: ``None``
            Filter the query using a MongoDB compatable dict based filter

        show_hidden: ``False``
            Public wrapper around `self.__provide_all__` (see above for more details)

        enable_overrides: ``False``
            If false do not load overrides

        """
        filt = filt or {}

        self.documents = self.mongo.read(filt)

        self.__provide_all__ = show_hidden

        if enable_overrides:

            override_filt = {
                k: v
                for k, v in filt.items()
                if k in ['set_id', 'category', 'family', 'element_id'] and v
            }
            self.override_documents = MongoAPI(DB_NAME, OVERRIDE_TABLE).read(
                query={'column_type': self.column_type, **override_filt}
            )

        return self

    def reload(self, filt: Optional[dict] = None) -> Optional[dict]:
        """
        Replace entire column or parts of column filtered by datasource with new data.
        Documents should already be loaded into into self.documents by
        self._generate_mongo_documents().

        This method is used by various SoT backends to manage 'their' portions of the
        configuration data column (as identified by 'datasource').

        """
        filt = filt or {}
        filt.update({'datasource': self.container.datasource})

        if self.column_type != 'device':
            self._is_registered()

        self.mongo.reload(self.documents, filt)

        return self

    def delete(self, filt: dict) -> int:
        """
        Delete documents from MongoDB filtered by filter. Documents should already be
        loaded into self.documents by self._generate_mongo_documents().

        """
        if not filt:
            # We don't want to try a delete with an empty filter.
            raise NetDBException(
                code=422,
                message='Invalid filter.',
            )

        return self.mongo.delete_many(filt)

    def replace(self) -> int:
        """
        Upsert existing documents with new ones. Documents should already be loaded
        into self.documents by self._generate_mongo_documents().

        """
        if self.column_type != 'device':
            self._is_registered()

        count = 0
        for document in self.documents:
            if self.mongo.replace_one(document):
                count += 1

        return count

    def set_overrides(self, documents: List[OverrideDocument]) -> Self:
        """
        Set load inputted override documents into self.override so they can be used in column
        generation. Used by OverrideHandler to validate new overrides.

        documents:
            List of override documents

        """
        self.override_documents = documents

        return self

    def validate(self) -> bool:
        """
        Make sure that column data is valid. In case of column validations, we
        assume that column has already been validated by FastAPI and only validate
        that device is registered.

        """
        if self.column_type != 'device':
            self._is_registered()

        return True
