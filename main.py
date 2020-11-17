import networkx as nx
import matplotlib.pyplot as plt
import GUI
import Game


def main():
    game = Game.Game(boardSize=6)

    game.addSettlement(position=(1,1), player=1)
    game.addRoad(point1=(1,1), point2=(1,2), player=2)
    game.addCity(position=(3,3), player=3)

    # player number's binary representation sets his RGB value
    getPlayerColor = lambda player: (255 * (player % 2), 255 * ((player // 2) % 2), 255 * (player // 4))
    GUI.makeGraphical(game, getPlayerColor)


if __name__ == "__main__":
    main()
