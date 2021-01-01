import sys  # FIXME: DELETE ME
from typing import Tuple, Dict, List

sys.path.append("C:\ProgramData\Miniconda3\Lib\site-packages")  # FIXME: DELETE ME
import gym
from CatanGame.CatanGame import CatanGame
from CatanGame.Exceptions import InvalidActionException
from Shared_Constants import PlayerNumber, PointCoordinate, RoadPlacement, ActionType


class GymInterface(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, player_num: PlayerNumber, game: CatanGame):
        super(GymInterface, self).__init__()
        # self.observation_space = None
        # self.action_space = None

        self.prev_victory_points = 0
        self.player_num = player_num
        self.game = game
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

    # -------------------- Gym helper methods -----------------

    def _build_first_buildings_round1(self,
                                      settlement_location: PointCoordinate,
                                      road_location: RoadPlacement):
        self.game.players[self.player_num - 1].desired_beginning_settlement_and_road_location = \
            (settlement_location, road_location)
        self.game.players[self.player_num - 1].buildSettlementAndRoadRound1(game=self.game)

    def _build_first_buildings_round2(self,
                                      settlement_location: PointCoordinate,
                                      road_location: RoadPlacement):
        self.game.players[self.player_num - 1].desired_beginning_settlement_and_road_location = \
            (settlement_location, road_location)
        self.game.players[self.player_num - 1].buildSettlementAndRoadRound2(game=self.game)

    def _buy_buildings(self, purchases: Dict):
        self.game.players[self.player_num - 1].desired_shopping_list = purchases
        self.game.players[self.player_num - 1].purchase_buildings_and_cards(game=self.game)

    # -------------------- Gym methods -----------------

    def step(self, action: dict):
        if action['action_type'] == ActionType.FIRST_BUILDING:
            self._build_first_buildings_round1(
                settlement_location=action['building_locations']["settlement"],
                road_location=action['building_locations']["road"]
            )

        elif action["action_type"] == ActionType.SECOND_BUILDING:
            self._build_first_buildings_round1(
                settlement_location=action['building_locations']["settlement"],
                road_location=action['building_locations']["road"]
            )

        elif action['action_type'] == ActionType.THIEF_PLACEMENT:
            self.game.players[self.player_num - 1].desired_thief_location = action['desired_thief_location']
            self.game.rollDice(player_num=self.player_num)

        elif action['action_type'] == ActionType.TRADE_RESOURCES:
            self.game.players[self.player_num - 1].desired_trades_list = action['desired_trades']
            self.game.players[self.player_num - 1].trade_resources()

        elif action['action_type'] == ActionType.BUILDINGS_PURCHASE:
            self._buy_buildings(purchases=action['purchases'])

        else:
            raise InvalidActionException()

        return self._get_info_for_player()

    def _get_info_for_player(self):
        observation = (self.game.board, self.game.players[self.player_num - 1].resources)

        reward = self.game.players[self.player_num - 1].victory_points - self.prev_victory_points
        self.prev_victory_points = self.game.players[self.player_num - 1].victory_points

        done = self.game.endGame()

        info = None

        return observation, reward, done, info

    def reset(self):
        self.prev_victory_points = 0
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

        return self.game.board

    def render(self, mode="human"):
        pass
