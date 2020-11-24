from Player import Player
from Board import Board


class RandomPlayer(Player):
    # only called if dice rolled 7
    def move_thief(self, board: Board): # TODO
        raise NotImplementedError()

    # purposely unimplemented, merely a placeholder function for future development
    def trade_resources(self, board: Board):
        pass

    # purchasing development cards is currently disabled (not implemented)
    def purchase_buildings_and_cards(self, board: Board): # TODO
        raise NotImplementedError()

    # purposely unimplemented, merely a placeholder function for future development
    def play_development_cards(self, board: Board):
        pass
