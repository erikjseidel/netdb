from typing import Union
from pymongo import MongoClient, ReadPreference
from config.defaults import TRANSACTIONS, MONGO_URL


class MongoAPI:
    """
    A basic MongoDB API which provides the operations needed by netdb.

    """

    def __init__(self, database: str, collection: str):
        """
        Initialize a MongoDB connection.

        database:
            MongoDB database to connect to

        collection:
            MongoDB collection to use

        """
        if TRANSACTIONS:
            # Transactions implies a replica set. Read from first available (which should
            # just be local instance)
            self.client = MongoClient(MONGO_URL, read_preference=ReadPreference.NEAREST)
        else:
            self.client = MongoClient(MONGO_URL)

        cursor = self.client[database]
        self.collection = cursor[collection]

    def read(self, query: Union[dict, None] = None) -> list:
        """
        Read documents from the collection filtered by query.

        query: ``None``
            Filter to use when reading documents from the collection

        """
        query = query or {}

        documents = self.collection.find(query)

        return [
            {item: data[item] for item in data if item != '_id'} for data in documents
        ]

    def reload(self, documents: list, filt: dict) -> bool:
        """
        Delete all documents in a collection matching a filter and then load new documents
        into the collection. This is done as a single transaction provided that transactions
        are enabled (requires a MongoDB replica set).

        This method implements the netdb reload operation whereby a SoT will delete all the
        documents in the collections associated with its intent (identified by datasource)
        and then load documents representing its current intent in their place.

        documents:
            New list of documents to load into the collection

        filt:
            Filter to use when deleting documents from the collection (e.g. `{'datasource':
            'netbox'}`)

        """
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

    def write_one(self, document: dict) -> str:
        """
        Add a single document to a collection

        document
            A dict representing the new document to load into the collection

        """
        return str(self.collection.insert_one(document).inserted_id)

    def replace_one(self, document: dict) -> bool:
        """
        Replace a single document to a collection

        document
            A dict representing the new document to load into the collection in
            place of an existing document

        """
        filt = {
            'set_id': document.get('set_id'),
            'category': document.get('category'),
            'family': document.get('family'),
            'element_id': document.get('element_id'),
            'datasource': document['datasource'],
        }

        return bool(self.collection.replace_one(filt, document).modified_count)

    def delete_many(self, filt: dict) -> int:
        """
        Delete all documents matching a filter from the collection

        filt:
            Filter to use when deleting documents from the collection

        """
        return self.collection.delete_many(filt).deleted_count

    def create_index(self, index: list) -> bool:
        """
        Index a collection using a compound (multi-key) index

        index:
            the set of keys (i.e. compound index) used to index the collection

        """
        self.collection.create_index(index, unique=True)

        return True
