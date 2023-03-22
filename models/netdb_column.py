

class netdbColumn:

    DB_NAME = 'netdb'

    COLUMNS = [
        'device',
        'interface',
        'igp',
        'firewall',
        ]

    ELEMENT_ID = {
        'device'   : 'id',
        'interface': 'interface_id',
        'igp'      : 'set_id',
        'firewall' : 'element_id',
        'policy'   : 'element_id',
        'bgp'      : 'element_id',
        }


    def to_mongo(self):
        out = []

        for config_set, categories in self.data.items():
            if config_set.startswith('_'):
                entry = {
                        'set_id'     : config_set,
                        'category'   : '_roles',
                        'roles'      : categories['roles'],
                        }
                out.append(entry)

            for category, contents in categories.items():
                if category in self._COLUMN_CAT['type_1']:
                    for family in ['ipv4', 'ipv6']:
                        if family in contents:
                            for element, elem_data in contents[family].items():
                                entry = {
                                        'set_id'          : config_set,
                                        'category'        : self._TO_MONGO[category],
                                        'family'          : family,
                                        self._ELEMENT_ID  : element,
                                        }

                                if not config_set.startswith('_'):
                                    entry.update({ 'id' : config_set })

                                entry.update(elem_data)
                                out.append(entry)

                elif category in self._COLUMN_CAT['type_2']:
                    for element, elem_data in contents.items():
                        entry = {
                                'set_id'          : config_set,
                                'category'        : self._TO_MONGO[category],
                                self._ELEMENT_ID  : element,
                                }

                        if not config_set.startswith('_'):
                            entry.update({ 'id' : config_set })

                        entry.update(elem_data)
                        out.append(entry)

                elif category in self._COLUMN_CAT['type_3']:
                    entry = {
                            'set_id'         : config_set,
                            'category'       : self._TO_MONGO[category],
                            self._ELEMENT_ID : "%s.%s" % (config_set, category),
                            }

                    if not config_set.startswith('_'):
                        entry.update({ 'id' : config_set })

                    entry.update(contents)
                    out.append(entry)

        return out


    def from_mongo(self, data):
        out = {}

        for element in data:
            config_set = element.pop('set_id')
            element.pop('id', None)
            if config_set not in out:
                out[config_set] = {}

            category = element.pop('category')
            new_cat  = self._FROM_MONGO[category]

            if category in self._MONGO_CAT['type_1']:
                family = element.pop('family')
                elem   = element.pop('element_id')

                if new_cat not in out[config_set]:
                    out[config_set][new_cat] = {}

                if family not in out[config_set][new_cat]:
                    out[config_set][new_cat][family] = {}

                out[config_set][new_cat][family][elem] = element

            elif category in self._MONGO_CAT['type_2']:
                elem   = element.pop('element_id')

                if new_cat not in out[config_set]:
                    out[config_set][new_cat] = {}

                out[config_set][new_cat][elem] = element

            elif category in self._MONGO_CAT['type_3']:
                element.pop('element_id', None)
                out[config_set][new_cat] = element

            elif category == '_roles':
                out[config_set]['roles'] = element['roles']

            else:
                out = {}

        self.data = out


    def set(self, data):
        self.data = data


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
