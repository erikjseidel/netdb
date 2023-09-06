from ..base import BaseContainer, BaseColumnModel
from typing import Literal, Optional, Dict, List
from pydantic import BaseModel, Field, Extra
from ipaddress import IPv6Address, IPv4Address


class DeviceCVars(BaseColumnModel):
    ibgp_ipv4: Optional[IPv4Address] = None
    ibgp_ipv6: Optional[IPv6Address] = None
    iso: Optional[str] = None
    router_id: IPv4Address
    local_asn: int = Field(ge=1, lt=2**32)

    class Config:
        extra = Extra.allow


class Device(BaseColumnModel):
    location: str
    providers: List[str]
    roles: Optional[List[str]] = None
    node_name: str
    meta: Optional[dict] = None
    cvars: DeviceCVars


class DeviceContainer(BaseContainer):
    __flat__ = True

    column_type: Literal['device']
    column: Dict[str, Device]
