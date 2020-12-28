from Player import Player
from Board import Board
from CatanGame import CatanGame
from abc import ABC, abstractmethod


class RLPlayer(Player):
    @abstractmethod
    def move_thief(self, board: Board):
        raise NotImplementedError()

    # TODO: standardize var names to snake_case
    @abstractmethod
    def dropHalfCards(self):
        raise NotImplementedError() # TODO

    @abstractmethod
    def buildSettlementAndRoadRound1(self, game: CatanGame):
        raise NotImplementedError()

    @abstractmethod
    def buildSettlementAndRoadRound2(self, game: CatanGame):
        raise NotImplementedError()

    @abstractmethod
    def buy_road_or_settlement_or_city_or_development_card(self, game: CatanGame):
        raise NotImplementedError()
