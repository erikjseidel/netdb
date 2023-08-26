from pymongo import MongoClient, ReadPreference, errors
from pymongo.errors import *
from config.defaults import TRANSACTIONS

from .decorators import netdb_internal

class mongoAPI:

    def __init__(self, database, collection):
        if TRANSACTIONS:
            # Transactions implies a replica set. Read from first available (which should just be local instance)
            self.client = MongoClient("mongodb://localhost:27017/", read_preference=ReadPreference.NEAREST)  
        else:
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
    def reload(self, documents, filt):
        if TRANSACTIONS:
            with self.client.start_session() as session:
                with session.start_transaction():
                    self.collection.delete_many(filt, session=session)
                    self.collection.insert_many(documents, ordered = False, session=session)
        else:
            self.collection.delete_many(filt)
            self.collection.insert_many(documents, ordered = False)

        return True, None, 'Reload complete'


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
    def update_one(self, document):
        filt = {
                'set_id'     : document.get('set_id'),
                'category'   : document.get('category'),
                'family'     : document.get('family'),
                'element_id' : document.get('element_id'),
                'datasource' : document['datasource'],
                }

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
