from typing import Union, Self
from fastapi.encoders import jsonable_encoder
from config.defaults import DB_NAME
from models.root import RootContainer, COLUMN_TYPES
from util.mongo_api import MongoAPI
from util.exception import NetDBException


class ColumnODM:

    # If set then elements with weight < 1 are presented as well
    __provide_all__ = False

    # In mongodb filter dict format. Used to filter mongodb queries.
    __filter__ = {}

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

        # MongoDB documents stored here pending load into MongoDB.
        self.mongo_data = None

        self.column_type = None

        if container:
            self.column_type = container.column_type
            self.flat = container.flat
            self.categories = container.categories
            self.datasource = container.datasource
            self.weight = container.weight
            self.column = jsonable_encoder(container.column, exclude_none=True)

        elif column_type:
            self.column_type = column_type

        if not self.column_type or self.column_type not in COLUMN_TYPES:
            raise NetDBException(
                code=422,
                message=f'Column {self.column_type} not available',
            )

        # Initialize the MongoDB driver
        self.mongo = MongoAPI(DB_NAME, self.column_type)

    def _to_mongo(self) -> None:
        """
        Convert Pydantic serialized column dict formated data into MongoDB document format
        which can then be loaded into MongoDB.
        """
        out = []

        datasource = self.datasource
        weight = self.weight

        for set_id, set_data in self.column.items():
            if self.flat:
                #
                # In case of flat columns (where each set identified by set_id is stored
                # in a single document) their is not need for further looping within the
                # set. The entire set will be stored in a document and we then continue
                # to the next set.
                #
                entry = {
                    'set_id': set_id,
                    'datasource': datasource,
                    'weight': weight,
                    'flat': True,
                    'data': set_data,
                }
                out.append(entry)

                continue

            for set_element_id, set_element_data in set_data.items():
                if set_element_id in self.categories:
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
                                entry = {
                                    'set_id': set_id,
                                    'category': set_element_id,
                                    'family': element_id,
                                    'element_id': family_element_id,
                                    'datasource': datasource,
                                    'weight': weight,
                                    'data': family_element_data,
                                }
                                out.append(entry)
                        else:
                            entry = {
                                'set_id': set_id,
                                'category': set_element_id,
                                'element_id': element_id,
                                'datasource': datasource,
                                'weight': weight,
                                'data': element_data,
                            }
                            out.append(entry)
                else:
                    #
                    # In cases of columns with no categories (e.g. 'interface' column)
                    # the set is simply deviced into elements(e.g. one element for each
                    # interface).
                    #
                    entry = {
                        'set_id': set_id,
                        'element_id': set_element_id,
                        'datasource': datasource,
                        'weight': weight,
                        'data': set_element_data,
                    }
                    out.append(entry)

        self.mongo_data = out

    def _from_mongo(self) -> None:
        """
        Convert MongoDB documents into column formated dict data.
        """
        out = {}

        for element in self.mongo_data:

            if element['weight'] < 1 and not self.__provide_all__:
                #
                # By default elements with weight less than 1 are not returned as such
                # elements are informational only (e.g. current state data 'mined' from
                # the devices themselves as opposed to 'intent' based elements loaded
                # from an SoT) and thus not intended to be loaded onto devices.
                #
                continue

            if flat := element.pop('flat', False):
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

            element_data = element.pop('data')

            if not element_data.get('meta'):
                element_data['meta'] = {}

            element_data['meta']['netdb'] = {
                'datasource': element['datasource'],
                'weight': element['weight'],
            }

            unwind = out
            if not flat:
                #
                # This is where, in the case of flat==False, we determine where in the
                # set dict to place this particular element's nested dict.
                #
                for i in ['set_id', 'category', 'family']:
                    if name := element.get(i):
                        if not unwind.get(name):
                            unwind[name] = {}
                        unwind = unwind[name]

            if element_id in unwind:
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

            unwind[element_id] = element_data

        self.column = out

    def _is_registered(self) -> bool:
        """
        This method enforces one particular constraint, namely that set_ids in all
        columns except for the device column should align with a set (i.e. device)
        within in the device column. That is to say set_ids are expected to be device
        names and the device should already be 'registered' in the device column.

        """
        out = MongoAPI(DB_NAME, 'device').read()
        devices = []

        for device in out:
            devices.append(device.pop('set_id'))

        for set_id in self.column.keys():
            if set_id not in devices:
                raise NetDBException(
                    code=422,
                    message=f'{set_id}: device not registered.',
                )

        return True

    def _replace(self) -> int:
        """
        Upsert existing documents with new ones. Documents should already be loaded
        into self.mongo_data by self._to_mongo().

        """
        count = 0

        for document in self.mongo_data:
            if self.mongo.replace_one(document):
                count += 1

        return count

    def reload(self) -> Union[dict, None]:
        """
        Replace entire column or parts of column filtered by datasource with new data.
        Documents should already be loaded into into self.mongo_data by
        self._to_mongo().

        This method is used by various SoT backends to manage 'their' portions of the
        configuration data column (as identified by 'datasource').

        """
        self.__filter__ = {'datasource': self.datasource}

        if self.column_type != 'device':
            self._is_registered()

        self._to_mongo()
        if self.mongo.reload(self.mongo_data, self.__filter__):
            return self.column

        return None

    def delete(self, filt: dict) -> int:
        """
        Delete documents from MongoDB filtered by filter. Documents should already be
        loaded into self.mongo_data by self._to_mongo().

        """
        if not filt:
            # We don't want to try a delete with an empty filter.
            raise NetDBException(
                code=422,
                message='Invalid filter.',
            )

        return self.mongo.delete_many(self.__filter__)

    def replace(self) -> int:
        """
        Wrapper around self._replace(). Calls self._registered() first to verify that
        the set_id in question is associated with a device set in the device column.

        """
        if self.column_type != 'device':
            self._is_registered()

        self._to_mongo()
        return self._replace()

    def validate(self) -> bool:
        """
        Make sure that column data is valid. Thanks to FastAPI and its Pydantic based
        validators, the only remaining thing to validate here is that set_ids in non-
        device columns are the same name as a set_id in the device column.

        """
        if self.column_type != 'device':
            self._is_registered()

        return True

    def load_mongo(self, filt: Union[dict, None] = None) -> Self:
        """
        Pull column data for a column from MongoDB and store it in self.mongo_data

        filt: ``None``
            Filter the query using a MongoDB compatable dict based filter

        """
        if filt:
            self.__filter__ = filt

        self.mongo_data = self.mongo.read(self.__filter__)

        return self

    def fetch(self, show_hidden: bool = False) -> dict:
        """
        Convert MongoDB documents stored in self.mongo_data into column formatted
        structured dict data and return it to caller.

        show_hidden: ``False``
            Public wrapper around `self.__provide_all__` (see above for more details)

        """
        self.__provide_all__ = show_hidden
        self._from_mongo()

        return self.column
