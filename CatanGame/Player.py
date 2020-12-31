from typing import Dict, Union, List, Tuple

from CatanGame import Exceptions
import CatanGame.Board as Board
import CatanGame
from Shared_Constants import TileCoordinate, PointCoordinate, RoadPlacement, Resource


class Player:
    def __init__(self, player_number: int):
        self.player_number = player_number
        # resources to build first 2 settlements and 2 roads at beginning of game
        self.resources = {"sheep": 2, "wheat": 2, "wood": 4, "brick": 4, "ore": 0}
        self.victory_points = 0

        # ------ turn-controlling params to be controlled by gym ------
        self.desired_beginning_settlement_and_road_location: Tuple[PointCoordinate, RoadPlacement] = None
        self.desired_thief_location: TileCoordinate = None
        self.desired_shopping_list: Dict[Resource, List[Union[RoadPlacement, PointCoordinate]]] = None
        self.desired_trades_list: Dict[Resource, Resource] = None

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
    
    def valid_buy_road(self, game: CatanGame):
        valid_road_locations = game.board.get_valid_road_locations(player=self.player_number)
        if self.resources["wood"]>=1 and self.resources["brick"]>=1 and \
            bool(list(valid_road_locations)):
            return True
        return False
    
    def valid_buy_settlement(self, game: CatanGame):
        valid_settlement_locations = game.board.get_valid_settlement_locations(player=self.player_number)
        if self.resources["wood"]>=1 and self.resources["brick"]>=1 and \
            self.resources["sheep"]>=1 and self.resources["wheat"]>=1 and \
                bool(list(valid_settlement_locations)):
            return True
        return False

    def valid_buy_city(self, game: CatanGame):
        valid_city_locations = game.board.get_valid_city_locations(player=self.player_number)
        if self.resources["wheat"]>=2 and self.resources["ore"]>=3 and \
            bool(list(valid_city_locations)):
            return True
        return False

    def valid_buy_development_card(self):
        if self.resources["sheep"]>=1 and self.resources["wheat"]>=1 and self.resources["ore"]>=1:
            return True
        return False

    def valid_buy_actions(self, game: CatanGame):
        actions = []
        if self.valid_buy_road(game=game):
            actions.append('road')
        if self.valid_buy_settlement(game=game):
            actions.append('settlement')
        if self.valid_buy_city(game=game):
            actions.append('city')
        if self.valid_buy_development_card():
            actions.append('development_card')
        return actions

    def move_thief(self, board: Board):
        board.get_desired_thief_location(self.desired_thief_location)

    def _get_number_of_resources(self):
        return sum(list(self.resources.values()))

    def dropHalfCards(self):
        raise NotImplementedError()

    def buildSettlementAndRoadRound1(self, game: CatanGame):
        game.addSettlement(self.desired_beginning_settlement_and_road_location[0])
        game.addRoad(self.desired_beginning_settlement_and_road_location[1])

    def buildSettlementAndRoadRound2(self, game: CatanGame):
        self.buildSettlementAndRoadRound1(game)
        # TODO: collect resources

    # purposely unimplemented, merely a placeholder function for future development
    def trade_resources(self):  # ABSTRACT
        raise NotImplementedError()

    # purposely unimplemented, merely a placeholder function for future development
    def play_development_cards(self):  # ABSTRACT
        raise NotImplementedError()

    # purposely unimplemented, merely a placeholder function for future development
    def trade_cards(self):  # ABSTRACT
        raise NotImplementedError()

    def purchase_buildings_and_cards(self, game: CatanGame):
        for road in self.desired_shopping_list["roads"]:
            game.addRoad(road)
        for settlement in self.desired_shopping_list["settlements"]:
            game.addSettlement(settlement)
        for city in self.desired_shopping_list["cities"]:
            game.addCity(city)