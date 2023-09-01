from ..base import BaseContainer, BaseColumnModel
from typing import Literal, Union, Dict, List
from pydantic import Field, IPvAnyInterface

class FirewallOptions(BaseColumnModel):
    all_ping: Union[str, None]                = Field(None, alias='all-ping')
    broadcast_ping: Union[str, None]          = Field(None, alias='broadcast-ping')
    config_trap: Union[str, None]             = Field(None, alias='config-trap')
    ipv6_receive_redirects: Union[str, None]  = Field(None, alias='ipv6-receive-redirects')
    ipv6_src_route: Union[str, None]          = Field(None, alias='ipv6-src-route')
    log_martians: Union[str, None]            = Field(None, alias='log-martians')
    send_redirects: Union[str, None]          = Field(None, alias='send-redirects')
    source_validation: Union[str, None]       = Field(None, alias='source-validation')
    syn_cookies: Union[str, None]             = Field(None, alias='syn-cookies')
    twa_hazards_protection: Union[str, None]  = Field(None, alias='twa-hazards-protection')
    ip_src_route: Union[str, None]            = Field(None, alias='ip-src-route')
    receive_redirect: Union[str, None]        = Field(None, alias='receive-redirect')


class FirewallMSSClamp(BaseColumnModel):
    ipv4: int = Field(ge=556, le=9172)
    ipv6: int = Field(ge=1280, le=9172)
    interfaces: List[str]


class FirewallStatePolicy(BaseColumnModel):
    established: Literal['accept', 'drop']
    related: Literal['accept', 'drop']


class FirewallZoneRule(BaseColumnModel):
    ipv4_ruleset: Union[str, None] = None
    ipv6_ruleset: Union[str, None] = None
    zone: str


class FirewallZonePolicy(BaseColumnModel):
    from_: Union[List[FirewallZoneRule], None] = Field(None, alias='from')
    interfaces: Union[List[str], None] = None
    default_action: Literal['accept', 'drop']


class FirewallGroup(BaseColumnModel):
    type: Literal['network']
    networks: List[IPvAnyInterface]


class FirewallGroupBase(BaseColumnModel):
    ipv4: Union[Dict[str, FirewallGroup], None] = None
    ipv6: Union[Dict[str, FirewallGroup], None] = None


class FirewallPolicyTarget(BaseColumnModel):
    network_group: Union[str, None] = None
    port: Union[List[int], None] = None


class FirewallPolicyRule(BaseColumnModel):
    action: Literal['accept', 'drop']
    state: Union[List[Literal['established', 'related']], None] = None
    source: Union[FirewallPolicyTarget, None] = None
    destination: Union[FirewallPolicyTarget, None] = None
    protocol: Union[str, None] = None


class FirewallPolicy(BaseColumnModel):
    default_action: Literal['accept', 'drop']
    rules: Union[List[FirewallPolicyRule], None] = None


class FirewallPolicyBase(BaseColumnModel):
    ipv4: Union[Dict[str, FirewallPolicy], None] = None
    ipv6: Union[Dict[str, FirewallPolicy], None] = None


class Firewall(BaseColumnModel):
    policies: Union[FirewallPolicyBase, None] = None
    groups: Union[FirewallGroupBase, None] = None
    state_policy: Union[FirewallStatePolicy, None] = None
    mss_clamp: Union[FirewallMSSClamp, None] = None
    zone_policy: Union[Dict[str, FirewallZonePolicy], None] = None
    options: FirewallOptions


class FirewallContainer(BaseContainer):
    __categories__ = [
            'policies',
            'groups',
            'zone_policy',
            ]

    column_type: Literal['firewall']
    column: Dict[str, Firewall]
