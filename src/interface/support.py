from enums import Biome, StructureColor
import math

import sys
sys.path.append("..")
from board import Structure

def odd_q_to_pixel(q, r, hex_size=50):
    x = (3 / 2) * hex_size * q
    y = math.sqrt(3) * hex_size * (r + 0.5 * (q % 2))
    return int(x), int(y)

def add_structure(main_board, clicked_tile, structure_type, structure_color):
    main_board[clicked_tile[0]][clicked_tile[1]].structure = Structure(
        structure_color, structure_type
    )


def remove_structure(main_board, clicked_tile):
    main_board[clicked_tile[0]][clicked_tile[1]].structure = None


def draw_player_choice(clicked_tile, small_squares, small_circles, label, color):
    if clicked_tile and label == "False":
        # If the clicked_tile exists in small_circles, remove it from there
        if clicked_tile in small_circles:
            del small_circles[clicked_tile]

            # Add the clicked_tile to small_squares with the specified color
        small_squares[clicked_tile] = color
        print(small_squares)

    if clicked_tile and label == "True":
        # If the clicked_tile exists in small_squares, remove it from there
        if clicked_tile in small_squares:
            del small_squares[clicked_tile]

            # Add the clicked_tile to small_circles with the specified color
        small_circles[clicked_tile] = color
        print(small_circles)

bundle_colors = [
    (223, 66, 59),  # Red
    (253, 201, 27),  # Orange
    (52, 199, 206),  # Cyan
    (174, 228, 255),  # Light blue
    (126, 85, 207),  # Violet
]

colors = {
    Biome.WATER: (97, 150, 202),  # blue for water
    Biome.DESERT: (255, 212, 81),  # sandy brown for desert
    Biome.MOUNTAIN: (185, 185, 185),  # brown for mountain
    Biome.SWAMP: (117, 87, 115),  # dark purple for swamp
    Biome.FOREST: (113, 173, 103),  # dark green for forest
    StructureColor.BLACK: (0, 0, 0),  # black
    StructureColor.BLUE: (0, 0, 255),  # blue
    StructureColor.WHITE: (255, 255, 255),  # white
    StructureColor.GREEN: (0, 128, 0),  # green
}