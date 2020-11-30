from enum import Enum
from typing import Dict, List
import random

from Shared_Constants import RANDOM_SEED

NUM_HEXAGON_SIDES = 6
NUM_DESERTS = 1
NUM_TILE_TYPES = 7
NUM_NUMBERS = 12  # number of possible dice rolls

random.seed(RANDOM_SEED)


class TileType(Enum):
    FOREST = 0
    FIELDS = 1
    PASTURE = 2
    MOUNTAINS = 3
    HILLS = 4
    DESERT = 5
    OCEAN = 6

def tiletype_to_resourcetype(tiletype: TileType):
    if tiletype==TileType.FOREST:
        return "wood"
    if tiletype==TileType.FIELDS:
        return "wheat"
    if tiletype==TileType.PASTURE:
        return "sheep"
    if tiletype==TileType.MOUNTAINS:
        return "ore"
    if tiletype==TileType.HILLS:
        return "brick"
    if tiletype==TileType.DESERT or tiletype==TileType.OCEAN:
        return None


# returns the number of tiles of each type to add to the board
def get_tile_set(board_size: int, rowWidths: List[int]) -> Dict[TileType, int]:
    num_remaining_tiles = sum(rowWidths)
    result = dict()
    result[TileType.DESERT] = NUM_DESERTS
    num_remaining_tiles -= result[TileType.DESERT]
    result[TileType.OCEAN] = NUM_HEXAGON_SIDES * board_size
    num_remaining_tiles -= result[TileType.OCEAN]
    less_common_tile_frequency, extra_tiles = divmod(num_remaining_tiles, NUM_TILE_TYPES - 2)
    for tile_type in TileType:
        if tile_type == TileType.DESERT or tile_type == TileType.OCEAN:
            continue
        result[tile_type] = less_common_tile_frequency
        if extra_tiles != 0:
            result[tile_type] += 1
            extra_tiles -= 1

    return result

# returns how many numbers (dice rolls) of each type to add to the board
def get_tile_number_set(board_size: int, rowWidths: List[int]) -> Dict[int, int]:
    num_tile_numbers = sum(rowWidths) - NUM_DESERTS - NUM_HEXAGON_SIDES * board_size
    result = dict()
    for i in range(12):
        result[i+1] = 0
    for _ in range(num_tile_numbers):
        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        while roll1+roll2 == 7:
            roll1 = random.randint(1,6)
            roll2 = random.randint(1,6)
        result[roll1 + roll2] += 1
    for i in range(12):
        if result[i+1] == 0:
            del result[i+1]

    return result
