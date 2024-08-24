from typing import Literal, Optional
from pydantic import BaseModel


class NetdbDocument(BaseModel):
    set_id: str
    datasource: str
    weight: int
    flat: Optional[bool] = False
    category: Optional[str] = None
    family: Optional[Literal['ipv4', 'ipv6']] = None
    element_id: Optional[str] = None
    data: dict
