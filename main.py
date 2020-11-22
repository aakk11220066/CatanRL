import networkx as nx
import matplotlib.pyplot as plt
import GUI
import Game


def main():
    game = Game.Game(board_size=3)

    game.addSettlement(position=(1,1), player_num=1, start_of_game=True)
    game.addRoad(point1=(1,1), point2=(1,2), player_num=1)
    game.addSettlement(position=(3, 3), player_num=3, start_of_game=True)
    game.players[3 - 1].resources["ore"] += 3
    game.players[3 - 1].resources["wheat"] += 2
    game.addCity(position=(3,3), player_num=3)

    # player_num number's binary representation sets his RGB value
    getPlayerColor = lambda player: (255 * (player % 2), 255 * ((player // 2) % 2), 255 * (player // 4))
    GUI.makeGraphical(game, getPlayerColor)


if __name__ == "__main__":
    main()
