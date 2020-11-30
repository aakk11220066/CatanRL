import networkx as nx
import matplotlib.pyplot as plt
import random
from GUI import GUI
import Game


def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list


def makeOrderPlayerGame(num_of_players, num_of_bots):
    players = [x + 1 for x in list(range(num_of_players))]
    len = num_of_players
    order_player_game = []
    for i in range(num_of_players):
        player = random.choice(players[:len])
        if player <= num_of_players - num_of_bots:
            order_player_game.append((player, "HUMAN"))
        else:
            order_player_game.append((player, "BOT"))
        swapPositions(players, player - 1, len - 1)
        len -= 1
    return order_player_game


def main():
    # Defined board size (scale)
    board_size = int(input("Please select the game board size (2,3,4...): "))
    while board_size < 2:
        board_size = int(input("Illegal board size. Try again.\nPlease select the game board size (2,3,4...): "))
    # Defined players
    num_of_players = int(input("How many players are playing (2,3,4...)? "))
    while num_of_players < 2:
        num_of_players = int(input("Illegal number of players. Try again.\nHow many players are playing (2,3,4...)? "))
    num_of_bots = int(input("How many computer bots are playing? (from 0 to " + str(num_of_players) + "): "))
    while not (num_of_players >= num_of_bots and num_of_bots >= 0):
        num_of_bots = int(input(
            "Illegal number of computer bots. Try again.\nHow many computer bots are playing? (from 0 to " + str(
                num_of_players) + "): "))
    order_player_game = makeOrderPlayerGame(num_of_players, num_of_bots)
    print(
        "The game contains " + str(num_of_players - num_of_bots) + " human players and " + str(num_of_bots) + " bots!")
    print("The order game playing: ")
    [print(e) for e in order_player_game]

    game = Game.Game(board_size=board_size)
    GUI(game).start()

    game.intializeGame(order_player_game)  # TODO: complete this function AKIVA: why is this necessary?  Pass order_player_game to constructor if Game object needs to know player order (currently on line 48)
    while (not game.endGame()):
        for (player, player_type) in order_player_game:

            game.players[player].play_phase1()
            game.players[player].play_phase2()
            game.players[player].play_phase3()

            # game.useSpecialCard(player) # TODO: complete this function
            # dice = game.rollDice()
            # if dice == 7:
            #     game.dropHalfCards() # TODO: complete this function 
            #     game.moveRobber(player[0], (i,j))  # TODO: complete this function
            # else:
            #     game.addSourcesToPlayers(dice) # TODO: complete this function

            # if player[1]=='bot':
            #     game.makeRandomAction(player[0]) # TODO: complete this function
            # else:
            #     game.makeAction(player[0]) # TODO: complete this function

            # game.useSpecialCard(player) # TODO: complete this function

            if game.endGame():
                break


if __name__ == "__main__":
    main()

    # game = Game.Game(actual_board_size=3)

    # game.addSettlement(position=(1,1), player_num=1, start_of_game=True)
    # game.addRoad(point1=(1,1), point2=(1,2), player_num=1)
    # game.addSettlement(position=(3, 3), player_num=3, start_of_game=True)
    # game.players[3 - 1].resources["ore"] += 3
    # game.players[3 - 1].resources["wheat"] += 2
    # game.addCity(position=(3,3), player_num=3)
    # print("After player 1 built 1 road, longest road owner was player", game.board.longest_road_owner, "with", game.players[game.board.longest_road_owner-1].victory_points, "victory points")
    # print("victory points situation:", list(map(lambda player: player.victory_points, game.players)))
    # game.addRoad(point1=(1, 1), point2=(1, 0), player_num=1)
    # print("After player 1 built 2 roads, longest road owner was player", game.board.longest_road_owner, "with", game.players[game.board.longest_road_owner-1].victory_points, "victory points")
    # print("victory points situation:", list(map(lambda player: player.victory_points, game.players)))
    # game.players[3 - 1].resources["wood"] += 3
    # game.players[3 - 1].resources["brick"] += 3
    # game.addRoad(point1=(3, 3), point2=(3, 4), player_num=3)
    # game.addRoad(point1=(3, 4), point2=(3, 5), player_num=3)
    # game.addRoad(point1=(3, 5), point2=(3, 6), player_num=3)
    # print("After player 3 built 3 roads, longest road owner was player", game.board.longest_road_owner, "with", game.players[game.board.longest_road_owner-1].victory_points, "victory points")
    # print("victory points situation:", list(map(lambda player: player.victory_points, game.players)))

    # # player_num number's binary representation sets his RGB value
    # getPlayerColor = lambda player: (255 * (player % 2), 255 * ((player // 2) % 2), 255 * (player // 4))
    # GUI.makeGraphical(game, getPlayerColor)
