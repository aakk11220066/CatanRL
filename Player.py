import Exceptions
import random
import Board
from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self):
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

    @abstractmethod
    def move_thief(self, board: Board): # TODO: AKIVA: delete this method.  Should be implemented in subclasses, not here
        tiles = dict((k, v) for k, v in board.graph.nodes.items() if k[0] == "tile")
        for tile in tiles.values():
            if tile['thief'] == True:
                pos = tile['position']
        del tiles[('tile',pos)]
        board._add_thief(random.choice(list(tiles.values()))['position'])

    def _get_number_of_resources(self):
        return sum(list(self.resources.values()))
        
    def dropHalfCards(self):
        num_removed = self._get_number_of_resources() // 2
        for i in range(num_removed):
            d = dict((k, v) for k, v in self.resources.items() if v > 0)
            self.resources[random.choice(list(d))] -= 1

    # purchasing development cards is currently disabled (not implemented)
    @abstractmethod
    def purchase_buildings_and_cards(self):
        raise NotImplementedError()

    # purposely unimplemented, merely a placeholder function for future development
    def trade_resources(self): # ABSTRACT
        raise NotImplementedError()

    # purposely unimplemented, merely a placeholder function for future development
    def play_development_cards(self): # ABSTRACT
        raise NotImplementedError()
