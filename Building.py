from enum import Enum
from typing import Tuple
from networkx import Graph

from Shared_Constants import NO_PLAYER

Coordinate = Tuple[int, int]


class BuildingTypes(Enum):
    Empty = 0,
    Settlement = 1,
    City = 2


def _settlement_location_available(board: Graph, position: Coordinate):
    return board.has_node(("point", position)) \
           and board.nodes[("point", position)]["building"] == BuildingTypes.Empty


def _point_connected_to_road(board: Graph, position: Coordinate, player: int):
    return any(edge["owner"] == player
               for _, _, edge in board.edges(("point", position), data=True)
               if "owner" in edge)


def _settlement_far_from_neighbors(board: Graph, position: Coordinate):
    return all(board.nodes[neighbor_index]["building"] == BuildingTypes.Empty
               for neighbor_index in board.neighbors(("point", position))
               if "building" in board.nodes[neighbor_index])


def is_valid_settlement_position(board: Graph, position: Coordinate, player: int, start_of_game: bool = False):
    return _settlement_location_available(board, position) \
           and _settlement_far_from_neighbors(board, position) \
           and (_point_connected_to_road(board, position, player) or start_of_game)


def is_valid_city_position(board: Graph, position: Coordinate, player: int):
    return board.has_node(("point", position)) \
           and board.nodes[("point", position)]["owner"] == player \
           and board.nodes[("point", position)]["building"] == BuildingTypes.Settlement


def _edge_location_available(board: Graph, point1: Coordinate, point2: Coordinate):
    return board.has_edge(("point", point1), ("point", point2)) \
           and board.edges[("point", point1), ("point", point2)]["owner"] == NO_PLAYER


def _road_is_connected(board: Graph, road: Tuple[Coordinate, Coordinate], player: int):
    return any(road_end["owner"] == player
               for road_end in [board.nodes[("point", road[0])], board.nodes[("point", road[0])]]
               if "owner" in road_end) \
           or any(_point_connected_to_road(board, point, player) for point in road)


def is_valid_road_position(board: Graph, point1: Coordinate, point2: Coordinate, player: int):
    loc_av = _edge_location_available(board, point1, point2)
    rd_con = _road_is_connected(board, (point1, point2), player)
    return _edge_location_available(board, point1, point2) \
           and _road_is_connected(board, (point1, point2), player)
