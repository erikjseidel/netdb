from util.mongo_api import MongoAPI
from util.exception import NetDBException
from config.defaults import DB_NAME
from fastapi.encoders import jsonable_encoder
from models.root import COLUMN_TYPES

class ColumnODM:

    _PROVIDE_ALL = False

    _FILT = {}

    def __init__(self, container=None, type=None):

        self.mongo_data = None
        self.column_type = None

        if container:

            self.column_type = container.column_type
            self.flat = container.flat
            self.categories = container.categories
            self.datasource = container.datasource
            self.weight = container.weight
            self.column = jsonable_encoder(container.column, exclude_none=True)

        elif type:
            self.column_type = type

        if not self.column_type or self.column_type not in COLUMN_TYPES:
            raise NetDBException(
                    code=422,
                    message=f'Column {type} not available',
                    )

        self.mongo = MongoAPI(DB_NAME, self.column_type)


    def _to_mongo(self):
        out = []

        datasource = self.datasource
        weight     = self.weight

        for set_id, set_data in self.column.items():
            if self.flat:
                entry = { 
                        'set_id'     : set_id,
                        'datasource' : datasource,
                        'weight'     : weight,
                        'flat'       : True,
                        'data'       : set_data,
                        }
                out.append(entry)

                continue

            for set_element_id, set_element_data in set_data.items():
                if set_element_id in self.categories:
                    for element_id, element_data in set_element_data.items():
                        if element_id in ['ipv4', 'ipv6']:
                            for family_element_id, family_element_data in element_data.items():
                                entry = {
                                        'set_id'     : set_id,
                                        'category'   : set_element_id,
                                        'family'     : element_id,
                                        'element_id' : family_element_id,
                                        'datasource' : datasource,
                                        'weight'     : weight,
                                        'data'       : family_element_data,
                                        }
                                out.append(entry)
                        else:
                            entry = {
                                    'set_id'     : set_id,
                                    'category'   : set_element_id,
                                    'element_id' : element_id,
                                    'datasource' : datasource,
                                    'weight'     : weight,
                                    'data'       : element_data,
                                    }
                            out.append(entry)
                else:
                    entry = {
                            'set_id'     : set_id,
                            'element_id' : set_element_id,
                            'datasource' : datasource,
                            'weight'     : weight,
                            'data'       : set_element_data,
                            }
                    out.append(entry)

        self.mongo_data = out


    def _from_mongo(self):
        out = {}

        for element in self.mongo_data:
            if element['weight'] < 1 and not _PROVIDE_ALL:
                continue

            flat = element.pop('flat', False)

            if flat:
                element_id = element.pop('set_id')
            else:
                element_id = element.pop('element_id')

            element_data = element.pop('data')

            if not element_data.get('meta'):
                element_data['meta'] = {}

            element_data['meta']['netdb'] = {
                    'datasource' : element['datasource'],
                    'weight'     : element['weight'],
                    }

            unwind = out

            if not flat:
                for i in ['set_id', 'category', 'family']:
                    if name := element.get(i):
                        if not unwind.get(name):
                            unwind[name] = {}
                        unwind = unwind[name]

            if element_id in unwind:
                if unwind[element_id]['meta']['netdb'].get('weight', 0) > element.get('weight', 0):
                    continue

            unwind[element_id] = element_data

        self.column = out


    def _is_registered(self):
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


    def _replace(self):
        count = 0

        for document in self.mongo_data:
            if self.mongo.replace_one(document):
                count += 1

        return count


    def reload(self):
        self._FILT = { 'datasource': self.datasource }

        if self.column_type != 'device':
            self._is_registered()

        self._to_mongo()
        if self.mongo.reload(self.mongo_data, self._FILT):
            return self.column

        return None


    def delete(self, filt):
        # We don't want to try a delete with an empty filter.
        if not isinstance(filt, dict):
            raise NetDBException(
                    code=422,
                    message='Invalid filter.',
                    )

        return self.mongo.delete_many(self._FILT)


    def replace(self):
        if self.column_type != 'device':
            self._is_registered()

        self._to_mongo()
        return self._replace()


    def validate(self):
        if self.column_type != 'device':
            self._is_registered()

        return True


    def load_mongo(self, filt=None):
        if filt:
            self._FILT = filt

        self.mongo_data = self.mongo.read(self._FILT)

        return self


    def fetch(self, show_hidden=False):
        self._PROVIDE_ALL = show_hidden
        self._from_mongo()

        return self.column
