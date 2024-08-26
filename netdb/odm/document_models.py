from typing import Literal, Optional
from pydantic import BaseModel


class NetdbDocument(BaseModel):
    """
    Structure of on-database document. Intended to be compatable with
    both SQL and document oriented databases (e.g. MongoDB).

    Incoming column data is decomposed into a number of NetdbDocuments
    which can then be stored on the backend database.

    """

    set_id: str
    datasource: str
    weight: int
    flat: Optional[bool] = False
    category: Optional[str] = None
    family: Optional[Literal['ipv4', 'ipv6']] = None
    element_id: Optional[str] = None
    data: dict
