from ..base import BaseContainer, BaseColumnModel
from typing import Literal, Union, Annotated, Dict, List
from pydantic import BaseModel, RootModel, Field, IPvAnyInterface, IPvAnyAddress, Extra
from ipaddress import IPv4Address

class InterfaceAddress(BaseColumnModel):
    meta: dict


class InterfaceVLANOptions(BaseColumnModel):
    id: int = Field(ge=1, le=4096)
    parent: str


class InterfaceLACPOptions(BaseColumnModel):
    hash_policy: Literal['layer2+3','layer3+4']
    rate: Literal['fast','slow']
    min_links: int = Field(ge=1, le=5)
    members: List[str]


class InterfacePolicy(BaseColumnModel):
    ipv4: Union[str, None] = None
    ipv6: Union[str, None] = None


class InterfaceFirewall(BaseColumnModel):
    local: Union[InterfacePolicy, None] = None
    egress: Union[InterfacePolicy, None] = None
    ingress: Union[InterfacePolicy, None] = None


class Interface(BaseColumnModel):
    type: Literal['ethernet', 'vlan', 'lacp', 'dummy', 'gre', 'l2gre']
    disabled: bool = False
    offload: bool = False
    description: Union[str, None] = None
    interface: Union[str, None] = None
    mac_address: Union[str, None] = None
    mtu: Union[int, None] = Field(None, ge=1280, le=9192)
    ttl: Union[int, None] = Field(None, ge=1, le=255)
    key: Union[IPv4Address, None] = None
    remote: Union[IPvAnyAddress, None] = None
    source: Union[IPvAnyAddress, None] = None
    address: Union[ Dict[ IPvAnyInterface, InterfaceAddress ], None ] = None
    vlan: Union[InterfaceVLANOptions, None] = None
    lacp: Union[InterfaceLACPOptions, None] = None
    firewall: Union[InterfaceFirewall, None] = None
    policy: Union[InterfacePolicy, None] = None
    meta: Union[dict, None] = None


class InterfaceRoot(RootModel):
    root: Dict[str, Interface]


class InterfaceContainer(BaseContainer):
    column_type: Literal['interface']
    column: Dict[str, InterfaceRoot]
