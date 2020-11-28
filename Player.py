import Exceptions
import random
import Board

class Player:
    def __init__(self):
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

    def move_thief(self, board: Board): # should be abstract method
        tiles = dict((k, v) for k, v in board.graph.nodes.items() if k[0] == "tile")
        for tile in tiles.values():
            if tile['thief'] == True:
                pos = tile['position']
        del tiles[('tile',pos)]
        board._add_thief(random.choice(list(tiles.values()))['position'])

    def get_number_of_resources(self): 
        return sum(list(self.resources.values()))
        
    def cutting_cards_in_half(self): # should be abstract method
        num_removed = self.get_number_of_resources()//2
        for i in range(num_removed):
            d = dict((k, v) for k, v in self.resources.items() if v > 0)
            self.resources[random.choice(list(d))] -= 1
