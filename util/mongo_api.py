from pymongo import MongoClient, errors
from pymongo.errors import *

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


    def write_one(self, document):
        response = self.collection.insert_one(document)

        return { 'result': True, 'comment': str(response.inserted_id) + ' created' }


    def write_many(self, documents):
        response = None

        try:
            response = self.collection.insert_many(documents, ordered = False)
        except BulkWriteError:
            return { 'result': True, 'comment':  'warning: duplicates were found. not all documents added' }

        return { 'result': True, 'comment': str(len(response.inserted_ids)) + ' documents created' }


    def update_one(self, filt, document):
        response = self.collection.update_one(filt, { "$set": document }, upsert = True)

        if response.modified_count > 0:
            return { 'result': True, 'comment': str(response.modified_count) + ' updated' }

        return { 'result': False, 'comment': 'nothing updated. %s matched' % response.matched_count }


    def delete_many(self, filt):
        response = self.collection.delete_many(filt)
        if response.deleted_count > 0:
            ret = { 'result': True, 'comment': '%s records deleted' % response.deleted_count }
        else:
            ret = { 'result': False, 'comment': 'Nothing deleted' }

        return ret
