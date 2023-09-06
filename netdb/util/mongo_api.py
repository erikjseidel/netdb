from pymongo import MongoClient, ReadPreference, errors
from pymongo.errors import *
from config.defaults import TRANSACTIONS, MONGO_URL
from util.exception import NetDBException


class MongoAPI:
    def __init__(self, database, collection):
        if TRANSACTIONS:
            # Transactions implies a replica set. Read from first available (which should just be local instance)
            self.client = MongoClient(MONGO_URL, read_preference=ReadPreference.NEAREST)
        else:
            self.client = MongoClient(MONGO_URL)

        database = database
        collection = collection
        cursor = self.client[database]
        self.collection = cursor[collection]

    def read(self, query={}):
        documents = self.collection.find(query)

        return [
            {item: data[item] for item in data if item != '_id'} for data in documents
        ]

    def reload(self, documents, filt):
        if TRANSACTIONS:
            with self.client.start_session() as session:
                with session.start_transaction():
                    self.collection.delete_many(filt, session=session)
                    self.collection.insert_many(
                        documents, ordered=False, session=session
                    )
        else:
            self.collection.delete_many(filt)
            self.collection.insert_many(documents, ordered=False)

        return True

    def write_one(self, document):
        return str(self.collection.insert_one(document).inserted_id)

    def replace_one(self, document):
        filt = {
            'set_id': document.get('set_id'),
            'category': document.get('category'),
            'family': document.get('family'),
            'element_id': document.get('element_id'),
            'datasource': document['datasource'],
        }

        return bool(self.collection.replace_one(filt, document).modified_count)

    def delete_many(self, filt):
        return self.collection.delete_many(filt).deleted_count

    def create_index(self, index):
        self.collection.create_index(index, unique=True)

        return True
