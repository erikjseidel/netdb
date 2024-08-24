from typing import Annotated, Union
from fastapi import Body

from .columns.device import DeviceContainer
from .columns.firewall import FirewallContainer
from .columns.policy import PolicyContainer
from .columns.interface import InterfaceContainer
from .columns.bgp import BGPContainer
from .columns.igp import IGPContainer

COLUMN_FACTORY = {
    'device': DeviceContainer,
    'firewall': FirewallContainer,
    'policy': PolicyContainer,
    'interface': InterfaceContainer,
    'bgp': BGPContainer,
    'igp': IGPContainer,
}

COLUMN_CLASSES = list(COLUMN_FACTORY.values())

COLUMN_TYPES = list(COLUMN_FACTORY.keys())

RootContainer = Annotated[
    Union[*COLUMN_CLASSES],
    Body(discriminator='column_type'),
]
