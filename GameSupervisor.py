#import networkx as nx
#import matplotlib.pyplot as plt
#import random
from GUI import GUI
from GymInterface import GymInterface
from PlayerController import PlayerController

class GameSupervisor:
    def __init__(self, RL_player_num: int = 1):
        self.RL_player_num = RL_player_num
        self.gym = GymInterface(RL_player_num=RL_player_num)
        GUI(self.gym.game).start()

    def run_game(self, outside_player: PlayerController):
        start_building_round1_observation = self.gym.reset()
        action = {
            "action_type":"first_building",
            "building_locations":outside_player.buildSettlementAndRoadRound1(start_building_round1_observation)
        }
        last_info = self.gym.step(action)
        outside_player.log_reward(last_info[1])
        action["building_locations"] = outside_player.buildSettlementAndRoadRound2(last_info[0])
        outside_player.log_reward(last_info[1])
        while not last_info[2]:
            last_info = self.gym.step(action)
            outside_player.log_reward(last_info[1])
            action = outside_player.move_thief(last_info[0])
            last_info = self.gym.step(action)
            outside_player.log_reward(last_info[0])
            action = outside_player.buy_road_or_settlement_or_city_or_development_card(last_info[0])

from RLPlayerController import RLPlayerController
if __name__ == "__main__":
    supervisor = GameSupervisor()
    supervisor.run_game(RLPlayerController())
