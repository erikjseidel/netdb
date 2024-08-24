from typing import Annotated, Union
from fastapi import Body

from .columns.device import DeviceContainer
from .columns.firewall import FirewallContainer
from .columns.policy import PolicyContainer
from .columns.interface import InterfaceContainer
from .columns.bgp import BGPContainer
from .columns.igp import IGPContainer

COLUMN_TYPES = [
    'device',
    'firewall',
    'policy',
    'interface',
    'bgp',
    'igp',
]

COLUMN_CLASSES = [
    DeviceContainer,  # device
    FirewallContainer,  # firewall
    PolicyContainer,  # policy
    InterfaceContainer,  # interface
    BGPContainer,  # bgp
    IGPContainer,  # igp
]

RootContainer = Annotated[
    Union[*COLUMN_CLASSES],
    Body(discriminator='column_type'),
]

COLUMN_FACTORY = dict(zip(COLUMN_TYPES, COLUMN_CLASSES))
