from os import remove
import pygame
import math
from interface.buttons import create_button_bundles, create_left_side_button_bundle
from board import Board
from enums import StructureType, Territory, Structure
from interface.drawing import (
    draw_hexagon,
    draw_small_octagon,
    draw_small_square,
    draw_small_circle,
    draw_small_triangle,
    draw_lines_close_to_hexagon_edges,
)
from interface.events import key_pressed
from interface.support import (
    odd_q_to_pixel,
    draw_player_choice,
    get_key_by_value,
    remove_structure,
)
from src.enums import bundle_colors, colors, structure_bundle_colors


class GameState:
    # this could be moved to config file?
    screen_width = 1400
    screen_height = 1000
    cols = Board.width
    rows = Board.height
    # Define button dimensions
    button_width = 100
    button_height = 40  # Adjust button size as needed
    bundle_gap = 40
    button_gap = 20
    # Define the gap between button bundles and between buttons within a bundle
    small_square_size = 10
    small_circle_size = 7
    small_triangle_size = 20
    small_octagon_size = 20
    # Define the size of each hexagon and the gap between hexagons
    hex_size = 50
    hex_gap = 5
    circle_offsets = (
        (0, -30),
        (30, -15),
        (20, 30),
        (-20, 30),
        (-30, -15),
    )

    def __init__(self, number_of_players: int, difficulty: int):
        hard = difficulty == 1
        self.skip_black = 0 if hard else 1
        self.font = pygame.font.Font(None, 36)
        print(f"Difficulty: {difficulty}, Hard: {hard}")
        self.main_board = Board()

        # Create the screen
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), 0, 0
        )
        pygame.display.set_caption("Cryptid Solver")

        # Get the button rectangles using the function from button_bundle.py
        self.button_rectangles = create_button_bundles(
            self.screen,
            self.button_width,
            self.button_height,
            self.button_gap,
            self.bundle_gap,
            bundle_colors[0:number_of_players],
        )

        self.structures_button_rectangles = create_button_bundles(
            self.screen,
            self.button_width,
            self.button_height,
            self.button_gap,
            self.bundle_gap,
            structure_bundle_colors,
        )

        # Main loop
        self.running = True
        self.clicked_tile = tuple()
        self.small_squares = {}
        self.small_circles = {}
        self.structure_placed = False
        self.alert = False
        self.structures = {}

        self.list_of_clues = []
        filename = "data/normal_clues.txt" if not hard else "data/advanced_clues.txt"
        with open(filename, "r") as f:
            self.list_of_clues = f.read().splitlines()

    def get_board_width(self) -> float:
        return (3 / 2) * self.hex_size * (self.cols + 1)

    def get_board_height(self) -> float:
        return math.sqrt(3) * self.hex_size * (self.rows + 1)

    # Function to center the board on the screen
    def get_board_offset(self) -> tuple[float, float]:
        x_offset = (self.screen_width - self.get_board_width()) / 2
        y_offset = (self.screen_height - self.get_board_height()) / 2

        return x_offset, y_offset


