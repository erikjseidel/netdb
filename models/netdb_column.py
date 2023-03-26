
from util.mongo_api     import MongoAPI

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


    def _is_registered(self):
        mongo_answer = MongoAPI(netdbColumn.DB_NAME, 'device').read()['out']
        devices = []
        for device in mongo_answer:
            devices.append(device.pop('id'))

        top_ids = self.data.keys()

        name = None

        registered = True
        for top_id in top_ids:
            if not top_id.startswith('_') and top_id not in devices:
                ret = { 'result': False, 'comment': '%s: device not registered' % top_id }
                registered = False
                break

        if registered:
            ret = { 'result': True, 'comment': 'all devices registered' }

        return ret


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


    def set(self, data):
        self.data = data
        return self


    def get(self):
        return self.data


    def save(self):
        if self._COLUMN != 'device':
            ret = self._is_registered()
            if not ret['result']:
                return ret

        ret = self._save_checker()
        if not ret['result']:
            return ret

        return self.mongo.write_many(self._to_mongo(self.data))


    def delete(self):
        # We don't want to try a delete with an empty filter.
        if not self._FILT:
            return { 'result': False, 'error': True, 'comment': 'filter not set' }
           
        return self.mongo.delete_many(self._FILT)
        

    def update(self):
        ret = self._is_registered()
        if not ret['result']:
            return ret

        ret = self._save_checker()
        if not ret['result']:
            return ret

        return self._update(self._to_mongo(self.data))


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

            if self.mongo.update_one(filt, document)['result']:
                count += 1

        if count > 0:
            return { 'result': True, 'comment': '%s documents updated' % str(count) }

        return { 'result': False, 'comment': 'no documents updated' }


    def load(self):
        ret = self.mongo.read(self._FILT)

        if not ret['out']:
            self.data = {}
            return { 'result': False, 'comment': 'empty data set' }

        self.data = self._from_mongo(ret['out'])
        return { 'result': True, 'comment': 'data set loaded' }


    def fetch(self):
        self.load()

        return { 'result': True, 'out': self.data }
