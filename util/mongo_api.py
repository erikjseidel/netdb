from pymongo import MongoClient

class MongoAPI:

    def __init__(self, database, collection):
        self.client = MongoClient("mongodb://localhost:27017/")  

        database = database
        collection = collection
        cursor = self.client[database]
        self.collection = cursor[collection]


    def read(self, query = {}):
        documents = self.collection.find(query)
        out = [{item: data[item] for item in data if item != '_id'} for data in documents]

        return {'result': True, 'out': out }


    def write(self, document):
        response = self.collection.insert_one(document)

        return { 'result': True, 'comment': str(response.inserted_id) + ' created' }


    def write_many(self, documents):
        response = self.collection.insert_many(documents)

        return { 'result': True, 'comment': str(len(response.inserted_ids)) + ' documents created' }


    def delete_many(self, filt):
        response = self.collection.delete_many(filt)
        if response.deleted_count > 0:
            ret = { 'result': True, 'comment': '%s records deleted' % response.deleted_count }
        else:
            ret = { 'result': False, 'comment': 'Nothing deleted' }

        return ret
