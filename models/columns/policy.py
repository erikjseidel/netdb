from ..base import BaseContainer, BaseColumnModel
from typing import Literal, Union, Dict, List
from pydantic import Field, IPvAnyAddress, IPvAnyNetwork


class PolicyBasicRule(BaseColumnModel):
    action: Literal['permit', 'deny']
    description: Union[str, None] = None
    regex: str


class PolicyCommunityRule(PolicyBasicRule):
    pass


class PolicyCommunity(BaseColumnModel):
    description: Union[str, None] = None
    rules: List[PolicyCommunityRule]


class PolicyASPathRule(PolicyBasicRule):
    pass


class PolicyASPath(BaseColumnModel):
    description: Union[str, None] = None
    rules: List[PolicyASPathRule]


class PolicyRouteMapSet(BaseColumnModel):
    local_pref: Union[int, None] = Field(None, ge=0, le=255)
    as_path_exclude: Union[int, None] = Field(None, ge=1, lt=2**32)
    next_hop: Union[IPvAnyAddress, None] = None
    origin: Union[str, None] = None
    community: Union[str, None] = None
    large_community: Union[str, None] = None


class PolicyRouteMapMatch(BaseColumnModel):
    prefix_list: Union[str, None] = None
    community_list: Union[str, None] = None
    as_path: Union[str, None] = None
    rpki: Literal['notfound', 'valid', 'invalid', None] = None


class PolicyRouteMapRule(BaseColumnModel):
    action: Literal['permit', 'deny']
    match: Union[PolicyRouteMapMatch, None] = None
    set: Union[PolicyRouteMapSet, None] = None
    number: int = Field(ge=0, le=999)
    continue_: Union[int, None] = Field(None, ge=0, le=999, alias='continue')


class PolicyRouteMap(BaseColumnModel):
    rules: List[PolicyRouteMapRule]


class PolicyRouteMapBase(BaseColumnModel):
    ipv4: Union[Dict[str, PolicyRouteMap], None] = None
    ipv6: Union[Dict[str, PolicyRouteMap], None] = None


class PolicyPrefixListRules(BaseColumnModel):
    le: Union[int, None] = Field(None, ge=0, le=128)
    ge: Union[int, None] = Field(None, ge=0, le=128)
    prefix: IPvAnyNetwork


class PolicyPrefixList(BaseColumnModel):
    rules: List[PolicyPrefixListRules]


class PolicyPrefixListBase(BaseColumnModel):
    ipv4: Union[Dict[str, PolicyPrefixList], None] = None
    ipv6: Union[Dict[str, PolicyPrefixList], None] = None


class Policy(BaseColumnModel):
    prefix_lists: Union[PolicyPrefixListBase, None] = None
    route_maps: Union[PolicyRouteMapBase, None] = None
    aspath_lists: Union[Dict[str, PolicyASPath], None] = None
    community_lists: Union[Dict[str, PolicyCommunity], None] = None


class PolicyContainer(BaseContainer):
    __categories__ = [
            'prefix_lists',
            'route_maps',
            'aspath_lists',
            'community_lists',
            ]

    column_type: Literal['policy']
    column: Dict[str, Policy]
