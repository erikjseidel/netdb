

class netdbColumn:

    DB_NAME = 'netdb'

    _FILT = {}

    def _get_type(category):
        for d_type, categories in self.COLUMN_CAT.items():
            if category in categories:
                return d_type

        return None


    def _to_mongo(self):
        out = []

        for config_set, categories in self.data.items():
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

        self.data = out


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
        ret = self._save_checker()

        if not ret['result']:
            return ret

        return self.mongo.write_many(self._to_mongo())


    def delete(self):
        # We don't want to try a delete with an empty filter.
        if not self._FILT:
            return { 'result': False, 'error': True, 'comment': 'filter not set' }
           
        return self.mongo.delete_many(self._FILT)
        

    def update(self):
        # We don't want to try an update with an empty filter.
        if not self._FILT:
            return { 'result': False, 'error': True, 'comment': 'filter not set' }

        if not self._save_checker()['result']:
            return ret

        self.mongo.delete_many(self._FILT)

        return self.mongo.write_many(self._to_mongo())


    def load(self):
        ret = self.mongo.read(self._FILT)

        if not ret['out']:
            self.data = {}
            return { 'result': False, 'comment': 'empty data set' }

        self._from_mongo(ret['out'])
        return { 'result': True, 'comment': 'data set loaded' }


    def fetch(self):
        self.load()

        return { 'result': True, 'out': self.data }
