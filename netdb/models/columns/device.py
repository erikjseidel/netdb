from typing import Literal, Optional, Dict, List
from ipaddress import IPv6Address, IPv4Address, IPv4Network
from pydantic import Field, Extra, IPvAnyAddress, IPvAnyNetwork
from ..base import BaseContainer, BaseColumnModel


class DeviceCVars(BaseColumnModel):
    ibgp_ipv4: Optional[IPv4Address] = None
    ibgp_ipv6: Optional[IPv6Address] = None
    iso: Optional[str] = None
    router_id: IPv4Address
    local_asn: int = Field(ge=1, lt=2**32)
    primary_ipv4: IPv4Address
    primary_ipv6: IPv6Address
    dns_servers: List[IPvAnyAddress]
    znsl_prefixes: List[IPvAnyNetwork]

    class Config:
        extra = Extra.allow


class DHCPRange(BaseColumnModel):
    start_address: IPv4Address
    end_address: IPv4Address


class DHCPServer(BaseColumnModel):
    router_ip: IPv4Address
    network: IPv4Network
    ranges: List[DHCPRange]


class Device(BaseColumnModel):
    location: str
    providers: List[str]
    roles: Optional[List[str]] = None
    node_name: str
    meta: Optional[dict] = None
    cvars: DeviceCVars
    dhcp_servers: Optional[List[DHCPServer]] = None


class DeviceContainer(BaseContainer):
    __flat__ = True

    column_type: Literal['device']
    column: Dict[str, Device]
