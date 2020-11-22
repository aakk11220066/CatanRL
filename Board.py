import networkx as nx
import Tile
from Building import BuildingTypes
from Tile import TileType
from Shared_Constants import RANDOM_SEED, NO_PLAYER
from typing import Tuple, List
from random import choice
import random

Coordinate = Tuple[int, int]
rowWidths: List  # defined by _hexagonalBoard


random.seed(RANDOM_SEED)


# returns the coordinates of all 6 points around the given tile (all 6 corners of the hexagon)
def get_point_coordinates_around_tile(tile_position: Coordinate):
    for local_row in range(2):
        for local_col in range(3):
            yield tile_position[0] + local_row, 2 * tile_position[1] + local_col


# returns a standard hexagonal board to play on
def _hexagonalBoard(_size: int) -> nx.Graph:
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
            if row == 0 or col == 0 or col == rowWidth - 1 or row == len(rowWidths) - 1:
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
                tile_number = 0  # impossible dice roll
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


'''
tile at position (i,j) can be accessed with: Board.graph.nodes[("tile", (i,j))]
    which returns a dictionary with the tile's attributes.  Note that points and
    tiles are indexed in the same way as PyCatan library indexed them.
tile attributes: 
    position: Coordinate
    tile_type: Tile.TileType
    number: int
    thief: boolean
    
point at position (i,j) can be accessed with: Board.graph.nodes[("point", (i,j))]
    which returns a dictionary with the point's attributes.  Note that points and
    tiles are indexed in the same way as PyCatan library indexed them.
point attributes:
    position: Coordinate
    owner: int
    building: Building.BuildingTypes

edge connecting points (i,j) and (k,l) can be accessed with: 
    Board.graph[("point", (i,j))][("point", (k,l))]
    which returns a dictionary with the edge's attributes.
edge attributes:
    owner: int
    
edge connecting point (i,j) and tile (k,l) can be accessed with:
    Board.graph[("point", (i,j))][("tile", (k,l))]
    currently these edges have no attributes
    
Graph is undirected, of course.  Every tile is connected to all 6 points around it
    and each point is connected to the 3 points around it and the 3 tiles surrounding 
    it.  Points, tiles, and edges on the ocean are still considered regular points, 
    tiles, and edges. 
'''
class Board:
    def __init__(self, boardSize=3, thief_location=(1, 1)):  # locate thief at random location?
        self.graph = _hexagonalBoard(boardSize)
        self.boardSize = boardSize
        self._add_thief(thief_location)
        self.longest_road_owner = NO_PLAYER
        self.longest_road_length = 1

    def _add_thief(self, thief_location: Coordinate):
        self.graph.nodes[("tile", thief_location)]['thief'] = True
        self.thief_location = thief_location


    def get_road_length(self, new_road: Tuple[Coordinate, Coordinate], player) -> int:
        player_subgraph = self.graph.subgraph((u,v) for u,v,edge in self.graph.edges(data=True)
                           if "owner" in edge and edge["owner"] == player)

        # TODO: implement
