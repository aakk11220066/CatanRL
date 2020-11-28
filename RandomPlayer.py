import random
import Board
from Player import Player


class RandomPlayer(Player):
    # only called if dice rolled 7
    def move_thief(self, board: Board):
        tiles = dict((k, v) for k, v in board.graph.nodes.items() if k[0] == "tile")
        for tile in tiles.values():
            if tile['thief'] == True:
                pos = tile['position']
        del tiles[('tile',pos)]
        random.choice(list(tiles.values()))['thief'] = True
    # purposely unimplemented, merely a placeholder function for future development
    def trade_resources(self):
        pass

    # purchasing development cards is currently disabled (not implemented)
    def purchases_buildings_and_cards(self): # TODO
        raise NotImplementedError()

    # purposely unimplemented, merely a placeholder function for future development
    def play_development_cards(self):
        pass

    def cutting_cards_in_half(self):
        num_removed = self.get_number_of_resources()//2
        for i in range(num_removed):
            d = dict((k, v) for k, v in self.resources.items() if v > 0)
            self.resources[random.choice(list(d))] -= 1

