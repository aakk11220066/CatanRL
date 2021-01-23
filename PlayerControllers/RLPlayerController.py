import itertools
from typing import Dict, Tuple
import torch
import torch_geometric

from CatanGame.Board import Board
from PlayerControllers.PlayerController import PlayerController, Action
from PlayerControllers.RLPlayerControllerHelpers.Shared_Constants import ActionType
from collections import namedtuple
import random

from PlayerControllers.RLPlayerControllerHelpers.NeuralNetworks import ActionTranslator, BoardTranslator, Q_net
from CatanGame.Shared_Constants import PlayerNumber, RANDOM_SEED
import PlayerControllers.RLPlayerControllerHelpers.Shared_Constants as Settings

random.seed(RANDOM_SEED)

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class RLPlayerController(PlayerController):
    def __init__(self, player_num: PlayerNumber, board_size, greediness):
        """
        :param player_num:
        :param board_size:
        :param greediness: probability of selecting best action vs. exploring (1 is deterministic, 0 is fully random)
        """
        super().__init__(player_num)
        assert (0 <= greediness <= 1)
        self.greediness = greediness
        self.memory = ReplayMemory(capacity=Settings.REPLAY_MEM_SIZE)
        self.thief_loc_translator = ActionTranslator(
            in_dim=Settings.THIEF_MANIFEST_DIM,
            hidden_dims=Settings.THIEF_HIDDEN_DIMS,
            representation_dim=Settings.ACTION_LATENT_DIM,
            dropout=Settings.DROPOUT
        )
        self.trade_translator = ActionTranslator(
            in_dim=Settings.TRADE_MANIFEST_DIM,
            hidden_dims=Settings.TRADE_HIDDEN_DIMS,
            representation_dim=Settings.ACTION_LATENT_DIM,
            dropout=Settings.DROPOUT
        )
        self.purchase_translator = ActionTranslator(
            in_dim=Settings.PURCHASE_MANIFEST_DIM,
            hidden_dims=Settings.PURCHASE_HIDDEN_DIMS,
            representation_dim=Settings.ACTION_LATENT_DIM,
            dropout=Settings.DROPOUT
        )
        self.board_translator = BoardTranslator(
            GCN_hidden_channels=Settings.GCN_HIDDEN_CHANNELS,
            perceptron_hidden_dims=[Settings.PERCEPTRON_DIM_COEFF * board_size],
            board_representation_dim=Settings.BOARD_LATENT_DIM_COEFF * board_size,
            dropout=Settings.DROPOUT
        )
        num_resource_classes = 5
        self.qnet = Q_net( # in_dim includes 1 dimension determining type of action
            in_dim=Settings.BOARD_LATENT_DIM_COEFF * board_size + num_resource_classes + Settings.ACTION_LATENT_DIM + 1,
            hidden_dims = Settings.QNET_HIDDEN_DIMS
        )

    def _construct_Qnet_input(self, board: Board, resources: Dict, action_data, action_type: int) \
            -> Tuple[torch_geometric.data.Data, torch.Tensor]:
        board_representation = self.board_translator(torch_geometric.utils.convert.from_networkx(board.graph))
        resources = list(resources.values())

        translators = {
            Settings.THIEF_MOVEMENT_REP: self.thief_loc_translator,
            Settings.TRADE_REP: self.trade_translator,
            Settings.PURCHASE_REP: self.purchase_translator
        }
        action_data = translators[action_type](action_data)

        return board_representation, \
               torch.cat((torch.tensor(resources), action_data, torch.unsqueeze(torch.tensor(action_type), dim=0)))

    def get_desired_thief_location(self, observation: Tuple[Board, Dict]) -> Action:
        board, resources = observation
        _, possible_thief_locations = zip(board.get_valid_thief_locations())
        thief_location_scores = list(map(
            lambda thief_loc: self.qnet(
                self._construct_Qnet_input(
                    board=board,
                    resources=resources,
                    action_data=thief_loc,
                    action_type=Settings.THIEF_MOVEMENT_REP
                )
            ),
            possible_thief_locations
        ))
        assert possible_thief_locations
        if random.random() > self.greediness:
            return max(range(len(thief_location_scores)), key=lambda idx: possible_thief_locations[idx])
        return random.choice(possible_thief_locations) # FIXME: should be multinomially distributed?

    def build_settlement_and_road_round_1(self, observation) -> Action:
        raise NotImplementedError()

    def build_settlement_and_road_round_2(self, observation) \
            -> Action:
        raise NotImplementedError()

    def purchase_buildings_and_cards(self, observation) -> Action:
        board, resources = observation
        purchase_options = self._get_valid_purchases(available_resources=resources.copy())
        purchase_loc_fns = {
            "road": board.get_valid_road_locations(player=self.player_num),
            "settlement": board.get_valid_settlement_locations(player=self.player_num),
            "city": board.get_valid_city_locations(player=self.player_num),
            "development_card": None,
            "do_nothing": None
        }
        purchase_options = itertools.chain(map(lambda purchase: purchase_loc_fns[purchase], purchase_options))
        purchase_scores = list(map(
            lambda purchase_option: self.qnet(
                self._construct_Qnet_input(
                    board=board,
                    resources=resources,
                    action_data=purchase_option,
                    action_type=Settings.PURCHASE_REP
                )
            ),
            purchase_options
        ))
        assert purchase_scores
        if random.random() < self.greediness:
            return purchase_options[max(range(len(purchase_options)), key=lambda idx: purchase_options[idx])]
        return random.choice(purchase_options)  # FIXME: should be multinomially distributed?
        return {
            "action_type": ActionType.BUILDINGS_PURCHASE,
            "purchases": {
                "roads": purchased_roads,
                "settlements": purchased_settlements,
                "cities": purchased_cities,
                "development_cards": purchased_development_cards
            }
        }

    def get_desired_trade(self, observation) -> Action:
        board, resources = observation
        trade_options = self._get_valid_trades(resources.copy())
        trade_scores = list(map(
            lambda trade_option: self.qnet(
                self._construct_Qnet_input(
                    board=board,
                    resources=resources,
                    action_data=trade_option,
                    action_type=Settings.TRADE_REP
                )
            ),
            trade_options
        ))
        assert trade_options
        if random.random() > self.greediness:
            return max(range(len(trade_scores)), key=lambda idx: trade_options[idx])
        return random.choice(trade_options)  # FIXME: should be multinomially distributed?

    def log_transition(self, observation, action, reward: int, next_observation):
        self.memory.push(observation, action, reward, next_observation)
