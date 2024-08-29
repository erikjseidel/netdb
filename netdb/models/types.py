from typing import Annotated, Union, Literal, Optional
from pydantic import BaseModel
from fastapi import Body

from .base_types import FamilyType
from .columns.device import DeviceContainer
from .columns.firewall import FirewallContainer
from .columns.policy import PolicyContainer
from .columns.interface import InterfaceContainer
from .columns.bgp import BGPContainer
from .columns.protocol import ProtocolContainer

COLUMN_FACTORY = {
    'device': DeviceContainer,
    'firewall': FirewallContainer,
    'policy': PolicyContainer,
    'interface': InterfaceContainer,
    'bgp': BGPContainer,
    'protocol': ProtocolContainer,
}

COLUMN_TYPES = list(COLUMN_FACTORY.keys())

COLUMN_CLASSES = list(COLUMN_FACTORY.values())

ColumnType = Annotated[str, Literal[*COLUMN_TYPES]]

RootContainer = Annotated[
    Union[*COLUMN_CLASSES],
    Body(discriminator='column_type'),
]


class BaseDocument(BaseModel):
    """
    Abstract type used to derive NetdbDocument and OverrideDocument
    types

    """

    set_id: str
    category: Optional[str] = None
    family: Optional[FamilyType] = None
    element_id: Optional[str] = None
    data: dict


class NetdbDocument(BaseDocument):
    """
    Structure of on-database document. Intended to be compatable with
    both SQL and document oriented databases (e.g. MongoDB).

    Incoming column data is decomposed into a number of NetdbDocuments
    which can then be stored on the backend database.

    """

    weight: int
    datasource: str
    flat: Optional[bool] = False


class OverrideDocument(BaseDocument):
    """
    Structure of override document. Intended to be compatable with
    both SQL and document oriented databases (e.g. MongoDB).

    Used to store overrides of column records.

    """

    column_type: ColumnType
