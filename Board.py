import networkx as nx

import Tile
from Building import BuildingTypes
from Tile import TileType, RANDOM_SEED
from typing import Tuple, List
from random import choice
import random

Coordinate = Tuple[int, int]
rowWidths: List  # defined by _hexagonalBoard

NO_PLAYER = 0

random.seed(RANDOM_SEED)


def get_point_coordinates_around_tile(tile_position: Coordinate):
    for local_row in range(2):
        for local_col in range(3):
            yield tile_position[0] + local_row, 2 * tile_position[1] + local_col


def _hexagonalBoard(_size: int):
    assert (_size > 0)
    size = _size + 1  # account for ocean surrounding board
    result = nx.Graph()

    global rowWidths
    rowWidths = [row + size for row in range(size)]
    rowWidths.extend((3 * size - 2 - row for row in range(size, 2 * size - 1)))
    tile_set = Tile.get_tile_set(_size, rowWidths=rowWidths)
    number_set = Tile.get_tile_number_set(_size, rowWidths)
    for row, rowWidth in enumerate(rowWidths):
        for col in range(rowWidth):
            tile_coordinates = (row, col)

            # add tile
            # select type
            if row == 0 or col == 0 or col == rowWidth-1 or row == len(rowWidths)-1:
                tile_type = TileType.OCEAN
            else:
                tile_type = choice(list(tile_set.keys()))
                while tile_type == TileType.OCEAN:
                    tile_type = choice(list(tile_set.keys()))
            tile_set[tile_type] -= 1
            if tile_set[tile_type] == 0:
                del tile_set[tile_type]

            # select number
            if tile_type not in {TileType.OCEAN, TileType.DESERT}:
                tile_number = choice(list(number_set.keys()))
                number_set[tile_number] -= 1
                if number_set[tile_number] == 0:
                    del number_set[tile_number]
            else:
                tile_number = 0 # impossible dice roll
            result.add_node(
                ("tile", tile_coordinates),
                position=tile_coordinates,
                tile_type=tile_type,
                number=tile_number,
                thief=False
            )

            prev_point_coordinates = None
            for point_coordinates in get_point_coordinates_around_tile(tile_coordinates):
                # add surrounding points
                result.add_node(
                    ("point", point_coordinates),
                    position=point_coordinates,
                    owner=NO_PLAYER,
                    building=BuildingTypes.Empty
                )
                # connect surrounding points to tile
                result.add_edge(("tile", tile_coordinates), ("point", point_coordinates))

                # connect surrounding points to each other
                if prev_point_coordinates is not None:
                    result.add_edge(
                        ("point", point_coordinates), ("point", prev_point_coordinates),
                        owner=NO_PLAYER
                    )

                prev_point_coordinates = point_coordinates

    return result


class Board:
    def _add_thief(self, thief_location: Coordinate):
        self.graph.nodes[("tile", thief_location)]['thief'] = True
        self.thief_location = thief_location

    def __init__(self, boardSize=3, thief_location=(1, 1)):  # locate thief at random location?
        self.graph = _hexagonalBoard(boardSize)
        self.boardSize = boardSize
        self._add_thief(thief_location)
