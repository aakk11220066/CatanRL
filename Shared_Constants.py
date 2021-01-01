from typing import Tuple
from enum import Enum

RANDOM_SEED = 42
NO_PLAYER = -1
BANK_TRADE_PRICE = 4

Coordinate = Tuple[int, int]
TileCoordinate = Tuple[str, Coordinate]
PointCoordinate = Tuple[str, Coordinate]
RoadPlacement = Tuple[PointCoordinate, PointCoordinate]
Resource = str
PlayerNumber = int


class ActionType(Enum):
    FIRST_BUILDING = 0
    SECOND_BUILDING = 1
    THIEF_PLACEMENT = 2
    BUILDINGS_PURCHASE = 3
    TRADE_RESOURCES = 4