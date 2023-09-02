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
