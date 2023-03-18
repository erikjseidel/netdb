
from util.mongo_api import MongoAPI

DATABASE_NAME = 'netdb'

# List of valid columns. Columns have 1:1 alignment with MongoDB collections
NETDB_COLUMNS = [
        'device',
        'interface',
        ]

class NetDB:

    def __init__(self, column):
        if column not in NETDB_COLUMNS:
            raise Exception('Internal error: Invalid column type')

        self.column = column

        self.mongo = MongoAPI( DATABASE_NAME, column )


    def _save(self, data):
        return self.mongo.write(data)


    def _fetch(self, query = {} ):

        ret = self.mongo.read(query)

        if not ret['out']:
            return { 'result': False, 'comment': 'empty data set' }

        return ret


    def _delete(self):
        if 'id' not in self.data:
            return { 'result': False, 'comment': 'id required for delete' }

        key = self.data['id']
        query = { 'id': key.upper() if key != None else None }

        return self.mongo.delete(query)


    def _update(self):
        if 'id' not in self.data:
            return { 'result': False, 'comment': 'id required for delete' }

        #
        #  Update deletes the old entry and replaces it. 
        #
        check = self.mongo.delete({ 'id': self.data['id'] })
        if not check['result']:
            return check

        return self.mongo.write(self.data)


    def _common_save_checker(self, data):
        if 'id' not in data:
            return { 'result': False, 'comment': 'id key is required' }

        return { 'result': True, 'comment': 'checks passed' }


    def _device_save_checker(self, data):
        if data['id'].startswith('_'):
            return { 'result': False, 'comment': 'device id cannot start with `_`' }

        data['id'] = data['id'].upper()

        collection = self._fetch()

        if 'out' not in collection:
            return { 'result': True, 'comment': 'first entry for new collection' }

        for element in collection['out']:
            if element['id'] == data['id']:
                return { 'result': False, 'comment': 'id must be unique' }

        return { 'result': True, 'comment': 'device checks passed' }


    def _interface_save_checker(self, data):
        if 'id' not in data:
            return { 'result': False, 'comment': 'id key is required' }

        if 'interface_id' not in data:
            return { 'result': False, 'comment': 'interface id key is required' }

        device_id = data['id'].upper()

        interfaces = self._fetch( { 'id': device_id } )

        ret = self._registration_check(data, device_id)
        if not ret['result']:
             return ret

        if 'out' not in interfaces:
            return { 'result': True, 'comment': 'first interface entry for this router' }

        # interface_id is simply the name of the interface. it must be unique.
        for element in interfaces['out']:
            if element['interface_id'] == data['interface_id']:
                return { 'result': False, 'comment': 'interface id must be unique' }

        return { 'result': True, 'comment': 'checks passed' }

    
    def _registration_check(self, data, device_id):

        devices = MongoAPI( DATABASE_NAME, 'device' ).read({ 'id': device_id })

        for element in devices['out']:
            if element['id'] == data['id']:
                return { 'result': True, 'comment': 'device is registered' }

        return { 'result': False, 'comment': 'device not registered' }


    def save(self, data):

        if self.column == 'device':
            items = data
            added = 0
            if not isinstance(data, list):
                items = [ data ]

            out = {}

            for index, item in enumerate(items):
                out[index] = {} 

                check = self._common_save_checker(item)
                out[index]['common checks'] = check
                if not check['result']:
                    continue

                check = self._device_save_checker(item)
                out[index]['device checks'] = check
                if not check['result']:
                    continue

                ret = self._save(item)
                out[index].append(ret)
                if not ret['result']:
                    ret.update({ 'index': index })
                    return ret

                added += 1

            comment = str(added) + ' of ' + str(len(items)) + ' items added'
            ret = { 'result': True, 'out': out, 'comment': comment }

        elif self.column == 'interface':
            items = data
            added = 0
            if not isinstance(data, list):
                items = [ data ]

            out = {}
               
            for index, item in enumerate(items):
                out[index] = {} 

                check = self._common_save_checker(item)
                out[index]['common checks'] = check
                if not check['result']:
                    continue

                check = self._interface_save_checker(item)
                out[index]['interface checks'] = check
                if not check['result']:
                    continue

                ret = self._save(item)
                out[index]['save'] = ret
                if not ret['result']:
                    ret.update({ 'index': index })
                    return ret

                added += 1

            comment = str(added) + ' of ' + str(len(items)) + ' items added'
            ret = { 'result': True, 'out': out, 'comment': comment }

        else:
            ret = { 'result': False, 'comment': 'column method not yet implemented.' }

        return ret


    def delete(self, data):
        self.data = data    

        if self.column == 'device':
            ret = self._delete()
        else:
            ret = { 'result': False, 'comment': 'column method not yet implemented.' }

        return ret


    def fetch(self, id_key = None):

        query = {}

        if id_key != None:
            query = { "id": id_key.upper() }

        return self._fetch(query)

