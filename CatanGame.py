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


class CatanGame:
    """
    :param board_size: number of tiles along each side of the hexagonal board
    :param function_delay: how long to wait after performing each public function.
        Used to allow humans watching the GUI to watch the game unfold turn by turn
    """

    def __init__(self, board_size: int = 3, order_player_game: list = [1,2], threshold_victory_points=10, function_delay=0):
        self.board = Board.Board(boardSize=board_size)
        # Note: player number i should go in cell number i-1 (e.g. player 1 goes in cell 0)
        self.players = [RandomPlayer(player_number=player) for player in order_player_game] # TODO: add non random players as well
        self.function_delay = function_delay
        self.threshold_victory_points = threshold_victory_points

    def _collect_surrounding_resources(self, settlement_location: Coordinate):
        player_num = self.board.graph.nodes[("point", settlement_location)]["owner"]
        assert (player_num != Shared_Constants.NO_PLAYER)
        for tile_type in map(lambda tile_label: self.board.graph.nodes[tile_label]["tile_type"],
                             self.board.get_surrounding_tiles(settlement_location)):
            resource_type = tiletype_to_resourcetype(tile_type)
            if resource_type:
                self.players[player_num - 1].resources[resource_type] += 1

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
        print("Dice: ",dice)
        if dice==7:
            for player in self.players:
                if player._get_number_of_resources()>7:
                    player.dropHalfCards()
            self.players[player_num-1].move_thief(self.board)
        else:
            tiles = dict((k, v) for k, v in self.board.graph.nodes.items() if k[0] == "tile" and v['tile_type']!=TileType.OCEAN)
            points = dict((k, v) for k, v in self.board.graph.nodes.items() if k[0] == "point")
            for tile in tiles.values():
                if tile['number'] == dice:
                    if tile['thief'] == True:
                        continue
                    for point_coordinates in Board.get_point_coordinates_around_tile(tile['position'], actual_board_size=self.board.boardSize+1):
                        #print("point_coordinates:",point_coordinates)
                        num_player = points[('point',point_coordinates)]['owner']
                        if num_player>0:
                            resource_type = tiletype_to_resourcetype(tile['tile_type'])
                            self.players[num_player-1].resources[resource_type] +=1
                            print("Player:",num_player,"-> Resource:",resource_type)

    def endGame(self):
        for player in self.players:
            if player.victory_points >= self.threshold_victory_points:
                print("The player ", player.player_number," won the game with ",player.victory_points," victory points!")
                return True
        return False

# --------------------HELPER FUNCTIONS FOR PREPPING GAME------------------
def _swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

def makeOrderPlayerGame(num_of_players):
    players = [x + 1 for x in list(range(num_of_players))]
    '''len = num_of_players
    order_player_game = []
    for i in range(num_of_players):
        player = random.choice(players[:len])
        if player <= num_of_players - num_of_bots:
            order_player_game.append((player, "HUMAN"))
        else:
            order_player_game.append((player, "BOT"))
        _swapPositions(players, player - 1, len - 1)
        len -= 1
    return order_player_game'''
    return players

def enterParametersGame():
    # Defined board size (scale)
    board_size = int(input("Please select the game board size (2,3,4...): "))
    while board_size < 2:
        board_size = int(input("Illegal board size. Try again.\nPlease select the game board size (2,3,4...): "))
    # Defined players
    num_of_players = int(input("How many players are playing (2,3,4...)? "))
    while num_of_players < 2:
        num_of_players = int(input("Illegal number of players. Try again.\nHow many players are playing (2,3,4...)? "))
    num_of_bots = int(input("How many computer bots are playing? (from 0 to " + str(num_of_players) + "): "))
    while not (num_of_players >= num_of_bots and num_of_bots >= 0):
        num_of_bots = int(input(
            "Illegal number of computer bots. Try again.\nHow many computer bots are playing? (from 0 to " + str(
                num_of_players) + "): "))
    order_player_game = makeOrderPlayerGame(num_of_players)
    print("The game contains " + str(num_of_players - num_of_bots) + " human players and " + str(num_of_bots) + " bots!")
    print("The order game playing: ")
    [print(e) for e in order_player_game]
    return board_size, order_player_game
