from typing import Union
from mocked_data import device, interface, bgp, protocol, firewall, policy, override  # type: ignore

from config.settings import NetdbSettings

NetdbSettings.initialize()

COLLECTION_FACTORY = {
    'device': device.mock_standard_device_documents,
    'interface': interface.mock_standard_interface_documents,
    'protocol': protocol.mock_standard_protocol_documents,
    'bgp': bgp.mock_standard_bgp_documents,
    'firewall': firewall.mock_standard_firewall_documents,
    'policy': policy.mock_standard_policy_documents,
    NetdbSettings.get_settings().override_table: override.mock_override_documents,
}


class MongoAPI:

    def __init__(self, database: str, collection: str):
        self.collection = collection
        self.filter: dict = {}
        self.documents: list = []

    def read_column(self, query: Union[dict, None] = None) -> list:
        """
        Mock MongoAPI read_column (NetdbDocument) returns for valid column types.
        """
        documents = COLLECTION_FACTORY[self.collection]()

        if query:
            # Simulate a mongo filtered return by, well, filtering the return.
            return [
                document
                for document in documents
                if all(getattr(document, k) == v for k, v in query.items())
            ]

        return documents

    def read_overrides(self, query: Union[dict, None] = None) -> list:
        """
        Mock MongoAPI read_overrides (OverrideDocument) return. Currently just
        a wrapper around read_column as mocked data already in the correct
        document format.
        """
        return self.read_column(query)

    def reload(self, documents: list, filt: dict) -> bool:
        """
        Mock MongoAPI reload
        """
        self.filter = filt
        self.documents = documents

        return True

    def replace_one(self, document: dict) -> bool:
        """
        Mock MongoAPI replace
        """
        self.documents.append(document)

        return True

    def delete_many(self, filt: dict) -> int:
        """
        Mock MongoAPI delete
        """
        self.filter = filt
        documents = COLLECTION_FACTORY[self.collection]()

        # Simulate a mongo filtered delete by, well, counting number of
        # matching mocked elements.

        return len(
            [
                document
                for document in documents
                if all(getattr(document, k) == v for k, v in filt.items())
            ]
        )

    def create_index(self, index: list) -> bool:
        """
        Mock the creation of indexes.
        """
        return True
