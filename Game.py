import time
import random
from typing import Tuple

import Board
import Building
import Exceptions
import Shared_Constants
from RandomPlayer import RandomPlayer
from Shared_Constants import NO_PLAYER
from Tile import tiletype_to_resourcetype, TileType

Coordinate = Tuple[int, int]
Player_number = int


class Game:
    """
    :param board_size: number of tiles along each side of the hexagonal board
    :param function_delay: how long to wait after performing each public function.
        Used to allow humans watching the GUI to watch the game unfold turn by turn
    """

    def __init__(self, board_size: int = 3, order_player_game: list = [(1, "BOT"),(2, "BOT")], threshold_victory_points=10, function_delay=0):
        self.board = Board.Board(boardSize=board_size)
        # Note: player number i should go in cell number i-1 (e.g. player 1 goes in cell 0)
        self.players = [RandomPlayer(player[0]) for player in order_player_game] # TODO: add non random players as well
        self.function_delay = function_delay
        self.threshold_victory_points = threshold_victory_points

    def _collect_surrounding_resources(self, settlement_location: Coordinate):
        player_num = self.board.graph.nodes[("point", settlement_location)]["owner"]
        assert (player_num != Shared_Constants.NO_PLAYER)
        for tile_type in map(lambda tile_label: self.board.graph.nodes[tile_label]["tile_type"],
                             self.board.get_surrounding_tiles(settlement_location)):
            resource_type = tiletype_to_resourcetype(tile_type)
            if resource_type:
                for player in self.players:
                    if player.player_number==player_num:
                        player.resources[resource_type] += 1
                        break
                #self.players[player_num].resources[resource_type] += 1

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
        if dice==7:
            for player in self.players:
                if player._get_number_of_resources()>7:
                    player.dropHalfCards()
            self.players[player_num].move_thief(self.board)
        else:
            tiles = dict((k, v) for k, v in self.board.graph.nodes.items() if k[0] == "tile" and v['tile_type']!=TileType.OCEAN)
            points = dict((k, v) for k, v in self.board.graph.nodes.items() if k[0] == "point")
            for tile in tiles.values():
                if tile['number'] == dice:
                    if tile['thief'] == True:
                        continue
                    for point_coordinates in Board.get_point_coordinates_around_tile(tile['position'], Board.get_board_half(row, size)): # TODO complete 'row' and 'size'
                        num_player = points[('point',point_coordinates)]['owner']
                        if num_player>0:
                            resource = tile['tile_type']
                            self.players[num_player].resources[resource] +=1

    def initializeGame(self):
        for player in self.players:
            player.buildSettlementAndRoadRound1(self) 
        for player in reversed(self.players):
            player.buildSettlementAndRoadRound2(self)

    def endGame(self):
        for player in self.players:
            if player.victory_points >= self.threshold_victory_points:
                print("The player ", player.player_number," won the game with ",player.victory_points," victory points!")
                return True
        return False
            

