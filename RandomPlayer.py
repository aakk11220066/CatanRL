from Player import Player


class RandomPlayer(Player):
    # only called if dice rolled 7
    def move_thief(self): # TODO
        raise NotImplementedError()

    # purposely unimplemented, merely a placeholder function for future development
    def trade_resources(self):
        pass

    # purchasing development cards is currently disabled (not implemented)
    def purchases_buildings_and_cards(self): # TODO
        raise NotImplementedError()

    # purposely unimplemented, merely a placeholder function for future development
    def play_development_cards(self):
        pass
