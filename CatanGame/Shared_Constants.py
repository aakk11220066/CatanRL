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