def run(s: GameState):
    while s.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                s.running = False

            if event.type == pygame.KEYDOWN:
                key_pressed(
                    s.main_board, s.clicked_tile, s.small_squares, s.small_circles
                )

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any button is clicked

                x, y = event.pos
                if s.structure_placed:
                    for bundle_index, button_rects in enumerate(s.button_rectangles):
                        for button_index, button_rect in enumerate(button_rects):
                            if button_rect.collidepoint(x, y):
                                # Handle button click
                                label = "True" if button_index == 0 else "False"
                                color = bundle_colors[bundle_index]
                                print(
                                    f"Clicked a button at Bundle {bundle_index + 1}, Label: {label}, Color: {color}"
                                )
                                draw_player_choice(
                                    s.clicked_tile,
                                    s.small_squares,
                                    s.small_circles,
                                    label,
                                    color,
                                )
                else:
                    for bundle_index, button_rects in enumerate(
                        s.structures_button_rectangles[: -s.skip_black]
                    ):
                        for button_index, button_rect in enumerate(button_rects):
                            if button_rect.collidepoint(x, y):
                                # Handle button click
                                structure_type = (
                                    StructureType.SHACK
                                    if button_index == 0
                                    else StructureType.STONE
                                )
                                color = structure_bundle_colors[bundle_index]
                                print(
                                    f"Clicked a button at Bundle {bundle_index + 1}, Structure: {structure_type}, Color: {color}"
                                )
                                placed_structure = Structure(color, structure_type).name
                                if placed_structure not in s.structures:
                                    s.structures[placed_structure] = s.clicked_tile
                                else:
                                    remove_structure(
                                        s.main_board.grid,
                                        s.structures[placed_structure],
                                    )
                                    s.structures[placed_structure] = s.clicked_tile

                                s.main_board.grid[s.clicked_tile[0]][
                                    s.clicked_tile[1]
                                ].structure = Structure(
                                    get_key_by_value(colors, color), structure_type
                                )

                    if pygame.Rect(
                        s.screen.get_width() - s.button_width - s.bundle_gap,
                        s.screen.get_height() - s.button_height - s.bundle_gap,
                        s.button_width,
                        s.button_height,
                    ).collidepoint(x, y):
                        print("Confirm button clicked")
                        print(s.small_squares)
                        print(s.small_circles)
                        s.structure_placed = True

                for row in range(s.rows):
                    for col in range(s.cols):
                        x, y = event.pos
                        tile_x, tile_y = odd_q_to_pixel(col, row)
                        x_offset, y_offset = s.get_board_offset()
                        tile_x += x_offset
                        tile_y += y_offset
                        # Check if the mouse click is within the tile's bounding rectangle
                        if (
                            abs(x - tile_x) < s.hex_size
                            and abs(y - tile_y) < s.hex_size * math.sqrt(3) / 2
                        ):
                            s.clicked_tile = (row, col)
                            print(f"Clicked tile: {s.clicked_tile}")

        # Clear the screen
        s.screen.fill((255, 255, 255))

        # Center the board on the screen
        x_offset, y_offset = s.get_board_offset()

        # display clues
        if s.structure_placed:
            text_offset = 100
            for clue in s.list_of_clues:
                num_players_text = s.font.render(f"{clue}", True, (0, 0, 0))
                s.screen.blit(
                    num_players_text, (s.get_board_width() + 150, text_offset)
                )
                text_offset += 20
        # Draw each hexagon on the screen
        for row in range(s.rows):
            for col in range(s.cols):
                # print(f'{row}/{rows}', f'{col}/{cols}')
                value = s.main_board.grid[row][col]
                # print(main_board.grid)
                # print(value)
                color = value.biome.get_color()
                x, y = odd_q_to_pixel(col, row)
                x += x_offset
                y += y_offset

                if s.clicked_tile == (row, col):
                    lighter_color = [min(c + 50, 255) for c in color]
                    draw_hexagon(s.screen, s.hex_size, x, y, lighter_color)
                else:
                    draw_hexagon(s.screen, s.hex_size, x, y, color)
                if value.territory is not None:
                    if value.territory == Territory.COUGAR:
                        draw_lines_close_to_hexagon_edges(
                            s.screen, s.hex_size, x, y, 2, (255, 0, 0)
                        )
                    elif value.territory == Territory.BEAR:
                        draw_lines_close_to_hexagon_edges(
                            s.screen, s.hex_size, x, y, 2, (0, 0, 0)
                        )
                if value.structure is not None:
                    if value.structure.type == StructureType.STONE:
                        draw_small_octagon(
                            s.screen,
                            row,
                            col,
                            colors[value.structure.color],
                            s.small_octagon_size,
                            x_offset,
                            y_offset,
                        )
                    elif value.structure.type == StructureType.SHACK:
                        draw_small_triangle(
                            s.screen,
                            row,
                            col,
                            colors[value.structure.color],
                            s.small_triangle_size,
                            x_offset,
                            y_offset,
                        )

        def draw_buttons(buttons, colors, structures=False):
            # Draw the button bundles on the screen if structured are placed
            for bundle_index, button_rects in enumerate(buttons):
                bundle_x = (
                    bundle_index * (s.button_width * 2 + s.button_gap * 2)
                    + s.bundle_gap
                )
                bundle_y = s.screen_height - s.button_height - s.bundle_gap
                for button_index, button_rect in enumerate(button_rects):
                    button_x = bundle_x + (s.button_width + s.button_gap) * button_index
                    button_y = bundle_y
                    pygame.draw.rect(
                        s.screen,
                        (0, 0, 0),  # Black color for the border
                        (
                            button_x - 2,
                            button_y - 2,
                            s.button_width + 4,
                            s.button_height + 4,
                        ),  # Larger rectangle for the border
                    )
                    pygame.draw.rect(
                        s.screen,
                        colors[bundle_index],
                        (button_x, button_y, s.button_width, s.button_height),
                    )
                    font = pygame.font.Font(None, 24)
                    if s.structure_placed:
                        label = "True" if button_index == 0 else "False"
                    else:
                        label = "Shack" if button_index == 0 else "Stone"
                    if colors[bundle_index] == (255, 255, 255):
                        text = font.render(label, True, (0, 0, 0))
                    else:
                        text = font.render(label, True, (255, 255, 255))
                    text_rect = text.get_rect(
                        center=(
                            button_x + s.button_width // 2,
                            button_y + s.button_height // 2,
                        )
                    )
                    s.screen.blit(text, text_rect)

        def draw_confirm_button():
            button_x = s.screen.get_width() - s.button_width - s.bundle_gap
            button_y = s.screen.get_height() - s.button_height - s.bundle_gap
            pygame.draw.rect(
                s.screen,
                (0, 0, 0),  # Black color for the border
                (
                    button_x - 2,
                    button_y - 2,
                    s.button_width + 4,
                    s.button_height + 4,
                ),  # Larger rectangle for the border
            )
            pygame.draw.rect(
                s.screen,
                (255, 255, 255),
                (button_x, button_y, s.button_width, s.button_height),
            )
            font = pygame.font.Font(None, 24)
            text = font.render("Confirm", True, (0, 0, 0))
            text_rect = text.get_rect(
                center=(button_x + s.button_width // 2, button_y + s.button_height // 2)
            )
            s.screen.blit(text, text_rect)

        if s.structure_placed:
            draw_buttons(s.button_rectangles, bundle_colors)
        else:
            draw_buttons(
                s.structures_button_rectangles[: -s.skip_black],
                structure_bundle_colors[: -s.skip_black],
            )
            # if any((len(structures) == 6 and not hard, len(structures) == 8 and hard)):
            draw_confirm_button()

        for small_square in s.small_squares.keys():
            tile, color = small_square, s.small_squares[small_square]
            # print(clicked_tile, selected_color)
            draw_small_square(
                s.screen,
                tile[0],
                tile[1],
                color,
                s.small_square_size,
                x_offset,
                y_offset + 30,
            )
        for coords in s.small_circles.keys():
            for index, color in enumerate(s.small_circles[coords]):
                #  color = small_circles[small_circle]
                x_with_offset = x_offset + s.circle_offsets[index][0]
                y_with_offset = y_offset + s.circle_offsets[index][1]
                draw_small_circle(
                    s.screen,
                    coords[0],
                    coords[1],
                    color,
                    s.small_circle_size,
                    x_with_offset,
                    y_with_offset,
                )

        # Update the display
        pygame.display.flip()

    # Quit pygame and exit the program
    pygame.quit()
