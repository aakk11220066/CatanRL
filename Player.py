import Exceptions
import random
import Board
import Game
from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, player_number: int):
        self.player_number = player_number
        # resources to build first 2 settlements and 2 roads at beginning of game
        self.resources = {"sheep": 2, "wheat": 2, "wood": 4, "brick": 4, "ore": 0}
        self.victory_points = 0

    def spend_resources(self, sheep=0, wheat=0, wood=0, brick=0, ore=0):
        if self.resources["sheep"] < sheep \
                or self.resources["wheat"] < wheat \
                or self.resources["wood"] < wood \
                or self.resources["brick"] < brick \
                or self.resources["ore"] < ore:
            raise Exceptions.InsufficientResourcesException()

        self.resources["sheep"] -= sheep
        self.resources["wheat"] -= wheat
        self.resources["wood"] -= wood
        self.resources["brick"] -= brick
        self.resources["ore"] -= ore
    
    def valid_buy_road(self, game: Game):
        valid_road_locations = game.board.get_valid_road_locations(player=self.player_number)
        if self.resources["wood"]>=1 and self.resources["brick"]>=1 and \
            bool(valid_road_locations):
            return True
        return False
    
    def valid_buy_settlement(self, game: Game):
        valid_settlement_locations = game.board.get_valid_settlement_locations(player=self.player_number)
        if self.resources["wood"]>=1 and self.resources["brick"]>=1 and \
            self.resources["sheep"]>=1 and self.resources["wheat"]>=1 and \
                bool(valid_settlement_locations):
            return True
        return False

    def valid_buy_city(self):
        if self.resources["wheat"]>=2 and self.resources["ore"]>=3:
            return True
        return False

    def valid_buy_development_card(self):
        if self.resources["sheep"]>=1 and self.resources["wheat"]>=1 and self.resources["ore"]>=1:
            return True
        return False

    def valid_buy_actions(self, game: Game):
        actions = []
        if self.valid_buy_road(game=game):
            actions.append('road')
        if self.valid_buy_settlement(game=game):
            actions.append('settlement')
        if self.valid_buy_city():
            actions.append('city')
        if self.valid_buy_development_card():
            actions.append('development_card')
        return actions

    @abstractmethod
    def move_thief(self, board: Board):
        raise NotImplementedError()

    def _get_number_of_resources(self):
        return sum(list(self.resources.values()))
        
    @abstractmethod    
    def dropHalfCards(self):
        raise NotImplementedError()

    @abstractmethod
    def buildSettlementAndRoadRound1(self, board: Board):
        raise NotImplementedError()

    @abstractmethod
    def buildSettlementAndRoadRound2(self, board: Board):
        raise NotImplementedError()    

    # purchasing development cards is currently disabled (not implemented)
    @abstractmethod
    def purchase_buildings_and_cards(self):
        raise NotImplementedError()

    # purposely unimplemented, merely a placeholder function for future development
    def trade_resources(self):  # ABSTRACT
        raise NotImplementedError()

    # purposely unimplemented, merely a placeholder function for future development
    @abstractmethod
    def play_development_cards(self):  # ABSTRACT
        raise NotImplementedError()

    # purposely unimplemented, merely a placeholder function for future development
    @abstractmethod
    def trade_cards(self):  # ABSTRACT
        raise NotImplementedError()

    @abstractmethod
    def buy_road_or_settlement_or_city_or_development_card(self): 
        raise NotImplementedError()


