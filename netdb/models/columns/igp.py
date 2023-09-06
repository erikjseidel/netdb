from typing import Literal, Dict, Optional, List
from pydantic import Field
from ..base import BaseContainer, BaseColumnModel


class ISISInterface(BaseColumnModel):
    name: str
    passive: bool = False


class ISISRedistributeMap(BaseColumnModel):
    connected_map: Optional[str] = None
    static_map: Optional[str] = None


class ISISRedistributeLevel(BaseColumnModel):
    level_1: Optional[ISISRedistributeMap] = None
    level_2: Optional[ISISRedistributeMap] = None


class ISISRedistributePolicy(BaseColumnModel):
    ipv4: Optional[ISISRedistributeLevel] = None
    ipv6: Optional[ISISRedistributeLevel] = None


class ISIS(BaseColumnModel):
    level: int = Field(None, ge=1, le=3)
    lsp_mtu: int = Field(1471, ge=1200, le=9200)
    iso: str
    interfaces: List[ISISInterface]
    redistribute: Optional[ISISRedistributePolicy] = None
    meta: Optional[dict]


class IGPRoot(BaseColumnModel):
    isis: ISIS


class IGPContainer(BaseContainer):
    column_type: Literal['igp']
    column: Dict[str, IGPRoot]
