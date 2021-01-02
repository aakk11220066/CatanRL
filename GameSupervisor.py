# import networkx as nx
# import matplotlib.pyplot as plt
# import random
import itertools
from typing import List, Tuple

from CatanGame.CatanGame import CatanGame
from CatanGame.GUI import GUI
import CatanGame.CatanGame as GameHelperFunctions
from GymInterface import GymInterface
from PlayerControllers.PlayerController import PlayerController
from PlayerControllers.RandomPlayerController import RandomPlayerController

# DONE: divide files into folders, add README, add .gitignore
class GameSupervisor:
    def __init__(self, gui: bool = True, board_size: int = 3, order_player_game: List[int] = [1,2,3],
                 function_delay = 0.1):
        self.gui = gui
        if gui:
            board_size, order_player_game = GameHelperFunctions.enterParametersGame()
        self.board_size = board_size
        self.order_player_game = order_player_game
        self.game = CatanGame(board_size=board_size, order_player_game=order_player_game, function_delay=function_delay)
        self.controllers: List[Tuple[PlayerController, GymInterface]] = [
            (RandomPlayerController(player_num=i), GymInterface(player_num=i, game=self.game))
            for i in order_player_game
        ]

    def add_player_controller(self, player_controller: PlayerController):
        player_num = player_controller.player_num
        self.controllers[player_num - 1] = (
            player_controller,
            GymInterface(player_num=player_num, game=self.game)
        )

    def run_game(self, resource_boost_amount: int = 0):
        beginning_observation = self.reset()
        self._boost_resources(amount=resource_boost_amount)
        done = False

        for controller, gym_interface in self.controllers:
            action = controller.buildSettlementAndRoadRound1(observation=beginning_observation)
            beginning_observation, reward, done, info = gym_interface.step(action=action)
            controller.log_reward(reward=reward)

        for controller, gym_interface in reversed(self.controllers):
            action = controller.buildSettlementAndRoadRound2(
                observation=beginning_observation,
                collect_resources_around_settlement=self.game.collect_surrounding_resources
            )
            beginning_observation, reward, done, info = gym_interface.step(action=action)
            controller.log_reward(reward=reward)

        observation = beginning_observation
        for controller_pair in itertools.cycle(self.controllers):
            if done:
                break
            observation, done, info = self._play_turn(*controller_pair, observation=observation)

    def reset(self):
        self.game = CatanGame(board_size=self.board_size, order_player_game=self.order_player_game, function_delay=0.1)
        if self.gui:
            GUI(self.game).start()
        for _, gym_interface in self.controllers:
            gym_interface.reset()
            gym_interface.game = self.game
        return self.game.board, self.game.players[self.controllers[0][0].player_num - 1].resources

    # ----------------- CatanGame helper methods -------------------
    def _play_turn(self, controller: PlayerController, gym_interface: GymInterface, observation):
        print('@@@@@@@@@@@@@@@@@@@@ Player', controller.player_num, 'play @@@@@@@@@@@@@@@@@@@@')
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

        #self.game.players[player - 1].play_development_cards()  # Future implemention

        action = controller.get_desired_thief_location(observation=observation)
        observation, reward, done, info = gym_interface.step(action)
        controller.log_reward(reward=reward)

        action = controller.get_desired_trade(observation=observation)
        observation, reward, done, info = gym_interface.step(action)
        controller.log_reward(reward=reward)

        action = controller.purchase_buildings_and_cards(observation=observation)
        observation, reward, done, info = gym_interface.step(action=action)
        controller.log_reward(reward=reward)

        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

        return observation, done, info

    def _boost_resources(self, amount: int = 10):
        """
        Gives all players a large boost of available_resources to make the game easier to demonstrate
        """
        for player in self.game.players:
            player.resources["sheep"] += amount
            player.resources["wheat"] += amount
            player.resources["wood"] += amount
            player.resources["brick"] += amount
            player.resources["ore"] += amount


# DONE: add game + game_supervisor server that multiple gym environments attach to to allow for multiple RL agents
# DONE: random player should engage with this server too
if __name__ == "__main__":
    supervisor = GameSupervisor(gui=True) # player1=red, player2=yellow, player3=green
    supervisor.run_game(resource_boost_amount=100000000)

