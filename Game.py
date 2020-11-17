from typing import Tuple

import Board
import Building

Coordinate = Tuple[int,int]

class Game:
    def __init__(self):
        self.board = Board.Board()

    def addSettlement(self, position: Coordinate, player: int):
        self.board.graph.nodes[("point", position)]["owner"] = player
        self.board.graph.nodes[("point", position)]["building"] = Building.BuildingTypes.Settlement
        # TODO: complete this function

    def addCity(self, position: Coordinate, player: int):
        self.board.graph.nodes[("point", position)]["owner"] = player
        self.board.graph.nodes[("point", position)]["building"] = Building.BuildingTypes.City
        # TODO: complete this function

    def addRoad(self, point1: Coordinate, point2: Coordinate, player: int):
        self.board.graph[("point", point1)][("point", point2)]["owner"] = player
        # TODO: complete this function