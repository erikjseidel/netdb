from typing import Annotated, Union
from fastapi import Body

from .containers.device import DeviceContainer
from .containers.firewall import FirewallContainer
from .containers.policy import PolicyContainer
from .containers.interface import InterfaceContainer
from .containers.bgp import BGPContainer
from .containers.igp import IGPContainer

COLUMN_TYPES = [
        'device',
        'firewall',
        'policy',
        'interface',
        'bgp',
        'igp',
        ]

RootContainer = Annotated[
        Union[
            DeviceContainer,     # device
            FirewallContainer,   # firewall
            PolicyContainer,     # policy
            InterfaceContainer,  # interface
            BGPContainer,        # bgp
            IGPContainer,        # igp
            ],
            Body(discriminator='column_type')
        ]
