import time
import random
from typing import Tuple

import Board
import Building
import Exceptions
from Player import Player
from Shared_Constants import NO_PLAYER

Coordinate = Tuple[int, int]
Player_number = int


class Game:
    """
    :param board_size: number of tiles along each side of the hexagonal board
    :param function_delay: how long to wait after performing each public function.
        Used to allow humans watching the GUI to watch the game unfold turn by turn
    """

    def __init__(self, board_size: int = 3, num_players: int = 3, function_delay=0):
        self.board = Board.Board(boardSize=board_size)
        self.players = [Player() for _ in range(num_players)]
        self.function_delay = function_delay

    def addSettlement(self, position: Coordinate, player_num: Player_number, start_of_game: bool = False):
        if not Building.is_valid_settlement_position(self.board.graph, position, player_num, start_of_game):
            raise Exceptions.InvalidSettlementPlacementException()
        self.players[player_num - 1].spend_resources(wood=1, brick=1, wheat=1, sheep=1)

        self.board.graph.nodes[("point", position)]["owner"] = player_num
        self.board.graph.nodes[("point", position)]["building"] = Building.BuildingTypes.Settlement
        self.players[player_num - 1].victory_points += 1

        time.sleep(self.function_delay)

    def addCity(self, position: Coordinate, player_num: Player_number):
        if not Building.is_valid_city_position(self.board.graph, position, player_num):
            raise Exceptions.InvalidCityPlacementException()
        self.players[player_num - 1].spend_resources(wheat=2, ore=3)

        self.board.graph.nodes[("point", position)]["owner"] = player_num
        self.board.graph.nodes[("point", position)]["building"] = Building.BuildingTypes.City
        self.players[player_num - 1].victory_points += 1

        time.sleep(self.function_delay)

    def _award_longest_road(self, loser: Player_number, award_to: Player_number):
        if loser != NO_PLAYER:
            self.players[loser - 1].victory_points -= 2
        self.players[award_to - 1].victory_points += 2
        self.board.longest_road_owner = award_to

    def addRoad(self, point1: Coordinate, point2: Coordinate, player_num: Player_number):
        if not Building.is_valid_road_position(self.board.graph, point1, point2, player_num):
            raise Exceptions.InvalidRoadPlacementException()
        self.players[player_num - 1].spend_resources(wood=1, brick=1)

        self.board.graph[("point", point1)][("point", point2)]["owner"] = player_num

        players_longest_road = self.board.get_longest_road_length(player=player_num)
        if players_longest_road > self.board.longest_road_length:
            self.board.longest_road_length = players_longest_road
            self._award_longest_road(loser=self.board.longest_road_owner, award_to=player_num)

        time.sleep(self.function_delay)

    def rollDice(self, player_num: Player_number):
        dice = random.randint(1, 6) + random.randint(1, 6)
        dice = 7
        if dice==7:
            for player in self.players:
                if player.get_number_of_resources()>7:
                    player.cutting_cards_in_half()
            self.players[player_num].move_thief(self.board)
        else:
            tiles = dict((k, v) for k, v in self.board.graph.nodes.items() if k[0] == "tile")
            points = dict((k, v) for k, v in self.board.graph.nodes.items() if k[0] == "point")
            for tile in tiles.values():
                if tile['number'] == dice:
                    if tile['thief'] == True:
                        continue
                    for point_coordinates in Board.get_point_coordinates_around_tile(tile['position']):
                        num_player = points[('point',point_coordinates)]['owner']
                        if num_player>0:
                            resource = tile['tile_type']
                            self.players[num_player].resources[resource] +=1
            

