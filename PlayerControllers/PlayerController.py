from abc import ABC, abstractmethod
from typing import Dict

from Shared_Constants import PlayerNumber
from CatanGame.Building import prices
Action = Dict


class PlayerController(ABC):
    def __init__(self, player_num: PlayerNumber):
        self.player_num = player_num

    def _can_afford(self, available_resources: Dict[str, int], purchase: str):
        return all(
            available_resources[resource] >= prices[purchase][resource]
            for resource in prices[purchase]
        )

    @abstractmethod
    def get_desired_thief_location(self, observation) -> Action:
        raise NotImplementedError()

    @abstractmethod
    def build_settlement_and_road_round_1(self, observation) -> Action:
        raise NotImplementedError()

    @abstractmethod
    def build_settlement_and_road_round_2(self, observation) \
            -> Action:
        raise NotImplementedError()

    @abstractmethod
    def get_desired_trade(self, observation) -> Action:
        raise NotImplementedError()

    @abstractmethod
    def purchase_buildings_and_cards(self, observation) -> Action:
        raise NotImplementedError()

    @abstractmethod
    def log_reward(self, reward: int):
        raise NotImplementedError()
