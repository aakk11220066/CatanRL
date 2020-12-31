from typing import Tuple
import CatanGame.Board

RANDOM_SEED = 42
NO_PLAYER = -1

Coordinate = Tuple[int, int]
TileCoordinate = Tuple[str, Coordinate]
PointCoordinate = Tuple[str, Coordinate]
RoadPlacement = Tuple[PointCoordinate, PointCoordinate]
Resource = str
PlayerNumber = int
ObservationType = CatanGame.Board