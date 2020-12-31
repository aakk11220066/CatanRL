# import networkx as nx
# import matplotlib.pyplot as plt
# import random
import itertools
from typing import List, Tuple

from CatanGame.CatanGame import CatanGame
import CatanGame.CatanGame as GameHelperFunctions
from GymInterface import GymInterface
from PlayerControllers.PlayerController import PlayerController
from PlayerControllers.RLPlayerController import RLPlayerController
from PlayerControllers.RandomPlayerController import RandomPlayerController
from Shared_Constants import PlayerNumber, ObservationType

# TODO: divide files into folders, add README, add .gitignore
class GameSupervisor:
    def __init__(self, RL_player_num: int = 1, gui: bool = False):
        board_size, order_player_game = GameHelperFunctions.enterParametersGame()
        self.order_player_game = order_player_game
        self.game = CatanGame(board_size=board_size, order_player_game=order_player_game, function_delay=0.1)
        self.controllers: List[Tuple[PlayerController, GymInterface]] = []
        assert (len(self.controllers) == len(order_player_game))

    def add_RLPlayer(self, player_num: PlayerNumber):
        self.controllers.append((
            RLPlayerController(player_num=player_num, game=self.game),
            GymInterface(player_num=player_num, game=self.game)
        ))

    def add_RandomPlayer(self, player_num: PlayerNumber):
        self.controllers.append((
            RandomPlayerController(player_num=player_num, game=self.game),
            GymInterface(player_num=player_num, game=self.game)
        ))

    def run_game(self):
        beginning_observation = self.reset()
        done = False

        for controller, gym_interface in self.controllers:
            action = controller.buildSettlementAndRoadRound1(observation=beginning_observation)
            beginning_observation, reward, done, info = gym_interface.step(action=action)
            controller.log_reward(reward=reward)

        for controller, gym_interface in reversed(self.controllers):
            action = controller.buildSettlementAndRoadRound2(observation=beginning_observation)
            beginning_observation, reward, done, info = gym_interface.step(action=action)
            controller.log_reward(reward=reward)

        observation = beginning_observation
        for controller_pair in itertools.cycle(self.controllers):
            if not done:
                observation = self._playTurn(*controller_pair)

    def reset(self):
        self.game = CatanGame(board_size=self.game.board.board_size, order_player_game=self.order_player_game, function_delay=0.1)
        for _, gym_interface in self.controllers:
            gym_interface.reset()
        return self.game.board

    # ----------------- CatanGame helper methods -------------------
    def _playTurn(self, controller: PlayerController, gym_interface: GymInterface, observation: ObservationType):
        print('@@@@@@@@@@@@@@@@@@@@ Player', controller.player_num, 'play @@@@@@@@@@@@@@@@@@@@')
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

        #self.game.players[player - 1].play_development_cards()  # Future implemention

        action = controller.get_desired_thief_location(observation=observation)
        observation, reward, done, info = gym_interface.step(action)
        controller.log_reward(reward=reward)

        #self.game.players[player - 1].trade_cards()  # Future implemention

        action = controller.buy_road_or_settlement_or_city_or_development_card(observation=observation)
        observation, reward, done, info = gym_interface.step(action=action)
        controller.log_reward(reward=reward)

        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

        return observation

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


# DONE: add game + game_supervisor server that multiple gym environments attach to to allow for multiple RL agents
# DONE: random player should engage with this server too
if __name__ == "__main__":
    supervisor = GameSupervisor()
    # TODO: add some Controllers
    supervisor.run_game()

