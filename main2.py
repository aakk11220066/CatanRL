#import networkx as nx
#import matplotlib.pyplot as plt
#import random
from GUI import GUI
import Game


def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

def makeOrderPlayerGame(num_of_players):
    players = [x + 1 for x in list(range(num_of_players))]
    '''len = num_of_players
    order_player_game = []
    for i in range(num_of_players):
        player = random.choice(players[:len])
        if player <= num_of_players - num_of_bots:
            order_player_game.append((player, "HUMAN"))
        else:
            order_player_game.append((player, "BOT"))
        swapPositions(players, player - 1, len - 1)
        len -= 1
    return order_player_game'''
    return players

def enterParametersGame():
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
    order_player_game = makeOrderPlayerGame(num_of_players)
    print("The game contains " + str(num_of_players - num_of_bots) + " human players and " + str(num_of_bots) + " bots!")
    print("The order game playing: ")
    [print(e) for e in order_player_game]
    return board_size, order_player_game


def main():
    board_size, order_player_game = enterParametersGame()

    game = Game.Game(board_size=board_size, order_player_game=order_player_game, function_delay=1)
    GUI(game).start()
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    game.initializeGame()
    while (not game.endGame()):

        for player in order_player_game:
            print('@@@@@@@@@@@@@@@@@@@@ Player',player,'play @@@@@@@@@@@@@@@@@@@@')
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
            game.players[player-1].play_development_cards() # Future implemention
            game.rollDice(player_num=player)
            game.players[player-1].trade_cards() # Future implemention
            game.players[player-1].buy_road_or_settlement_or_city_or_development_card(game=game) # The function calls the game TODO
            print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')

            if game.endGame():
                break


if __name__ == "__main__":
    main()
