from CatanGame.GUI import GUI
import CatanGame


def main():
    game = CatanGame.CatanGame.CatanGame(board_size=3, function_delay=0.5)
    gui = GUI(game)
    gui.start()

    game.players[1 - 1].resources["wood"] += 3000
    game.players[1 - 1].resources["brick"] += 3000
    game.players[1 - 1].resources["sheep"] += 3000
    game.players[1 - 1].resources["wheat"] += 3000
    game.add_settlement(position=("point", (3, 9)), player_num=1, start_of_game=True)
    game.collect_surrounding_resources(("point", (3, 9)))
    game.board.move_thief(("point", (3, 3)))
    print("game.board.get_valid_city_locations(1) =", list(game.board.get_valid_city_locations(1)))

    game.add_settlement(position=("point", (1, 2)), player_num=1, start_of_game=True)
    print("game.board.get_valid_city_locations(1) =", list(game.board.get_valid_city_locations(1)))
    # print("After player 1 built 1 road, longest road owner was player", game.board.longest_road_owner, "with",
    #      game.players[game.board.longest_road_owner - 1].victory_points, "victory points")
    # print("victory points situation:", _list(map(lambda player: player.victory_points, game.players)))
    game.add_road(road=(("point", (3, 8)), ("point", (3, 9))), player_num=1)
    # print("After player 1 built 2 roads, longest road owner was player", game.board.longest_road_owner, "with",
    #      game.players[game.board.longest_road_owner - 1].victory_points, "victory points")
    # print("victory points situation:", _list(map(lambda player: player.victory_points, game.players)))
    # print("After player 3 built 3 roads, longest road owner was player", game.board.longest_road_owner, "with",
    #      game.players[game.board.longest_road_owner - 1].victory_points, "victory points")
    # print("victory points situation:", _list(map(lambda player: player.victory_points, game.players)))

    game.add_settlement(position=("point", (4, 5)), player_num=1, start_of_game=True)
    game.add_settlement(position=("point", (5, 2)), player_num=1, start_of_game=True)
    print("game.board.get_valid_city_locations(1) =", list(game.board.get_valid_city_locations(1)))

    '''game.addRoad((3, 2), (3,3), 3)
    game.addRoad((3, 2), (4, 2), 3)
    game.addRoad((4, 2), (4, 3), 3)
    game.addRoad((4,3), (5, 2), 3)
    while game.board.get_valid_road_locations(player=1):
        for loc in game.board.get_valid_road_locations(player=1):
            game.addRoad(point1=loc[0][1], point2=loc[1][1], player_num=1)'''


if __name__ == "__main__":
    main()
