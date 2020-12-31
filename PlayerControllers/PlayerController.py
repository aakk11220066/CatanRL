from CatanGame.Board import Board
from abc import ABC, abstractmethod

from Shared_Constants import PlayerNumber
from GymInterface import GymInterface
from CatanGame.CatanGame import CatanGame


class PlayerController(ABC):
    def __init__(self, player_num: PlayerNumber, game: CatanGame):
        self.player_num = player_num

    @abstractmethod
    def get_desired_thief_location(self, observation):
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
