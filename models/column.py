from marshmallow import ValidationError
from util.mongo_api import mongoAPI
from util.decorators import netdb_provider, netdb_internal
from config.defaults import DB_NAME

import schema.schema as schema

class netdbColumn:
    DB_NAME = DB_NAME

    _FILT = {}
    _PROJ = {}

    def __init__(self, data = {}):
        self.data = data
        self.mongo = mongoAPI(netdbColumn.DB_NAME, self._COLUMN)


    def _get_type(category):
        for d_type, categories in self.COLUMN_CAT.items():
            if category in categories:
                return d_type

        return None


    def _to_mongo(self, data):
        out = []

        for config_set, categories in data.items():
            if config_set.startswith('_'):
                entry = {
                        'set_id'     : [ config_set ],
                        'roles'      : categories['roles'],
                        }
                out.append(entry)

            for category, contents in categories.items():
                if category in self._COLUMN_CAT['type_1']:
                    for family in ['ipv4', 'ipv6']:
                        if family in contents:
                            for element, elem_data in contents[family].items():
                                entry = {
                                        'set_id'      : [config_set, category, family, element],
                                        }

                                entry.update(elem_data)
                                out.append(entry)

                elif category in self._COLUMN_CAT['type_2']:
                    for element, elem_data in contents.items():
                        entry = {
                                'set_id'      : [config_set, category, element],
                                }

                        entry.update(elem_data)
                        out.append(entry)

                elif category in self._COLUMN_CAT['type_3']:
                    entry = {
                            'set_id'      : [config_set, category],
                            **contents
                            }

                    out.append(entry)

        return out


    def _from_mongo(self, data):
        out = {}

        for element in data:
            set_id  = element.pop('set_id')
            elem_id = set_id.pop()

            unwind = out
            for i in set_id:
                if not unwind.get(i):
                    unwind[i] = {}
                unwind = unwind[i]

            if elem_id in unwind:
                if unwind[elem_id].get('weight', 0) > element.get('weight', 0):
                    continue

            unwind[elem_id] = element

        return out


    @netdb_internal
    def _is_registered(self):
        result, out, comment  = mongoAPI(netdbColumn.DB_NAME, 'device').read()
        devices = []
        for device in out:
            devices.append(device.pop('id'))

        top_ids = self.data.keys()

        for top_id in top_ids:
            if not top_id.startswith('_') and top_id not in devices:
                return False, self.data[top_id], '%s: device not registered' % top_id

        return True, None, 'all devices registered'


    @netdb_internal
    def _save_checker(self):
        if not isinstance(self.data, dict) or not self.data:
            return False, None, 'invalid dataset'

        for top_id, categories in self.data.items():
            if top_id.startswith('_'):
                if 'roles' not in categories.keys():
                    return False, None, '%s: roles required for shared config set' % top_id

            try:
                schema.newSchema(self._COLUMN).load(categories)
            except ValidationError as error:
                return False, error.messages, '%s: invalid data' % top_id

        return True, None, 'netdb says: dry run. all checks passed for all elements.'


    @netdb_internal
    def _update(self, documents):
        count = 0

        for document in documents:
            if 'id' in document:
                filt = { 'id' : document['id'] }

            else:
                filt = { 'set_id': document['set_id'] }

            if 'datasource' in document:
                filt.update({ 'datasource' : document['datasource'] })

            result, out, comment = self.mongo.update_one(filt, document)
            if result: count += 1

        if count > 0:
            doc = "document" if count == 1 else "documents"
            return True, None, '%s %s updated' % (str(count), doc)

        return False, None, 'no documents updated'


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
                "id"         : 1,
                "datasource" : 1,
                })

        if 'filter' in project_dict:
            self._FILT = project_dict['filter']

        return self


    @netdb_provider
    def save(self):
        if self._COLUMN != 'device':
            result, out, comment = self._is_registered()
            if not result: 
                return result, out, comment

        result, out, comment = self._save_checker()
        if not result: 
            return result, out, comment

        result, out, comment = self.mongo.write_many(self._to_mongo(self.data))
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
        if self._COLUMN != 'device':
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
        if self._COLUMN != 'device':
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

        return True, self.data, 'data set loaded'
