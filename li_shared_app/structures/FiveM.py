from typing import List

import ujson
from pydantic import BaseModel


class Player(BaseModel):
    endpoint: str
    id: int
    identifiers: List[str]
    name: str
    ping: int

    class Config:
        json_loads = ujson.loads


class Players(BaseModel):
    __root__: List[Player]

    class Config:
        json_loads = ujson.loads
