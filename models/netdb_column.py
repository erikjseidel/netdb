

class netdbColumn:

    DB_NAME = 'netdb'



    def to_mongo(self):
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


    def from_mongo(self, data):
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


    def set(self, data):
        self.data = data
        return self


    def get(self):
        return self.data


    def save(self):
        ret = self._save_checker()

        if not ret['result']:
            return ret

        return self.mongo.write_many(self.to_mongo())


    def load(self, filt = {}):
        ret = self.mongo.read(filt)

        if not ret['out']:
            self.data = {}
            return { 'result': False, 'comment': 'empty data set' }

        self.from_mongo(ret['out'])
        return { 'result': True, 'comment': 'data set loaded' }


    def fetch(self, filt = {}):
        self.load(filt)

        return { 'result': True, 'out': self.data }
