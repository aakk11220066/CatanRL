from PlayerControllers.PlayerController import PlayerController

Action = dict

# All functions of controller should return Actions
class RLPlayerController(PlayerController):
    def get_desired_thief_location(self, observation):
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
