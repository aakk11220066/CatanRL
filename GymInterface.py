import sys  # FIXME: DELETE ME
from typing import Tuple, Dict, List

sys.path.append("C:\ProgramData\Miniconda3\Lib\site-packages")  # FIXME: DELETE ME
import gym
from CatanGame import CatanGame
from CatanGame import Coordinate
from Board import Board
import CatanGame as GameHelperFunctions
from itertools import count
from RLPlayer import RLPlayer


def _get_beginning_builder_method(
        settlement_location: Tuple[str, Coordinate],
        road_location: Tuple[Tuple[str, Coordinate], Tuple[str, Coordinate]],
        player_num: int):
    def result(self, game: CatanGame):
        game.addSettlement(position=settlement_location[1], player_num=player_num, start_of_game=True)
        game.addRoad(point1=road_location[0][1], point2=road_location[1][1], player_num=player_num)

    return result


def _get_thief_mover_method(new_thief_location: Tuple[str, Coordinate]):
    def result(self, board: Board):
        board.move_thief(thief_new_location=new_thief_location[1])

    return result


def get_purchase_maker_method(purchases: Dict[str, List], player_num: int):
    def result(game: CatanGame):
        for settlement in purchases["settlements"]:
            game.addSettlement(position=settlement[1], player_num=player_num)
        for city in purchases["cities"]:
            game.addCity(position=city[1], player_num=player_num)
        for road in purchases["roads"]:
            game.addRoad(point1=road[0][1], point2=road[1][1], player_num=player_num)

    return result


class GymInterface(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, RL_player_num: int):
        super(GymInterface, self).__init__()
        # self.observation_space = None
        # self.action_space = None

        self.prev_victory_points = 0
        self.RL_player_num = RL_player_num
        board_size, order_player_game = GameHelperFunctions.enterParametersGame()

        self.game = CatanGame(board_size=board_size, order_player_game=order_player_game, function_delay=0.1)
        self.game.players[RL_player_num - 1] = RLPlayer()
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    # -------------------- Gym helper methods -----------------

    def _init_game(self):
        # run game until RL agent's turn
        for player in self.game.players[:self.RL_player_num - 1]:
            player.buildSettlementAndRoadRound1(self)

    def _build_first_buildings(self,
                               settlement_location: Tuple[str, Coordinate],
                               road_location: Tuple[Tuple[str, Coordinate], Tuple[str, Coordinate]]):
        self.game.players[self.RL_player_num - 1].buildSettlementAndRoadRound1 = \
            self.game.players[self.RL_player_num - 1].buildSettlementAndRoadRound2 = \
            _get_beginning_builder_method(settlement_location, road_location, player_num=self.RL_player_num)

        if not hasattr(self, "round2"):
            for player in self.game.players[self.RL_player_num - 1:]:
                player.buildSettlementAndRoadRound1(self.game)
            self.round2 = True
            for player in reversed(self.game.players)[:-(self.RL_player_num - 1)]:
                player.buildSettlementAndRoadRound2(self.game)
        else:
            for player in self.game.players[-(self.RL_player_num - 1):]:
                player.buildSettlementAndRoadRound2(self.game)
            delattr(self, "round2")

    def _buy_buildings(self, purchases: Dict):
        self.game.players[self.RL_player_num - 1].buy_road_or_settlement_or_city_or_development_card = \
            get_purchase_maker_method(purchases, player_num=self.RL_player_num)
        self.game.players[self.RL_player_num - 1].buy_road_or_settlement_or_city_or_development_card(game=self.game)

        # Run all players until RL agent
        for player in self._get_player_turns():
            if player == self.RL_player_num:
                break
            self._playTurn(player)

    # -------------------- Gym methods -----------------

    def step(self, action: dict): # TODO: document actions
        if action['action_type'] == "first_building":
            self._build_first_buildings(
                settlement_location=action['building_locations']["settlement"],
                road_location=action['building_locations']["road"]
            )

        elif action['action_type'] == "thief placement":
            self.game.players[self.RL_player_num - 1].move_thief = \
                _get_thief_mover_method(action['desired_thief_location'])
            self.game.rollDice(player_num=self.RL_player_num)

        elif action['action_type'] == "buildings purchase":
            self._buy_buildings(purchases=action['purchases'])


        return self._get_info_for_player()

    def _get_player_turns(self):
        for player in count():
            yield (player % len(self.game.players)) + 1

    def _get_observation(self):
        return self.game.board # TODO: write separate class to translate board to PyGeometric

    def _get_info_for_player(self):
        observation = self._get_observation()

        reward = self.game.players[self.RL_player_num - 1].victory_points - self.prev_victory_points
        self.prev_victory_points = self.game.players[self.RL_player_num - 1].victory_points

        done = self.game.endGame()

        info = None

        return observation, reward, done, info

    def reset(self):
        self.prev_victory_points = 0
        # TODO: reset turn counter
        board_size, order_player_game = GameHelperFunctions.enterParametersGame()

        self.game = CatanGame(board_size=board_size, order_player_game=order_player_game, function_delay=0.1)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

        self._init_game()
        return self._get_observation()

    def render(self, mode="human"):
        pass

    # -------------------- CatanGame methods -----------------

    def _playTurn(self, player: int):
        assert (isinstance(player, int))
        print('@@@@@@@@@@@@@@@@@@@@ Player', player, 'play @@@@@@@@@@@@@@@@@@@@')
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        self.game.players[player - 1].play_development_cards()  # Future implemention
        self.game.rollDice(player_num=player)
        self.game.players[player - 1].trade_cards()  # Future implemention
        self.game.players[player - 1].buy_road_or_settlement_or_city_or_development_card(game=self.game)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    def _boost_resources(self):
        """
        Gives all players a large boost of resources to make the game easier to demonstrate
        """
        for player in self.game.players:
            player.resources["sheep"] += 10
            player.resources["wheat"] += 10
            player.resources["wood"] += 10
            player.resources["brick"] += 10
            player.resources["ore"] += 10
