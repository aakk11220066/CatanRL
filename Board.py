import networkx as nx
import Tile
from Building import BuildingTypes
from Building import is_valid_settlement_position, is_valid_road_position
from Tile import TileType
from Shared_Constants import RANDOM_SEED, NO_PLAYER
from typing import Tuple, List, Iterable
from random import choice
import random

Coordinate = Tuple[int, int]
rowWidths: List  # defined by _hexagonalBoard

random.seed(RANDOM_SEED)


def get_point_coordinates_around_tile(tile_position: Coordinate, actual_board_size: int):
    """
    :param tile_position: the coordinate of the tile whose point coordinates are desired
    :param actual_board_size: the size the user inputted + 1 (the "actual" size includes the layer of ocean)
    :returns the coordinates of all 6 points around the given tile (all 6 corners of the hexagon)
    """
    half_of_board = get_board_half(tile_position[0], actual_board_size)
    for local_row, local_col in [(0, 0), (0, 1), (0, 2), (1, 2), (1, 1), (1, 0), (0, 0)]:
        result = [tile_position[0] + local_row, 2 * tile_position[1] + local_col]

        # Hexagonal board causes offset between column indices of top points of tile and bottom point
        # due to different starting indices.  Exception is the middle row of the board.
        if (local_row == 1 and half_of_board == "upper") or (local_row == 0 and half_of_board == "lower"):
            result[1] += 1

        yield tuple(result)


# returns a standard hexagonal board to play on
def get_board_half(row: int, actual_board_size: int) -> str:
    assert (row >= 0 and actual_board_size > 0)
    if row < actual_board_size - 1:
        return "upper"
    if row == actual_board_size - 1:
        return "middle"
    return "lower"


def _hexagonalBoard(_size: int) -> nx.Graph:
    assert (_size > 1)
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
            for point_coordinates in get_point_coordinates_around_tile(tile_coordinates, size):
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

    def get_longest_road_length(self, player: int) -> int:
        players_edges = list((u, v) for u, v, edge in self.graph.edges(data=True)
                             if "owner" in edge and edge["owner"] == player)
        player_subgraph = nx.Graph(players_edges)
        longest_road_length = 0

        # NOTE: this loop a exponential time, presents a serious bottleneck
        for point in player_subgraph.nodes:
            longest_road_length = max(longest_road_length,
                                      _get_road_length(player_subgraph, road_start=point, player=player))

        return longest_road_length

    def get_valid_settlement_locations(self, player: int, start_of_game: bool = False) -> Iterable[
        Tuple[str, Coordinate]]:
        return filter(
            lambda node_label: is_valid_settlement_position(self.graph, node_label[1], player, start_of_game) and
                               node_label[0] == "point",
            self.graph.nodes
        )

    def get_valid_road_locations(self, player) -> Iterable[Tuple[Tuple[str, Coordinate], Tuple[str, Coordinate]]]:
        return filter(
            lambda edge_label: is_valid_road_position(self.graph, edge_label[0][1], edge_label[1][1], player) and
                               edge_label[0][0] == "point" and edge_label[1][0] == "point",
            self.graph.edges
        )

    def get_surrounding_tiles(self, settlement_location: Coordinate):
        return filter(
            lambda node_label: node_label[0] == "tile",
            self.graph.neighbors(("point", settlement_location))
        )


def _get_road_length(player_subgraph: nx.Graph, road_start: Coordinate, player) -> int:  # DFS
    longest_branch = 0
    for start, end in \
            ((start, end) for start, end, attributes in player_subgraph.edges(road_start, data=True)
             if "visited" not in attributes):
        player_subgraph.edges[start, end]["visited"] = None
        longest_branch = max(longest_branch, 1 + _get_road_length(player_subgraph, road_start=end, player=player))
        del player_subgraph.edges[start, end]["visited"]
    return longest_branch
