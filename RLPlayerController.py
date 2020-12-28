from Board import Board
from PlayerController import PlayerController


class RLPlayerController(PlayerController):
    def move_thief(self, observation):
        raise NotImplementedError()

    def dropHalfCards(self, observation):
        raise NotImplementedError() # TODO

    def buildSettlementAndRoadRound1(self, observation):
        raise NotImplementedError()

    def buildSettlementAndRoadRound2(self, observation):
        raise NotImplementedError()

    def buy_road_or_settlement_or_city_or_development_card(self, observation):
        raise NotImplementedError()

    def log_reward(self, reward: int):
        raise NotImplementedError()
