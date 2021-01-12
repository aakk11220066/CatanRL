from PlayerControllers.PlayerController import PlayerController
from collections import namedtuple
import random

from Shared_Constants import PlayerNumber, REPLAY_MEM_SIZE

Action = dict


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
    # All functions of controller should return Actions

    def __init__(self, player_num: PlayerNumber):
        super().__init__(player_num)
        self.memory = ReplayMemory(capacity=REPLAY_MEM_SIZE)

    def get_desired_thief_location(self, observation):
        raise NotImplementedError()

    def drop_half_cards(self, observation):
        raise NotImplementedError()  # TODO

    def build_settlement_and_road_round_1(self, observation):
        raise NotImplementedError()

    def build_settlement_and_road_round_2(self, observation) \
            -> Action:
        raise NotImplementedError()

    def buy_road_or_settlement_or_city_or_development_card(self, observation):
        raise NotImplementedError()

    def log_reward(self, reward: int):
        raise NotImplementedError()
