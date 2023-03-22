

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
