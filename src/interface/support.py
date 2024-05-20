from enums import Structure
import math

import sys

sys.path.append("..")


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
        small_squares[clicked_tile] = color

    if clicked_tile and label == "True":
        if clicked_tile not in small_circles:
            small_circles[clicked_tile] = []
        if color not in small_circles[clicked_tile]:
            small_circles[clicked_tile].append(color)


def get_key_by_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None  # Return None if the value is not found in the dictionary
