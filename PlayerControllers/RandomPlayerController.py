import itertools
import random
from typing import Tuple, Dict

from CatanGame import Building, Shared_Constants
from CatanGame.Board import Board
from PlayerControllers.PlayerController import PlayerController
from PlayerControllers.RLPlayerControllerHelpers.Shared_Constants import ActionType

random.seed(Shared_Constants.RANDOM_SEED)


class RandomPlayerController(PlayerController):
    def __init__(self, player_num: Shared_Constants.PlayerNumber):
        super(RandomPlayerController, self).__init__(player_num=player_num)

    '''def drop_half_cards(self):
        num_removed = self._get_number_of_resources() // 2
        for i in range(num_removed):
            d = dict((k, v) for k, v in self.available_resources.items() if v > 0)
            self.available_resources[random.choice(list(d))] -= 1'''

    def _build_road_randomly(self,
                             observation: Tuple[Board, Dict[str, int]],
                             upcoming_settlement_location: Shared_Constants.PointCoordinate = None):
        valid_road_locations = observation[0].get_valid_road_locations(
            player=self.player_num,
            upcoming_settlement_location=upcoming_settlement_location
        )
        try:
            return random.choice(list(valid_road_locations))
        except IndexError:  # valid_road_locations is empty
            return None

    def _build_settlement_randomly(self, observation: Tuple[Board, Dict[str, int]], start_of_game=False):
        valid_settlement_locations = observation[0].get_valid_settlement_locations(
            player=self.player_num,
            start_of_game=start_of_game
        )
        try:
            return random.choice(list(valid_settlement_locations))
        except IndexError:  # valid_settlement_locations is empty
            # print(f"Player {self.player_num} could not find anywhere to build a settlement!")
            return None

    def _build_city_randomly(self, observation: Tuple[Board, Dict[str, int]]):
        valid_city_locations = observation[0].get_valid_city_locations(player=self.player_num)
        try:
            return random.choice(list(valid_city_locations))
        except IndexError:  # valid_city_locations is empty
            return None

    @staticmethod
    def _buy_development_card_randomly(observation: Tuple[Board, Dict[str, int]]):
        print('Decided to buy development card (not implemented yet)')
        return None

    def get_desired_thief_location(self, observation: Tuple[Board, Dict[str, int]]):
        tiles = observation[0].get_valid_thief_locations()
        thief_new_position = ("tile", random.choice(list(tiles.values()))['position'])
        return {
            'action_type': ActionType.THIEF_PLACEMENT,
            'desired_thief_location': thief_new_position
        }

    def build_settlement_and_road_round_1(self, observation: Tuple[Board, Dict[str, int]]):
        desired_settlement = self._build_settlement_randomly(observation=observation, start_of_game=True)
        desired_road = self._build_road_randomly(observation=observation,
                                                 upcoming_settlement_location=desired_settlement)
        return {
            "action_type": ActionType.FIRST_BUILDING,
            'building_locations': {
                "settlement": desired_settlement,
                "road": desired_road
            }
        }

    def build_settlement_and_road_round_2(self, observation: Tuple[Board, Dict[str, int]]):
        desired_settlement = self._build_settlement_randomly(observation, start_of_game=True)
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
            "action_type": ActionType.SECOND_BUILDING,
            'building_locations': {
                "settlement": desired_settlement,
                "road": desired_road
            }
        }

    '''def play_development_cards(self):
        print('Player', self.player_num, 'play_development_cards or do_nothing')
        # development_card_action = ['DO_NOTHING'].expend(self.development_cards)
        # print(random.choice(development_card_action))
    '''

    def get_desired_trade(self, observation):
        available_resources = observation[1].copy()
        desired_trades = []
        while True:
            valid_trades = self._get_valid_trades(available_resources=available_resources)
            valid_trades = list(itertools.product(*valid_trades))
            trade_from_resource, trade_to_resource = random.choice(valid_trades)
            if trade_from_resource == trade_to_resource:
                continue
            if trade_from_resource == "do_nothing":
                break
            desired_trades.append((trade_from_resource, trade_to_resource))
            available_resources[trade_from_resource] -= Shared_Constants.BANK_TRADE_PRICE
        return {
            "action_type": ActionType.TRADE_RESOURCES,
            "desired_trades": desired_trades
        }

    def purchase_buildings_and_cards(self, observation: Tuple[Board, Dict[str, int]]):
        available_resources = observation[1].copy()
        valid_purchases = self._get_valid_purchases(available_resources=available_resources)
        purchased_roads, purchased_settlements, purchased_cities, purchased_development_cards = ([], [], [], [])
        upcoming_purchase = random.choice(valid_purchases)
        while upcoming_purchase != "do_nothing":
            if upcoming_purchase == 'road':
                potential_road_purchase = self._build_road_randomly(observation=observation)
                if potential_road_purchase and potential_road_purchase not in purchased_roads:
                    purchased_roads.append(potential_road_purchase)
            elif upcoming_purchase == 'settlement':
                potential_settlement_purchase = self._build_settlement_randomly(observation=observation)
                if potential_settlement_purchase and potential_settlement_purchase not in purchased_settlements:
                    purchased_settlements.append(potential_settlement_purchase)
            elif upcoming_purchase == 'city':
                potential_city_purchase = self._build_city_randomly(observation=observation)
                if potential_city_purchase and potential_city_purchase not in purchased_cities:
                    purchased_cities.append(potential_city_purchase)
            elif upcoming_purchase == 'development_card':
                potential_development_card_purchase = self._buy_development_card_randomly(observation=observation)
                if potential_development_card_purchase and \
                        potential_development_card_purchase not in purchased_development_cards:
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
            "action_type": ActionType.BUILDINGS_PURCHASE,
            "purchases": {
                "roads": purchased_roads,
                "settlements": purchased_settlements,
                "cities": purchased_cities,
                "development_cards": purchased_development_cards
            }
        }

    def log_transition(self, observation, action, reward: int, next_observation):
        pass
