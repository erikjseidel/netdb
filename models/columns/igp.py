from ..base import BaseContainer, BaseColumnModel
from typing import Literal, Dict, Union, List
from pydantic import Field

class ISISInterface(BaseColumnModel):
    name: str
    passive: bool = False


class ISISRedistributeMap(BaseColumnModel):
    connected_map: Union[str, None] = None
    static_map: Union[str, None] = None


class ISISRedistributeLevel(BaseColumnModel):
    level_1: Union[ISISRedistributeMap, None] = None
    level_2: Union[ISISRedistributeMap, None] = None


class ISISRedistributePolicy(BaseColumnModel):
    ipv4: Union[ISISRedistributeLevel, None] = None
    ipv6: Union[ISISRedistributeLevel, None] = None


class ISIS(BaseColumnModel):
    level: int = Field(None, ge=1, le=3)
    lsp_mtu: int = Field(1471, ge=1200, le=9200)
    iso: str
    interfaces: List[ISISInterface]
    redistribute: Union[ISISRedistributePolicy, None] = None
    meta: Union[dict, None] 


class IGPRoot(BaseColumnModel):
    isis: ISIS


class IGPContainer(BaseContainer):
    column_type: Literal['igp']
    column: Dict[str, IGPRoot]
