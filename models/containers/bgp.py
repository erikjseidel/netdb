from ..base import BaseContainer, BaseColumnModel
from typing import Literal, Union, Dict, List
from pydantic import Field, IPvAnyAddress, IPvAnyNetwork
from ipaddress import IPv4Address

class BGPOptions(BaseColumnModel):
    asn: int = Field(ge=1, lt=2**32)
    hold_time: Union[int, None] = Field(None, ge=15, le=180)
    keepalive_time: Union[int, None] = Field(None, ge=5, le=60)
    log_neighbor_changes: bool = False
    router_id: IPv4Address
    cluster_id: Union[IPv4Address, None] = None
    meta: Union[dict, None] = None


class BGPAddressFamilyElement(BaseColumnModel):
    networks: Union[List[IPvAnyNetwork], None] = None
    redistribute: List[str]


class BGPAddressFamily(BaseColumnModel):
    ipv4: Union[BGPAddressFamilyElement, None] = None
    ipv6: Union[BGPAddressFamilyElement, None] = None


class BGPRouteMap(BaseColumnModel):
    import_: Union[str, None] = Field(None, alias='import')
    export: Union[str, None] = None


class BGPFamilyOptions(BaseColumnModel):
    nhs: Union[bool, None] = None
    max_prefixes: Union[int, None] = Field(None, ge=1)
    route_reflector: Union[bool, None] = None
    default_originate: Union[bool, None] = None
    route_map: Union[BGPRouteMap, None] = None


class BGPFamily(BaseColumnModel):
    ipv4: Union[BGPFamilyOptions, None] = None
    ipv6: Union[BGPFamilyOptions, None] = None


class BGPTimers(BaseColumnModel):
    holdtime: int = Field(ge=15,le=3000)
    keepalive: int = Field(ge=5,le=1000)


class BGPPeerGroup(BaseColumnModel):
    type: Literal['ibgp', 'ebgp'] = 'ebgp'
    source: Union[IPvAnyAddress, None] = None
    family: Union[BGPFamily, None] = None
    multihop: Union[int, None] = Field(None, ge=1, le=255)
    password: Union[str, None] = None
    remote_asn: Union[int, None] = Field(None, ge=1, lt=2**32)
    meta: Union[dict, None] = None


# Neighbor extends peergroup with a couple of additional options.
class BGPNeighbor(BGPPeerGroup):
    peer_group: Union[str, None] = None
    timers: Union[BGPTimers, None] = None


class BGP(BaseColumnModel):
    options: Union[BGPOptions, None] = None
    address_family: Union[ BGPAddressFamily, None ] = None
    peer_groups: Union[ Dict[str, BGPPeerGroup], None ] = None
    neighbors: Union[ Dict[str, BGPNeighbor], None ] = None


class BGPContainer(BaseContainer):
    __categories__ = ['peer_groups', 'neighbors']

    column_type: Literal['bgp']
    column: Dict[str, BGP]
