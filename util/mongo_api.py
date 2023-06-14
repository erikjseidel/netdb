from pymongo import MongoClient, errors
from pymongo.errors import *

from .decorators import netdb_internal

class mongoAPI:

    def __init__(self, database, collection):
        self.client = MongoClient("mongodb://localhost:27017/")  

        database = database
        collection = collection
        cursor = self.client[database]
        self.collection = cursor[collection]


    @netdb_internal
    def read(self, query = {}, projection = {}):
        documents = self.collection.find(query, projection)

        out = [{item: data[item] for item in data if item != '_id'} for data in documents]

        if len(out) == 0:
            return False, None, 'No documents found'

        return True, out, '%s documents read' % len(out)


    @netdb_internal
    def write_one(self, document):
        response = self.collection.insert_one(document)

        return True, None, str(response.inserted_id) + ' created'


    @netdb_internal
    def write_many(self, documents):
        response = None

        try:
            response = self.collection.insert_many(documents, ordered = False)
        except BulkWriteError:
            return True, None, 'warning: duplicates were found. not all documents added'

        length = len(response.inserted_ids)
        doc = "document" if length == 1 else "documents"

        return True, None, '%s %s created' % (length, doc)


    @netdb_internal
    def update_one(self, filt, document):
        response = self.collection.replace_one(filt, document)

        if response.modified_count > 0:
            return True, None, 'document modified'

        return False, None, 'nothing updated. %s matched' % response.matched_count


    @netdb_internal
    def delete_many(self, filt):
        response = self.collection.delete_many(filt)
        if response.deleted_count == 0:
            return False, None, 'Nothing deleted'

        doc = "document" if response.deleted_count == 1 else "documents"
        return True, None, '%s %s deleted' % (response.deleted_count, doc)


    @netdb_internal
    def create_index(self, index):
        try:
            response = self.collection.create_index(index, unique=True)
        except OperationFailure:
            return False, None, 'incompatible index found'

        return True, None, response
