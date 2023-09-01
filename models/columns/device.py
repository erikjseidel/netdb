from ..base import BaseContainer, BaseColumnModel
from typing import Literal, Union, Dict, List
from pydantic import BaseModel, Field, Extra
from ipaddress import IPv6Address, IPv4Address

class DeviceCVars(BaseColumnModel):
    ibgp_ipv4: Union[IPv4Address, None] = None
    ibgp_ipv6: Union[IPv6Address, None] = None
    iso: Union[str, None] = None
    router_id: IPv4Address
    local_asn: int = Field(ge=1,lt=2**32)

    class Config:
        extra = Extra.allow


class Device(BaseColumnModel):
    location: str
    providers: List[str]
    roles: Union[ List[str], None ] = None
    node_name: str
    meta: Union[dict, None] = None
    cvars: DeviceCVars


class DeviceContainer(BaseContainer):
    __flat__ = True

    column_type: Literal['device']
    column: Dict[str, Device] 
