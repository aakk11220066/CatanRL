from Game import Game
from GUI import GUI
import gym
from gym import spaces

class Game_GymWrapper(gym.env):
    metadata = {'render.modes': ['human']}

    def __init__(self, game: Game, player_num, human_viewable = True):
        super(Game_GymWrapper, self).__init__()

        self.observation_space = spaces.Dict({
            "turn phase": spaces.Discrete(2) # 2 phases currently - dice rolling[1], building[1]
            # "development cards": spaces.Discrete(),  # Future implementation
            "dice result": spaces.Discrete(12),
            "resources": spaces.Dict({ # TODO: should be unbounded but discrete
                "sheep": spaces.Discrete(),
                "wheat": spaces.Discrete(),
                "wood": spaces.Discrete(),
                "brick": spaces.Discrete(),
                "ore": spaces.Discrete()
            }),
            "board": spaces.Tuple(()) # TODO: should get result from PyGeometric
        })

        self.action_space = spaces.Dict({
            # "play_development_cards": spaces.Discrete(),  # Future implementation

            # dice result, coordinates of where to move the thief (should be ignored if dice result != 7)
            "rollDice": spaces.MultiDiscrete([12, self.game.board.boardSize, self.game.board.boardSize]),

            # "trade_cards": spaces.Discrete(),  # Future implementation

            "buy_road_or_settlement_or_city_or_development_card": spaces.() # TODO: should be variable length
        })

        self.game = game
        self.player_num = player_num
        self.prev_victory_points = 0
        if human_viewable:
            self.render_request = False
            def get_render_request():
                result = self.render_request
                self.render_request = False
                return result
            self.gui = GUI(self.game, render_request_status=get_render_request)
            self.gui.start()

    def step(self, action):
        # TODO: perform action, define observation


        reward = self.game.players[self.player_num - 1].victory_points - self.prev_victory_points
        self.prev_victory_points = self.game.players[self.player_num - 1].victory_points

        done = self.game.endGame()

        info = None

        return observation, reward, done, info

    def reset(self):


    def render(self, mode='human', close=False):
        self.render_request = True