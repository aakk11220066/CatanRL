from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from CatanGame import Shared_Constants
from CatanGame.Shared_Constants import PlayerNumber
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

    def _get_valid_purchases(self, available_resources: Dict[str, int]):
        valid_purchases = ["road", "settlement", "city", "development_card"]
        valid_purchases = list(filter(
            lambda purchase: self._can_afford(available_resources=available_resources, purchase=purchase),
            valid_purchases
        ))
        valid_purchases.append("do_nothing")
        return valid_purchases

    @staticmethod
    def _get_valid_trades(available_resources: Dict[str, int]) -> Tuple[List[str], List[str]]:
        trade_from = list(filter(
            lambda resource: available_resources[resource] >= Shared_Constants.BANK_TRADE_PRICE,
            available_resources
        )) + ["do_nothing"]
        trade_to = list(available_resources.keys())
        return trade_from, trade_to

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
    def log_transition(self, observation, action: Action, reward: int, next_observation):
        raise NotImplementedError()
