import pygame
from typing import Tuple

import Board
import Building
from Tile import TileType
from Game import Game

# presets
HEX_WIDTH = 80
HEX_HEIGHT = 90
BOARD_PIXEL_DIMENSIONS = 300
NUMBER_BACKGROUND_RADIUS = 20
NUMBER_SIZE = 25
THIEF_WIDTH = 15
THIEF_HEIGHT = 60
ROAD_THICKNESS = 7
SETTLEMENT_WIDTH = 20
SETTLEMENT_HEIGHT = 25
CITY_WIDTH = 25
CITY_HEIGHT = 27
LEGEND_SIZE = 15
LEGEND_OFFSET = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (48, 48, 148)
RED = (255, 0, 0)
DARK_GRAY = (100, 100, 100)
TRANSPARENT = (0, 0, 0, 0)
tileColors = {
    TileType.FOREST: (0, 200, 0),
    TileType.HILLS: (220, 170, 0),
    TileType.MOUNTAINS: (200, 200, 200),
    TileType.PASTURE: (180, 255, 180),
    TileType.DESERT: (110, 110, 10),
    TileType.FIELDS: (255, 230, 20),
    TileType.OCEAN: (0, 125, 250)
}

game: Game  # redefined to Game type in makeGraphical function
Coordinate = Tuple[int, int]


# topLeft is the coordinate of the top left corner of the bounding box
def addHexagon(board, color, topLeftCorner: Coordinate):
    pygame.draw.polygon(board, color,
                        (
                            (topLeftCorner[0] + 0, topLeftCorner[1] + HEX_HEIGHT / 4),
                            (topLeftCorner[0] + 0, topLeftCorner[1] + 3 * HEX_HEIGHT / 4),
                            (topLeftCorner[0] + HEX_WIDTH / 2, topLeftCorner[1] + HEX_HEIGHT),
                            (topLeftCorner[0] + HEX_WIDTH, topLeftCorner[1] + 3 * HEX_HEIGHT / 4),
                            (topLeftCorner[0] + HEX_WIDTH, topLeftCorner[1] + HEX_HEIGHT / 4),
                            (topLeftCorner[0] + HEX_WIDTH / 2, topLeftCorner[1] + 0)
                        )
                        )
    pygame.draw.polygon(
        board,
        DARK_GRAY,
        (
            (topLeftCorner[0] + 0, topLeftCorner[1] + HEX_HEIGHT / 4),
            (topLeftCorner[0] + 0, topLeftCorner[1] + 3 * HEX_HEIGHT / 4),
            (topLeftCorner[0] + HEX_WIDTH / 2, topLeftCorner[1] + HEX_HEIGHT),
            (topLeftCorner[0] + HEX_WIDTH, topLeftCorner[1] + 3 * HEX_HEIGHT / 4),
            (topLeftCorner[0] + HEX_WIDTH, topLeftCorner[1] + HEX_HEIGHT / 4),
            (topLeftCorner[0] + HEX_WIDTH / 2, topLeftCorner[1] + 0)
        ),
        4
    )


def xAlign(rowWidth):
    return (BOARD_PIXEL_DIMENSIONS / 2) - (HEX_WIDTH * rowWidth / 2)


def yAlign(numRows):
    return (BOARD_PIXEL_DIMENSIONS / 2) - (3 * HEX_HEIGHT * numRows / 8)


