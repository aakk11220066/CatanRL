import time
import random

import CatanGame.Board as Board
import CatanGame.Building as Building
from CatanGame import Exceptions
import Shared_Constants
from Shared_Constants import RoadPlacement, PointCoordinate, PlayerNumber
from CatanGame.Player import Player
from Shared_Constants import NO_PLAYER
from CatanGame.Tile import tiletype_to_resourcetype, TileType


class CatanGame:
    """
    :param board_size: number of tiles along each side of the hexagonal board
    :param function_delay: how long to wait after performing each public function.
        Used to allow humans watching the GUI to watch the game unfold turn by turn
    """

    def __init__(self, board_size: int = 3, order_player_game: list = [1, 2], threshold_victory_points=10,
                 function_delay=0):
        self.board = Board.Board(boardSize=board_size)
        # Note: player number i should go in cell number i-1 (e.g. player 1 goes in cell 0)
        self.players = [Player(player_num=player) for player in order_player_game]
        self.function_delay = function_delay
        self.threshold_victory_points = threshold_victory_points

    def add_settlement(self, position: PointCoordinate, player_num: PlayerNumber, start_of_game: bool = False):
        if not Building.is_valid_settlement_position(self.board.graph, position, player_num, start_of_game):
            raise Exceptions.InvalidSettlementPlacementException()
        self.players[player_num - 1].spend_resources(**Building.prices["settlement"])

        self.board.graph.nodes[position]["owner"] = player_num
        self.board.graph.nodes[position]["building"] = Building.BuildingTypes.Settlement
        self.players[player_num - 1].victory_points += 1

        time.sleep(self.function_delay)

    def add_city(self, position: PointCoordinate, player_num: PlayerNumber):
        if not Building.is_valid_city_position(self.board.graph, position[1], player_num):
            raise Exceptions.InvalidCityPlacementException()
        self.players[player_num - 1].spend_resources(**Building.prices["city"])

        self.board.graph.nodes[("point", position[1])]["owner"] = player_num
        self.board.graph.nodes[("point", position[1])]["building"] = Building.BuildingTypes.City
        self.players[player_num - 1].victory_points += 1

        time.sleep(self.function_delay)

    def add_road(self, road: RoadPlacement, player_num: PlayerNumber):
        point1, point2 = road

        if not Building.is_valid_road_position(board=self.board.graph, road=road, player=player_num):
            raise Exceptions.InvalidRoadPlacementException()
        self.players[player_num - 1].spend_resources(**Building.prices["road"])

        self.board.graph[point1][point2]["owner"] = player_num
        players_longest_road = self.board.get_longest_road_length(player=player_num)
        if players_longest_road > self.board.longest_road_length:
            self.board.longest_road_length = players_longest_road
            self._award_longest_road(loser=self.board.longest_road_owner, award_to=player_num)

        time.sleep(self.function_delay)

    def roll_dice(self, player_num: PlayerNumber):
        dice = random.randint(1, 6) + random.randint(1, 6)
        print("Dice: ", dice)
        if dice == 7:
            # for player in self.players:
            #    if player._get_number_of_resources()>7:
            #        player.drop_half_cards()
            self.players[player_num - 1].move_thief(self.board)
        else:
            tiles = dict((k, v) for k, v in self.board.graph.nodes.items() if
                         k[0] == "tile" and v['tile_type'] != TileType.OCEAN)
            points = dict((k, v) for k, v in self.board.graph.nodes.items() if k[0] == "point")
            for tile in tiles.values():
                if tile['number'] == dice:
                    if tile['thief']:
                        continue
                    for point_coordinates in Board.get_point_coordinates_around_tile(tile['position'],
                                                                                     actual_board_size=self.board.boardSize + 1):
                        num_player = points[('point', point_coordinates)]['owner']
                        if num_player > 0:
                            resource_type = tiletype_to_resourcetype(tile['tile_type'])
                            self.players[num_player - 1].resources[resource_type] += 1
                            print("Player:", num_player, "-> Resource:", resource_type)

    def end_game(self):
        for player in self.players:
            if player.victory_points >= self.threshold_victory_points:
                print("Player", player.player_num, "won the game with ", player.victory_points,
                      " victory points!")
                return True
        return False

    # ---- helper methods -----

    def collect_surrounding_resources(self, settlement_location: PointCoordinate):
        player_num = self.board.graph.nodes[settlement_location]["owner"]
        # assert (player_num != Shared_Constants.NO_PLAYER)
        for tile_type in map(lambda tile_label: self.board.graph.nodes[tile_label]["tile_type"],
                             self.board.get_surrounding_tiles(settlement_location)):
            resource_type = tiletype_to_resourcetype(tile_type)
            if resource_type:
                self.players[player_num - 1].resources[resource_type] += 1

    def _award_longest_road(self, loser: PlayerNumber, award_to: PlayerNumber):
        if loser != NO_PLAYER:
            self.players[loser - 1].victory_points -= 2
        self.players[award_to - 1].victory_points += 2
        self.board.longest_road_owner = award_to


# --------------------HELPER FUNCTIONS FOR PREPPING GAME------------------
def _swap_positions(_list, pos1, pos2):
    _list[pos1], _list[pos2] = _list[pos2], _list[pos1]
    return _list


def make_order_player_game(num_of_players):
    players = [x + 1 for x in list(range(num_of_players))]
    '''len = num_of_players
    order_player_game = []
    for i in range(num_of_players):
        player = random.choice(players[:len])
        if player <= num_of_players - num_of_bots:
            order_player_game.append((player, "HUMAN"))
        else:
            order_player_game.append((player, "BOT"))
        _swap_positions(players, player - 1, len - 1)
        len -= 1
    return order_player_game'''
    return players


def enter_parameters_game():
    # Defined board size (scale)
    board_size = int(input("Please select the game board size (2,3,4...): "))
    while board_size < 2:
        board_size = int(input("Illegal board size. Try again.\nPlease select the game board size (2,3,4...): "))
    # Defined players
    num_of_players = int(input("How many players are playing (2,3,4...)? "))
    while num_of_players < 2:
        num_of_players = int(input("Illegal number of players. Try again.\nHow many players are playing (2,3,4...)? "))
    num_of_bots = int(input("How many computer bots are playing? (from 0 to " + str(num_of_players) + "): "))
    while not (num_of_players >= num_of_bots >= 0):
        num_of_bots = int(input(
            "Illegal number of computer bots. Try again.\nHow many computer bots are playing? (from 0 to " + str(
                num_of_players) + "): "))
    order_player_game = make_order_player_game(num_of_players)
    print(
        "The game contains " + str(num_of_players - num_of_bots) + " human players and " + str(num_of_bots) + " bots!")
    print("The order game playing: ")
    [print(e) for e in order_player_game]
    return board_size, order_player_game
