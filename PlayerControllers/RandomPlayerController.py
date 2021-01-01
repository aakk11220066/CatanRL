import random
from typing import Tuple, Dict

from CatanGame import Building
from CatanGame.Board import Board
from PlayerControllers.PlayerController import PlayerController
import Shared_Constants
from CatanGame.Tile import TileType

random.seed(Shared_Constants.RANDOM_SEED)


class RandomPlayerController(PlayerController):
    def __init__(self, player_num: Shared_Constants.PlayerNumber):
        super(RandomPlayerController, self).__init__(player_num=player_num)
    
    def get_desired_thief_location(self, observation: Tuple[Board, Dict[str, int]]):
        tiles = dict(
            (k, v) for k, v in observation[0].graph.nodes.items() if k[0] == "tile" and v['tile_type'] != TileType.OCEAN)
        '''for tile in tiles.values():
            if tile['thief']:
                pos = tile['position']
                tile['thief'] = False
                break'''
        pos = observation[0].thief_location
        assert (tiles[pos]["tile_type"])
        del tiles[pos]
        thief_new_position = ("tile", random.choice(list(tiles.values()))['position'])
        return {
            'action_type': Shared_Constants.ActionType.THIEF_PLACEMENT,
            'desired_thief_location': thief_new_position
        }

    '''def dropHalfCards(self):
        num_removed = self._get_number_of_resources() // 2
        for i in range(num_removed):
            d = dict((k, v) for k, v in self.available_resources.items() if v > 0)
            self.available_resources[random.choice(list(d))] -= 1'''

    def build_road_randomly(self,
                            observation: Tuple[Board, Dict[str, int]],
                            upcoming_settlement_location: Shared_Constants.PointCoordinate = None):
        valid_road_locations = observation[0].get_valid_road_locations(
            player=self.player_num,
            upcoming_settlement_location=upcoming_settlement_location
        )
        try:
            return random.choice(list(valid_road_locations))
        except(IndexError): # valid_road_locations is empty
            return None

    def build_settlement_randomly(self, observation: Tuple[Board, Dict[str, int]], start_of_game=False):
        valid_settlement_locations = observation[0].get_valid_settlement_locations(
            player=self.player_num,
            start_of_game=start_of_game
        )
        try:
            return random.choice(list(valid_settlement_locations))
        except(IndexError): # valid_settlement_locations is empty
            return None

    def build_city_randomly(self, observation: Tuple[Board, Dict[str, int]]):
        valid_city_locations = observation[0].get_valid_city_locations(player=self.player_num)
        try:
            return random.choice(list(valid_city_locations))
        except(IndexError): # valid_city_locations is empty
            return None

    def buy_development_card_randomly(self, observation: Tuple[Board, Dict[str, int]]):
        print('Complete buyDevelopmentCardRandomly')
        return None

    def buildSettlementAndRoadRound1(self, observation: Tuple[Board, Dict[str, int]]):
        desired_settlement = self.build_settlement_randomly(observation=observation, start_of_game=True)
        desired_road = self.build_road_randomly(observation=observation, upcoming_settlement_location=desired_settlement)
        return {
            "action_type": Shared_Constants.ActionType.FIRST_BUILDING,
            'building_locations': {
                "settlement": desired_settlement,
                "road": desired_road
            }
        }

    def buildSettlementAndRoadRound2(self, observation: Tuple[Board, Dict[str, int]], collect_resources_around_settlement: ()):
        desired_settlement = self.build_settlement_randomly(observation, start_of_game=True)
        collect_resources_around_settlement(settlement_location=desired_settlement)
        valid_road_locations = observation[0].get_valid_road_locations(
            player=self.player_num,
            upcoming_settlement_location=desired_settlement
        )
        valid_road_locations = filter(
            lambda road_endpoints:
                road_endpoints[0] == desired_settlement or
                road_endpoints[1] == desired_settlement,
            valid_road_locations
        )
        desired_road = random.choice(list(valid_road_locations))
        return {
            "action_type": Shared_Constants.ActionType.SECOND_BUILDING,
            'building_locations': {
                "settlement": desired_settlement,
                "road": desired_road
            }
        }

    def play_development_cards(self):
        print('Player', self.player_num, 'play_development_cards or do_nothing')
        # development_card_action = ['DO_NOTHING'].expend(self.development_cards)
        # print(random.choice(development_card_action))

    def trade_cards(self):
        print('Player', self.player_num, 'trade_cards or do_nothing')

    def purchase_buildings_and_cards(self, observation: Tuple[Board, Dict[str, int]]):
        available_resources = observation[1].copy()
        valid_purchases = ["road", "settlement", "city", "development_card"]
        valid_purchases = list(filter(
            lambda purchase: self._can_afford(available_resources=available_resources, purchase=purchase),
            valid_purchases
        ))
        valid_purchases.append("do_nothing")
        purchased_roads, purchased_settlements, purchased_cities, purchased_development_cards = ([], [], [], [])
        upcoming_purchase = random.choice(valid_purchases)
        while upcoming_purchase != "do_nothing":
            if upcoming_purchase == 'road':
                potential_road_purchase = self.build_road_randomly(observation=observation)
                if (potential_road_purchase):
                    purchased_roads.append(potential_road_purchase)
            elif upcoming_purchase == 'settlement':
                potential_settlement_purchase = self.build_settlement_randomly(observation=observation)
                if (potential_settlement_purchase):
                    purchased_settlements.append(potential_settlement_purchase)
            elif upcoming_purchase == 'city':
                potential_city_purchase = self.build_city_randomly(observation=observation)
                if potential_city_purchase:
                    purchased_cities.append(potential_city_purchase)
            elif upcoming_purchase == 'development_card':
                potential_development_card_purchase = self.buy_development_card_randomly(observation=observation)
                if potential_development_card_purchase:
                    purchased_development_cards.append(potential_development_card_purchase)

            for resource in Building.prices[upcoming_purchase]:
                available_resources[resource] -= Building.prices[upcoming_purchase][resource]

            valid_purchases.remove("do_nothing")
            valid_purchases = list(filter(
                lambda purchase: self._can_afford(available_resources=available_resources, purchase=purchase),
                valid_purchases
            ))
            valid_purchases.append("do_nothing")
            upcoming_purchase = random.choice(valid_purchases)
        return {
            "action_type": Shared_Constants.ActionType.BUILDINGS_PURCHASE,
            "purchases": {
                "roads": purchased_roads,
                "settlements": purchased_settlements,
                "cities": purchased_cities,
                "development_cards": purchased_development_cards
            }
        }

    def log_reward(self, reward: int):
        pass
