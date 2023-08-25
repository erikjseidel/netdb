from marshmallow import ValidationError
from util.mongo_api import mongoAPI
from util.decorators import netdb_provider, netdb_internal
from config.defaults import DB_NAME

import schema.schema as schema

class netdbColumn:
    DB_NAME = DB_NAME

    FLAT = False
    ELEMENTS_ONLY = False
    CATEGORIES = []

    _FILT = {}
    _PROJ = {}

    def __init__(self, data = {}):
        self.data = data
        self.mongo = mongoAPI(netdbColumn.DB_NAME, self.COLUMN)


    def _get_type(category):
        for d_type, categories in self.COLUMN_CAT.items():
            if category in categories:
                return d_type

        return None


    def _to_mongo(self, data):
        out = []

        datasource = data.pop('datasource')
        weight     = data.pop('weight')

        for set_id, set_data in data.items():
            if self.FLAT:
                entry = { 
                        'set_id'     : set_id,
                        'datasource' : datasource,
                        'weight'     : weight,
                        'data'       : set_data,
                        }
                out.append(entry)

                continue

            for set_element_id, set_element_data in set_data.items():
                if set_element_id in self.CATEGORIES:
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

        return out


    def _from_mongo(self, data):
        out = {}

        for element in data:
            if self.FLAT:
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

            if not self.FLAT:
                for i in ['set_id', 'category', 'family']:
                    if name := element.get(i):
                        if not unwind.get(name):
                            unwind[name] = {}
                        unwind = unwind[name]

            if element_id in unwind:
                if unwind[element_id]['meta']['netdb'].get('weight', 0) > element.get('weight', 0):
                    continue

            unwind[element_id] = element_data

        return out


    @netdb_internal
    def _is_registered(self):
        result, out, comment  = mongoAPI(netdbColumn.DB_NAME, 'device').read()
        devices = []
        for device in out:
            devices.append(device.pop('set_id'))

        set_ids = self.data.keys()

        for set_id in set_ids:
            if set_id not in ['datasource', 'weight'] and set_id not in devices:
                return False, None, f'{set_id}: device not registered.'

        return True, None, 'All devices registered.'


    @netdb_internal
    def _save_checker(self):
        data = self.data

        if not ( data or isinstance(data, dict) ):
            return False, None, 'Invalid dataset.'

        if not data.get('datasource') or not isinstance(data['datasource'], str):
            return False, None, 'A valid datasource string is required.'

        if not data.get('weight') or not isinstance(data['weight'], int):
            return False, None, 'A valid weight integer is required.'

        for set_id, set_elements in data.items():
            if set_id in ['datasource', 'weight']:
                continue

            if self.ELEMENTS_ONLY:
                for element, contents in set_elements.items():
                    try:
                        schema.newSchema(self.COLUMN).load(contents)
                    except ValidationError as error:
                        return False, error.messages, f'{set_id}: {element} contains invalid data.'
            else:
                try:
                    schema.newSchema(self.COLUMN).load(set_elements)
                except ValidationError as error:
                    return False, error.messages, f'{set_id}: Invalid data.'

        return True, None, 'netdb says: Dry run. All checks passed.'


    @netdb_internal
    def _update(self, documents):
        count = 0

        for document in documents:
            filt = { 'set_id': document['set_id'] }

            if 'datasource' in document:
                filt.update({ 'datasource' : document['datasource'] })

            result, out, comment = self.mongo.update_one(filt, document)
            if result: count += 1

        if count > 0:
            doc_word = "document" if count == 1 else "documents"
            return True, None, f'{count} {doc_word} updated.'

        return False, None, 'No documents updated.'


    def set(self, data):
        self.data = data
        return self


    def get(self):
        return self.data


    def filter(self, filt):
        if not filt:
            self._FILT = {}

        elif isinstance(filt, dict):
            self._FILT = filt

        else:
            self._FILT = { 'set_id': filt }

        return self


    def project(self, project_dict):
        if 'projection' in project_dict:
            self._PROJ = project_dict['projection']

            # These should always be returned.
            self._PROJ.update({
                "set_id"     : 1,
                "datasource" : 1,
                })

        if 'filter' in project_dict:
            self._FILT = project_dict['filter']

        return self


    @netdb_provider
    def save(self):
        if self.COLUMN != 'device':
            result, out, comment = self._is_registered()
            if not result: 
                return result, out, comment

        result, out, comment = self._save_checker()
        if not result: 
            return result, out, comment

        result, out, comment = self.mongo.write_many(self._to_mongo(self.data))
        return result, out, comment


    @netdb_provider
    def reload(self):
        # We don't want to try a delete with an empty filter.
        if not self._FILT or 'datasource' not in self._FILT:
            return False, None, 'filter not set'

        if self.COLUMN != 'device':
            result, out, comment = self._is_registered()
            if not result: 
                return result, out, comment

        result, out, comment = self._save_checker()
        if not result: 
            return result, out, comment

        result, out, comment = self.mongo.reload(self._to_mongo(self.data), self._FILT)
        return result, out, comment


    @netdb_provider
    def delete(self):
        # We don't want to try a delete with an empty filter.
        if not self._FILT:
            return False, None, 'filter not set'

        result, out, comment = self.mongo.delete_many(self._FILT)
        return result, out, comment


    @netdb_provider
    def update(self):
        if self.COLUMN != 'device':
            result, out, comment = self._is_registered()
            if not result: 
                return result, out, comment

        result, out, comment = self._save_checker()
        if not result: 
            return result, out, comment

        result, out, comment = self._update(self._to_mongo(self.data))

        return result, out, comment


    @netdb_provider
    def validate(self):
        if self.COLUMN != 'device':
            result, out, comment = self._is_registered()
            if not result: 
                return result, out, comment

        return self._save_checker()


    @netdb_provider
    def fetch(self):
        result, out, comment = self.mongo.read(self._FILT, self._PROJ)

        if not result:
            self.data = {}
            return False, out, comment

        self.data = self._from_mongo(out)

        return True, self.data, 'Data set loaded.'
