from Board import Board
from abc import ABC, abstractmethod


class PlayerController(ABC):
    @abstractmethod
    def move_thief(self, observation):
        raise NotImplementedError()

    @abstractmethod
    def dropHalfCards(self, observation):
        raise NotImplementedError()

    @abstractmethod
    def buildSettlementAndRoadRound1(self, observation):
        raise NotImplementedError()

    @abstractmethod
    def buildSettlementAndRoadRound2(self, observation):
        raise NotImplementedError()

    @abstractmethod
    def buy_road_or_settlement_or_city_or_development_card(self, observation):
        raise NotImplementedError()

    @abstractmethod
    def log_reward(self, reward: int):
        raise NotImplementedError()
