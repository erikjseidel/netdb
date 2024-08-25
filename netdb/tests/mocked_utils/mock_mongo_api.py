from typing import Union
from mocked_data import device, interface, bgp, protocol, firewall, policy


class MongoAPI:

    def __init__(self, database: str, collection: str):
        self.column_type = collection
        self.filter = None
        self.documents = []

    def read(self, query: Union[dict, None] = None) -> list:
        """
        Mock MongoAPI read returns for valid column types.
        """
        match self.column_type:
            case 'device':
                documents = device.mock_standard_device_documents()
            case 'interface':
                documents = interface.mock_standard_interface_documents()
            case 'protocol':
                documents = protocol.mock_standard_protocol_documents()
            case 'bgp':
                documents = bgp.mock_standard_bgp_documents()
            case 'firewall':
                documents = firewall.mock_standard_firewall_documents()
            case 'policy':
                documents = policy.mock_standard_policy_documents()

        if query:
            # Simulate a mongo filtered return by, well, filtering the return.
            return [
                document
                for document in documents
                if all(getattr(document, k) == v for k, v in query.items())
            ]

        return documents

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

        return 0

    def create_index(self, index: list) -> bool:
        """
        Mock the creation of indexes.
        """
        return True
