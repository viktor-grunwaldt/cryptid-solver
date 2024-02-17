import pygame
import math
import os
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
from interface.support import bundle_colors, colors, odd_q_to_pixel, draw_player_choice, structure_bundle_colors, get_key_by_value

def create_board(number_of_players: int, difficulty: int):

    hard = False
    if difficulty == 2:
        hard = True

    
    # Define the screen dimensions
    screen_width, screen_height = 1400, 1000

    main_board = Board()

    cols = Board.width
    rows = Board.height

    font = pygame.font.Font(None, 36)

    # Create the screen
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 0)
    pygame.display.set_caption("Cryptid Solver")

    # Define button dimensions
    button_width, button_height = 100, 40  # Adjust button size as needed

    # Define the gap between button bundles and between buttons within a bundle
    bundle_gap = 40
    button_gap = 20

    small_square_size = 10
    small_circle_size = 10
    small_triangle_size = 20
    small_octagon_size = 20

    # Define the size of each hexagon and the gap between hexagons
    hex_size = 50
    hex_gap = 5
    # Get the button rectangles using the function from button_bundle.py
    button_rectangles = create_button_bundles(
        screen, button_width, button_height, button_gap, bundle_gap, bundle_colors[0:number_of_players]
    )
    structures_button_rectangles = create_button_bundles(
        screen, button_width, button_height, button_gap, bundle_gap, structure_bundle_colors
    ) 

    left_side_buttons = create_left_side_button_bundle(screen)

    def get_board_width():
        return (3 / 2) * hex_size * (cols + 1)
    def get_board_height():
        return math.sqrt(3) * hex_size * (rows + 1)

    # Function to center the board on the screen
    def center_board(screen_width, screen_height, cols, rows):
        x_offset = (screen_width - get_board_width()) // 2
        y_offset = (screen_height - get_board_height()) // 2

        return x_offset, y_offset


    # Main loop
    running = True
    clicked_tile = None
    selected_color = None
    small_squares = {}
    small_circles = {}

    list_of_clues = []

    with open("data/normal_clues.txt", 'r') as file:
        list_of_clues = file.read().splitlines()
    if hard:
        with open("data/advanced_clues.txt", 'r') as file:
            list_of_clues += file.read().splitlines()

    structure_placed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                key_pressed(main_board, clicked_tile, small_squares, small_circles)

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any button is clicked
                x, y = event.pos
                if structure_placed:
                    for bundle_index, button_rects in enumerate(button_rectangles):
                        for button_index, button_rect in enumerate(button_rects):
                            if button_rect.collidepoint(x, y):
                                # Handle button click
                                label = "True" if button_index == 0 else "False"
                                color = bundle_colors[bundle_index]
                                print(
                                    f"Clicked a button at Bundle {bundle_index + 1}, Label: {label}, Color: {color}"
                                )
                                draw_player_choice(
                                    clicked_tile, small_squares, small_circles, label, color
                                )
                else:
                    for bundle_index, button_rects in enumerate(structures_button_rectangles):
                        for button_index, button_rect in enumerate(button_rects):
                            if button_rect.collidepoint(x, y):
                                # Handle button click
                                structure_type = StructureType.SHACK if button_index == 0 else StructureType.STONE
                                color = structure_bundle_colors[bundle_index]
                                print(
                                    f"Clicked a button at Bundle {bundle_index + 1}, Structure: {structure_type}, Color: {color}"
                                )
                                # print(main_board.grid[clicked_tile[0]][clicked_tile[1]])
                                
                                main_board.grid[clicked_tile[0]][clicked_tile[1]].structure = Structure(
                                  get_key_by_value(colors, color)  , structure_type
                                )
                                #     color, structure_type
                                # )
                                # print(main_board.grid[clicked_tile[0]][clicked_tile[1]].structure)
                    if pygame.Rect(screen.get_width() - button_width - bundle_gap, screen.get_height() - button_height - bundle_gap, button_width, button_height).collidepoint(x, y):
                        print("Confirm button clicked")
                        print(small_squares)
                        print(small_circles)
                        structure_placed = True

                for row in range(rows):
                    for col in range(cols):
                        x, y = event.pos
                        tile_x, tile_y = odd_q_to_pixel(col, row)
                        tile_x += x_offset
                        tile_y += y_offset
                        # Check if the mouse click is within the tile's bounding rectangle
                        if (
                            abs(x - tile_x) < hex_size
                            and abs(y - tile_y) < hex_size * math.sqrt(3) / 2
                        ):
                            clicked_tile = (row, col)
                            print(f"Clicked tile: {clicked_tile}")

        # Clear the screen
        screen.fill((255, 255, 255))

        # Center the board on the screen
        x_offset, y_offset = center_board(screen_width, screen_height, cols, rows)

        # display clues
        if structure_placed:
            text_offset = 100
            for clue in list_of_clues:
                num_players_text = font.render(f"{clue}", True, (0, 0, 0))
                screen.blit(num_players_text, (get_board_width()+150, text_offset))
                text_offset += 20
        # Draw each hexagon on the screen
        for row in range(rows):
            for col in range(cols):
                # print(f'{row}/{rows}', f'{col}/{cols}')
                value = main_board.grid[row][col]
                # print(main_board.grid)
                # print(value)
                color = colors.get(value.biome, (255, 255, 255))
                x, y = odd_q_to_pixel(col, row)
                x += x_offset
                y += y_offset

                if clicked_tile == (row, col):
                    lighter_color = [min(c + 50, 255) for c in color]
                    draw_hexagon(screen, hex_size, x, y, lighter_color)
                else:
                    draw_hexagon(screen, hex_size, x, y, color)
                if value.territory is not None:
                    if value.territory == Territory.COUGAR:
                        draw_lines_close_to_hexagon_edges(
                            screen, hex_size, x, y, 2, (255, 0, 0)
                        )
                    elif value.territory == Territory.BEAR:
                        draw_lines_close_to_hexagon_edges(
                            screen, hex_size, x, y, 2, (0, 0, 0)
                        )
                if value.structure is not None:
                    if value.structure.type == StructureType.STONE:
                        draw_small_octagon(
                            screen, row, col, colors[value.structure.color], small_octagon_size, x_offset, y_offset
                        )
                    elif value.structure.type == StructureType.SHACK:
                        draw_small_triangle(screen, row, col, colors[value.structure.color], small_triangle_size, x_offset, y_offset)
        def draw_buttons(buttons, colors, structures=False):
            # Draw the button bundles on the screen if structured are placed
            for bundle_index, button_rects in enumerate(buttons):
                bundle_x = bundle_index * (button_width * 2 + button_gap * 2) + bundle_gap
                bundle_y = screen_height - button_height - bundle_gap
                for button_index, button_rect in enumerate(button_rects):
                    button_x = bundle_x + (button_width + button_gap) * button_index
                    button_y = bundle_y
                    pygame.draw.rect(
                        screen,
                        (0,0,0),  # Black color for the border
                        (button_x - 2, button_y - 2, button_width + 4, button_height + 4),  # Larger rectangle for the border
                    )
                    pygame.draw.rect(
                        screen,
                        colors[bundle_index],
                        (button_x, button_y, button_width, button_height),
                    )
                    font = pygame.font.Font(None, 24)
                    if structure_placed:
                        label = "True" if button_index == 0 else "False"
                    else:
                        label = "Shack" if button_index == 0 else "Stone"
                    if colors[bundle_index] == (255, 255, 255):
                        text = font.render(label, True, (0,0,0))
                    else:
                        text = font.render(label, True, (255, 255, 255))
                    text_rect = text.get_rect(
                        center=(button_x + button_width // 2, button_y + button_height // 2)
                    )
                    screen.blit(text, text_rect)
        def draw_confirm_button():
            button_x = screen.get_width() - button_width - bundle_gap
            button_y = screen.get_height() - button_height - bundle_gap
            pygame.draw.rect(
                screen,
                (0,0,0),  # Black color for the border
                (button_x - 2, button_y - 2, button_width + 4, button_height + 4),  # Larger rectangle for the border
            )
            pygame.draw.rect(
                screen,
                (255, 255, 255),
                (button_x, button_y, button_width, button_height),
            )
            font = pygame.font.Font(None, 24)
            text = font.render("Confirm", True, (0,0,0))
            text_rect = text.get_rect(
                center=(button_x + button_width // 2, button_y + button_height // 2)
            )
            screen.blit(text, text_rect)

        if structure_placed:
            draw_buttons(button_rectangles, bundle_colors)
        else:
            draw_buttons(structures_button_rectangles, structure_bundle_colors)
            draw_confirm_button()

        for small_square in small_squares.keys():
            tile, color = small_square, small_squares[small_square]
            # print(clicked_tile, selected_color)
            draw_small_square(screen, tile[0], tile[1], color, small_square_size, x_offset, y_offset)
        for small_circle in small_circles.keys():
            tile, color = small_circle, small_circles[small_circle]
            draw_small_circle(screen, tile[0], tile[1], color, small_circle_size, x_offset, y_offset)

        # Update the display
        pygame.display.flip()

    # Quit pygame and exit the program
    pygame.quit()
