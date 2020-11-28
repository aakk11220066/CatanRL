from GUI import GUI
import Game


def main():
    game = Game.Game(board_size=3, function_delay=1)
    game.rollDice(player_num=1)
    GUI(game).start()

    game.addSettlement(position=(1, 1), player_num=1, start_of_game=True)
    game.addRoad(point1=(1, 1), point2=(1, 2), player_num=1)
    game.addSettlement(position=(3, 3), player_num=3, start_of_game=True)
    game.players[3 - 1].resources["ore"] += 3
    game.players[3 - 1].resources["wheat"] += 2
    game.addCity(position=(3, 3), player_num=3)
    print("After player 1 built 1 road, longest road owner was player", game.board.longest_road_owner, "with",
          game.players[game.board.longest_road_owner - 1].victory_points, "victory points")
    print("victory points situation:", list(map(lambda player: player.victory_points, game.players)))
    game.addRoad(point1=(1, 1), point2=(1, 0), player_num=1)
    print("After player 1 built 2 roads, longest road owner was player", game.board.longest_road_owner, "with",
          game.players[game.board.longest_road_owner - 1].victory_points, "victory points")
    print("victory points situation:", list(map(lambda player: player.victory_points, game.players)))
    game.players[3 - 1].resources["wood"] += 3
    game.players[3 - 1].resources["brick"] += 3
    game.addRoad(point1=(3, 3), point2=(3, 4), player_num=3)
    game.addRoad(point1=(3, 4), point2=(3, 5), player_num=3)
    game.addRoad(point1=(3, 5), point2=(3, 6), player_num=3)
    print("After player 3 built 3 roads, longest road owner was player", game.board.longest_road_owner, "with",
          game.players[game.board.longest_road_owner - 1].victory_points, "victory points")
    print("victory points situation:", list(map(lambda player: player.victory_points, game.players)))


if __name__ == "__main__":
    main()
