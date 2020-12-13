import random
import Board
from Player import Player
from Building import BuildingTypes, is_valid_settlement_position, _edge_location_available
import Shared_Constants
import Game
from Tile import TileType

random.seed(Shared_Constants.RANDOM_SEED)
class RandomPlayer(Player):
    # only called if dice rolled 7
    def move_thief(self, board: Board):
        tiles = dict((k, v) for k, v in board.graph.nodes.items() if k[0] == "tile" and v['tile_type']!=TileType.OCEAN)
        for tile in tiles.values():
            if tile['thief'] == True:
                pos = tile['position']
                tile['thief'] = False
                break
        del tiles[('tile',pos)]
        thief_new_position = random.choice(list(tiles.values()))['position']
        board._add_thief(thief_new_position) #TODO the thief duplicate to another location and take random resource from random player
        print("The thief moved to",thief_new_position)

    def dropHalfCards(self):
        num_removed = self._get_number_of_resources() // 2
        for i in range(num_removed):
            d = dict((k, v) for k, v in self.resources.items() if v > 0)
            self.resources[random.choice(list(d))] -= 1

    def buildRoadRandomly(self,game: Game):
        valid_road_locations = game.board.get_valid_road_locations(player=self.player_number)
        road_location = random.choice(list(valid_road_locations))
        game.addRoad(point1=road_location[0][1], point2=road_location[1][1], player_num=self.player_number) 

    def buildSettlementRandomly(self,game: Game,start_of_game=False):
        valid_settlement_locations = game.board.get_valid_settlement_locations(player=self.player_number, start_of_game=start_of_game)    
        settlement_location = random.choice(list(valid_settlement_locations))
        game.addSettlement(position=settlement_location[1], player_num=self.player_number, start_of_game=start_of_game)
        return settlement_location

    def buildCityRandomly(self,game: Game):
        print('Complete buildCityRandomly')
        # valid_settlement_locations = game.board.get_valid_settlement_locations(player=self.player_number, start_of_game=start_of_game)    
        # settlement_location = random.choice(list(valid_settlement_locations))
        # game.addSettlement(position=settlement_location[1], player_num=self.player_number, start_of_game=start_of_game)        

    def buyDevelopmentCardRandomly(self,game: Game):
        print('Complete buyDevelopmentCardRandomly')

    def buildSettlementAndRoadRound1(self, game: Game):
        self.buildSettlementRandomly(game=game,start_of_game=True)
        self.buildRoadRandomly(game=game)

    def buildSettlementAndRoadRound2(self, game: Game):
        settlement_location = self.buildSettlementRandomly(game=game,start_of_game=True)
        game._collect_surrounding_resources(settlement_location=settlement_location[1]) 
        valid_road_locations = game.board.get_valid_road_locations(player=self.player_number) # TODO 
        road_location = random.choice(list(valid_road_locations))
        game.addRoad(point1=road_location[0][1], point2=road_location[1][1], player_num=self.player_number) 
    
    def purchase_buildings_and_cards(self):
        pass

    def play_development_cards(self):
        print('Player',self.player_number,'play_development_cards or do_nothing')
        # development_card_action = ['DO_NOTHING'].expend(self.development_cards)
        # print(random.choice(development_card_action))

    def trade_cards(self):
        print('Player',self.player_number,'trade_cards or do_nothing')

    def buy_road_or_settlement_or_city_or_development_card(self,game: Game):
        actions = self.valid_buy_actions(game=game)
        actions.append('do_nothing')
        action = random.choice(actions)
        if action == 'do_nothing':
            print('Player',self.player_number,"do nothing on the buy_road_or_settlement_or_city_or_development_card part")
        elif action == 'road':
            self.buildRoadRandomly(game=game)
        elif action == 'settlement':
            self.buildSettlementRandomly(game=game)
        elif action == 'city':
            self.buildCityRandomly(game=game)
        elif action == 'development_card':
            self.buyDevelopmentCardRandomly(game=game)