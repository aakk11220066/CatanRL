from typing import Dict, Tuple, List

from CatanGame.Board import Board
from PlayerControllers.PlayerController import PlayerController, Action
from collections import namedtuple
import random

from PlayerControllers.RLPlayerControllerHelpers.NeuralNetworks import ActionTranslater, BoardTranslater, Q_net
from CatanGame.Shared_Constants import PlayerNumber, Coordinate, RANDOM_SEED
import PlayerControllers.RLPlayerControllerHelpers.Shared_Constants as settings

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
        self.memory = ReplayMemory(capacity=settings.REPLAY_MEM_SIZE)
        self.thief_loc_translater = ActionTranslater(
            in_dim=settings.THIEF_MANIFEST_DIM,
            hidden_dims=settings.THIEF_HIDDEN_DIMS,
            representation_dim=settings.ACTION_LATENT_DIM,
            dropout=settings.DROPOUT
        )
        self.trade_translater = ActionTranslater(
            in_dim=settings.TRADE_MANIFEST_DIM,
            hidden_dims=settings.TRADE_HIDDEN_DIMS,
            representation_dim=settings.ACTION_LATENT_DIM,
            dropout=settings.DROPOUT
        )
        self.purchase_translater = ActionTranslater(
            in_dim=settings.PURCHASE_MANIFEST_DIM,
            hidden_dims=settings.PURCHASE_HIDDEN_DIMS,
            representation_dim=settings.ACTION_LATENT_DIM,
            dropout=settings.DROPOUT
        )
        self.board_translater = BoardTranslater(
            GCN_hidden_channels=settings.GCN_HIDDEN_CHANNELS,
            perceptron_hidden_dims=[settings.PERCEPTRON_DIM_COEFF*board_size],
            board_representation_dim=settings.BOARD_LATENT_DIM_COEFF*board_size,
            dropout=settings.DROPOUT
        )
        num_resource_classes = 5
        self.qnet = Q_net( # in_dim includes 1 dimension determining type of action
            in_dim=settings.BOARD_LATENT_DIM_COEFF*board_size + num_resource_classes + settings.ACTION_LATENT_DIM + 1,
            hidden_dims = settings.QNET_HIDDEN_DIMS
        )

    def get_desired_thief_location(self, observation: Tuple[Board, Dict]) -> Action:
        def _construct_Qnet_input(self, board: Board, resources: Dict, thief_location: Coordinate):
            board_representation = self.board_translater(torch_geometric.utils.convert.from_networkx(board.graph))
            resources = list(resources.values())
            thief_location = self.thief_loc_translater(thief_location)
            # TODO: append 0 representing thief_placement action, concatenate
            raise NotImplementedError()

        board, resources = observation
        _, possible_thief_locations = zip(observation[0].get_valid_thief_locations())
        thief_location_scores = list(map(
            lambda thief_loc: self.qnet(
                _construct_Qnet_input(
                    self,
                    board=observation[0],
                    thief_location=thief_loc,
                    resources=observation[1]
                ).item()
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
        def _construct_Qnet_input(self, board: Board, resources: Dict, purchase_info=(0,)*5):
            board_representation = self.board_translater(torch_geometric.utils.convert.from_networkx(board.graph))
            resources = list(resources.values())
            purchase_representation = self.purchase_translater(purchase_info)
            # TODO: append 1 representing purchase action
            raise NotImplementedError()

        board, resources = observation
        _, purchase_options = zip(observation[0].)
        purchase_scores = list(map(
            lambda purchase_option: self.qnet(
                _construct_Qnet_input(
                    self,
                    board=observation[0],
                    purchase_info=purchase_option,
                    resources=observation[1]
                ).item()
            ),
            purchase_options
        ))
        assert purchase_options
        if random.random() > self.greediness:
            return max(range(len(purchase_scores)), key=lambda idx: purchase_options[idx])
        return random.choice(purchase_options) # FIXME: should be multinomially distributed?

    def get_desired_trade(self, observation) -> Action:
        def _construct_Qnet_input(self, board: Board, resources: Dict, trade_info):
            board_representation = self.board_translater(torch_geometric.utils.convert.from_networkx(board.graph))
            resources = list(resources.values())
            trade_representation = self.trade_translater(trade_info)
            # TODO: append 2 representing trade action
            raise NotImplementedError()

        board, resources = observation
        _, trade_options = zip(observation[0].)
        trade_scores = list(map(
            lambda trade_option: self.qnet(
                _construct_Qnet_input(
                    self,
                    board=observation[0],
                    trade_info=trade_option,
                    resources=observation[1]
                ).item()
            ),
            trade_options
        ))
        assert trade_options
        if random.random() > self.greediness:
            return max(range(len(trade_scores)), key=lambda idx: trade_options[idx])
        return random.choice(trade_options)  # FIXME: should be multinomially distributed?

    def log_transition(self, observation, action, reward: int, next_observation):
        self.memory.push(observation, action, reward, next_observation)