def setupBoard():
    # Create background
    board = pygame.Surface((BOARD_PIXEL_DIMENSIONS, BOARD_PIXEL_DIMENSIONS))
    board.fill(DARK_BLUE)

    font = pygame.font.Font('freesansbold.ttf', NUMBER_SIZE)

    # add legend
    for tile_type in TileType:
        pygame.draw.rect(board, tileColors[tile_type],
                         pygame.Rect(LEGEND_OFFSET,
                                     LEGEND_OFFSET + tile_type.value * (LEGEND_OFFSET // 2 + LEGEND_SIZE), LEGEND_SIZE,
                                     LEGEND_SIZE)
                         )
        legend_font = pygame.font.Font("freesansbold.ttf", LEGEND_SIZE)
        legend_text = legend_font.render(tile_type.name, True, BLACK)
        board.blit(legend_text,
                   (2 * LEGEND_OFFSET + LEGEND_SIZE,
                    tile_type.value * LEGEND_SIZE + LEGEND_OFFSET * (tile_type.value / 2 + 1))
                   )

    rowWidths = Board.rowWidths

    # add hexagons
    for (row, rowWidth) in enumerate(rowWidths):
        for col in range(rowWidth):
            topLeftCorner = (xAlign(rowWidth) + col * HEX_WIDTH, yAlign(len(rowWidths)) + 3 * row * HEX_HEIGHT / 4)
            tileData = game.board.graph.nodes[("tile", (row, col))]

            addHexagon(board, tileColors[tileData["tile_type"]],
                       topLeftCorner)
            if tileData["tile_type"] not in {TileType.DESERT, TileType.OCEAN}:
                pygame.draw.circle(board, WHITE,
                                   (int(topLeftCorner[0] + (HEX_WIDTH / 2)), int(topLeftCorner[1] + (HEX_HEIGHT / 2))),
                                   NUMBER_BACKGROUND_RADIUS
                                   )
                numColor = BLACK

                if tileData["number"] in {6, 8}:
                    numColor = RED
                text = font.render(str(tileData["number"]), True, numColor)
                board.blit(text,
                           (int(topLeftCorner[0] + (HEX_WIDTH / 2)) - (NUMBER_BACKGROUND_RADIUS / 2),
                            int(topLeftCorner[1] + (HEX_HEIGHT / 2)) - (NUMBER_BACKGROUND_RADIUS / 2))
                           )

    return board


def drawThief(board : pygame.Surface, topLeftCorner: Coordinate):
    pygame.draw.circle(board, BLACK,  # head
                       (int(topLeftCorner[0] + THIEF_WIDTH // 2), int(topLeftCorner[1] + THIEF_WIDTH // 2)),
                       THIEF_HEIGHT // 8)
    pygame.draw.line(board, BLACK,  # body
                     (topLeftCorner[0] + THIEF_WIDTH // 2, topLeftCorner[1] + THIEF_HEIGHT // 4),
                     (topLeftCorner[0] + THIEF_WIDTH // 2, topLeftCorner[1] + 3 * THIEF_HEIGHT // 4),
                     3
                     )
    pygame.draw.line(board, BLACK,  # right arm
                     (topLeftCorner[0] + THIEF_WIDTH // 2, topLeftCorner[1] + THIEF_HEIGHT // 4),
                     (topLeftCorner[0] + THIEF_WIDTH, topLeftCorner[1] + 2 * THIEF_HEIGHT // 4),
                     3
                     )
    pygame.draw.line(board, BLACK,  # left arm
                     (topLeftCorner[0] + THIEF_WIDTH // 2, topLeftCorner[1] + THIEF_HEIGHT // 4),
                     (topLeftCorner[0], topLeftCorner[1] + 2 * THIEF_HEIGHT // 4),
                     3
                     )
    pygame.draw.line(board, BLACK,  # right leg
                     (topLeftCorner[0] + THIEF_WIDTH // 2, topLeftCorner[1] + 3 * THIEF_HEIGHT // 4),
                     (topLeftCorner[0] + THIEF_WIDTH, topLeftCorner[1] + THIEF_HEIGHT),
                     3
                     )
    pygame.draw.line(board, BLACK,  # left leg
                     (topLeftCorner[0] + THIEF_WIDTH // 2, topLeftCorner[1] + 3 * THIEF_HEIGHT // 4),
                     (topLeftCorner[0], topLeftCorner[1] + THIEF_HEIGHT),
                     3
                     )


def getCornerCoordinates(cornerIndex: Coordinate):
    # offset of bottom half of board because top indices of hexagon now have higher index than lower
    if Board.get_board_half(cornerIndex[0], game.board.boardSize+1) == "lower":
        cornerIndex = cornerIndex[0], cornerIndex[1]-1

    rowWidth = Board.rowWidths[cornerIndex[0]]
    return (
        xAlign(rowWidth) + (cornerIndex[1] * (HEX_WIDTH / 2)),
        yAlign(len(Board.rowWidths)) + 3 * HEX_HEIGHT * cornerIndex[0] / 4 + (1 - (cornerIndex[1] % 2)) * (
                HEX_HEIGHT / 4)
    )


def drawRoads(board, getPlayerColor):
    for point_one_coordinates, point_two_coordinates in (
            (tagged_point1[1], tagged_point2[1]) for tagged_point1, tagged_point2 in game.board.graph.edges
            if (tagged_point1[0], tagged_point2[0]) == ("point", "point")
            and game.board.graph[tagged_point1][tagged_point2]["owner"] != Board.NO_PLAYER
    ):
        pygame.draw.line(board,
            getPlayerColor(game.board.graph[("point", point_one_coordinates)][("point", point_two_coordinates)]["owner"]),
            getCornerCoordinates(point_one_coordinates),
            getCornerCoordinates(point_two_coordinates),
            ROAD_THICKNESS
        )


def drawSettlements(board, getPlayerColor):
    for point in (game.board.graph.nodes[tagged_point] for tagged_point in game.board.graph.nodes
                if tagged_point[0] == 'point'
                and (game.board.graph.nodes[tagged_point]["building"]) == Building.BuildingTypes.Settlement
                ):
        rectangle_topLeftCorner = list(getCornerCoordinates(point["position"]))
        color = getPlayerColor(point["owner"])
        rectangle_topLeftCorner[0] = rectangle_topLeftCorner[0] - SETTLEMENT_WIDTH / 2
        rectangle_topLeftCorner[1] = rectangle_topLeftCorner[1] - SETTLEMENT_HEIGHT / 4
        rectangle_topLeftCorner = tuple(rectangle_topLeftCorner)
        pygame.draw.rect(board, color,  # body of settlement
                         rectangle_topLeftCorner + (SETTLEMENT_WIDTH, 3 * SETTLEMENT_HEIGHT / 4)
                         )
        pygame.draw.polygon(board, color,  # roof
                            (
                                rectangle_topLeftCorner,
                                (rectangle_topLeftCorner[0] + SETTLEMENT_WIDTH / 2,
                                 rectangle_topLeftCorner[1] - SETTLEMENT_HEIGHT / 4),
                                (rectangle_topLeftCorner[0] + SETTLEMENT_WIDTH, rectangle_topLeftCorner[1])
                            )
                            )


def drawCities(board, getPlayerColor):
    for point in (game.board.graph.nodes[tagged_point] for tagged_point in game.board.graph.nodes
                if tagged_point[0] == 'point'
                and (game.board.graph.nodes[tagged_point]["building"]) == Building.BuildingTypes.City
                ):
        city_topLeftCorner = list(getCornerCoordinates(point["position"]))
        color = getPlayerColor(point["owner"])
        city_topLeftCorner[0] = city_topLeftCorner[0] - CITY_WIDTH / 4
        city_topLeftCorner[1] = city_topLeftCorner[1] - CITY_HEIGHT / 2
        # rectangle_topLeftCorner = tuple(city_topLeftCorner)
        pygame.draw.polygon(board, color,
                            (
                                (city_topLeftCorner[0], city_topLeftCorner[1] + CITY_HEIGHT),
                                (city_topLeftCorner[0] + CITY_WIDTH, city_topLeftCorner[1] + CITY_HEIGHT),
                                (city_topLeftCorner[0] + CITY_WIDTH, city_topLeftCorner[1] + 2 * CITY_HEIGHT / 3),
                                (city_topLeftCorner[0] + 2 * CITY_WIDTH / 3,
                                 city_topLeftCorner[1] + 2 * CITY_HEIGHT / 3),
                                (city_topLeftCorner[0] + 2 * CITY_WIDTH / 3,
                                 city_topLeftCorner[1] + CITY_HEIGHT / 5),
                                (city_topLeftCorner[0] + CITY_WIDTH / 3, city_topLeftCorner[1]),
                                (city_topLeftCorner[0], city_topLeftCorner[1] + CITY_HEIGHT / 5),
                            )
                            )


def makeGraphical(getPlayerColor, render_request_status : bool):
    global BOARD_PIXEL_DIMENSIONS
    BOARD_PIXEL_DIMENSIONS += HEX_HEIGHT*1.5*game.board.boardSize

    pygame.init()
    screen = pygame.display.set_mode((int(1.2 * BOARD_PIXEL_DIMENSIONS), int(1.2 * BOARD_PIXEL_DIMENSIONS)))
    empty_board = setupBoard()

    done = False
    clock = pygame.time.Clock()

    while not done and render_request_status():
        # Clear the screen
        screen.fill(BLACK)
        board = empty_board.copy()

        thief_xAlign = xAlign(Board.rowWidths[game.board.thief_location[0]])
        thief_graphical_position = (
            thief_xAlign + (HEX_WIDTH * (game.board.thief_location[1] + 0.5)) - (THIEF_WIDTH * 0.5),
            yAlign(len(Board.rowWidths)) + (HEX_HEIGHT * (3 * game.board.thief_location[0] / 4 + 0.5)) -
                (THIEF_HEIGHT * 0.5)
        )
        drawThief(board, thief_graphical_position)
        
        drawRoads(board, getPlayerColor)
        drawSettlements(board, getPlayerColor)
        drawCities(board, getPlayerColor)

        # Draw board
        screen.blit(board, (int(BOARD_PIXEL_DIMENSIONS * 0.1), int(BOARD_PIXEL_DIMENSIONS * 0.1)))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Update the screen
        clock.tick()
        pygame.display.flip()

# player_num number's binary representation sets his RGB value
def default_player_colors(player: int):
    return 255 * (player % 2), 255 * ((player // 2) % 2), 255 * (player // 4)


class GUI(pygame.threads.Thread):
    def __init__(self, _game: Game, getPlayerColor=default_player_colors, render_request_status = None):
        super().__init__()
        global game
        game = _game
        self.getPlayerColor = getPlayerColor
        self.render_request_status = render_request_status
        if self.render_request_status is None:
            self.render_request_status = lambda: True


    def run(self):
        makeGraphical(self.getPlayerColor, self.render_request_status)
