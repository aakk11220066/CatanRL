import Exceptions


class Player:
    def __init__(self):
        self.resources = {"sheep": 2, "wheat": 2, "wood": 4, "brick": 4, "ore": 0}
        self.victory_points = 0

    def spend_resources(self, sheep=0, wheat=0, wood=0, brick=0, ore=0):
        if self.resources["sheep"] < sheep \
            or self.resources["wheat"] < wheat \
            or self.resources["wood"] < wood \
            or self.resources["brick"] < brick \
            or self.resources["ore"] < ore:

            raise Exceptions.InsufficientResourcesException()

        self.resources["sheep"] -= sheep
        self.resources["wheat"] -= wheat
        self.resources["wood"] -= wood
        self.resources["brick"] -= brick
        self.resources["ore"] -= ore
