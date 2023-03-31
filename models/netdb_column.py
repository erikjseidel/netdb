
from marshmallow        import ValidationError
from util.mongo_api     import MongoAPI
from util.decorators    import salty, netdb_internal

import schema.schema as schema

class netdbColumn:

    DB_NAME = 'netdb'

    _FILT = {}

    def __init__(self, data = {}):
        self.data = data
        self.mongo = MongoAPI(netdbColumn.DB_NAME, self._COLUMN)


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
                        'set_id'     : config_set,
                        'category'   : 'roles',
                        'roles'      : categories['roles'],
                        }
                out.append(entry)

            for category, contents in categories.items():
                if category in self._COLUMN_CAT['type_1']:
                    for family in ['ipv4', 'ipv6']:
                        if family in contents:
                            for element, elem_data in contents[family].items():
                                entry = {
                                        'set_id'      : config_set,
                                        'category'    : category,
                                        'family'      : family,
                                        'element_id'  : element,
                                        }

                                entry.update(elem_data)
                                out.append(entry)

                elif category in self._COLUMN_CAT['type_2']:
                    for element, elem_data in contents.items():
                        entry = {
                                'set_id'      : config_set,
                                'category'    : category,
                                'element_id'  : element,
                                }

                        entry.update(elem_data)
                        out.append(entry)

                elif category in self._COLUMN_CAT['type_3']:
                    entry = {
                            'set_id'      : config_set,
                            'category'    : category,
                            }

                    entry.update(contents)
                    out.append(entry)

        return out


    def _from_mongo(self, data):
        out = {}

        for element in data:
            config_set = element.pop('set_id')
            if config_set not in out:
                out[config_set] = {}

            category = element.pop('category')

            if category in self._COLUMN_CAT['type_1']:
                family = element.pop('family')
                elem   = element.pop('element_id')

                if category not in out[config_set]:
                    out[config_set][category] = {}

                if family not in out[config_set][category]:
                    out[config_set][category][family] = {}

                out[config_set][category][family][elem] = element

            elif category in self._COLUMN_CAT['type_2']:
                elem   = element.pop('element_id')

                if category not in out[config_set]:
                    out[config_set][category] = {}

                out[config_set][category][elem] = element

            elif category in self._COLUMN_CAT['type_3']:
                out[config_set][category] = element

            elif category == 'roles':
                out[config_set]['roles'] = element['roles']

            else:
                out = {}

        return out


    @netdb_internal
    def _is_registered(self):
        result, out, comment  = MongoAPI(netdbColumn.DB_NAME, 'device').read()
        devices = []
        for device in out:
            devices.append(device.pop('id'))

        top_ids = self.data.keys()

        for top_id in top_ids:
            if not top_id.startswith('_') and top_id not in devices:
                return False, None, '%s: device not registered'

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
                for key in ['category', 'family', 'element_id']:
                    if key in document:
                        filt.update({ key : document[key] })
 
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

        elif isinstance(filt, list):
            if len(filt) == 4:

                # the four tuple 'mask' filter. works similar to what one might see
                # in juniper config mode.
                keys = ['set_id', 'category', 'family', 'element_id']

                d = dict(zip(keys, filt))

                self._FILT = {k: v for k, v in d.items() if v }

        elif isinstance(filt, dict):
            self._FILT = filt

        else:
            self._FILT = { 'set_id': filt }

        return self


    @salty
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


    @salty
    def delete(self):
        # We don't want to try a delete with an empty filter.
        if not self._FILT:
            return False, None, 'filter not set'

        result, out, comment = self.mongo.delete_many(self._FILT)
        return result, out, comment


    @salty
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


    @salty
    def validate(self):
        if self._COLUMN != 'device':
            result, out, comment = self._is_registered()
            if not result: 
                return result, out, comment

        return self._save_checker()


    @salty
    def fetch(self):
        result, out, comment = self.mongo.read(self._FILT)

        if not result:
            self.data = {}
            return False, out, comment

        self.data = self._from_mongo(out)

        return True, self.data, 'data set loaded'
