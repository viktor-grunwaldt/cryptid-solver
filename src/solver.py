import pygame
import math
from interface.buttons import create_button_bundles, create_left_side_button_bundle
from board import Board
from enums import StructureType, Territory
from interface.drawing import (
    draw_hexagon,
    draw_small_square,
    draw_small_circle,
    draw_small_triangle,
    draw_lines_close_to_hexagon_edges,
)
from interface.events import key_pressed
from interface.support import bundle_colors, colors, odd_q_to_pixel, draw_player_choice

# Initialize pygame
pygame.init()

# Define the screen dimensions
screen_width, screen_height = 1400, 1000

main_board = Board()

cols = Board.width
rows = Board.height


# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cryptid Solver")

# Define button dimensions
button_width, button_height = 100, 40  # Adjust button size as needed

# Define the gap between button bundles and between buttons within a bundle
bundle_gap = 40
button_gap = 20

small_square_size = 10
small_circle_size = 10
small_triangle_size = 20
small_hexagon_size = 20

# Define the size of each hexagon and the gap between hexagons
hex_size = 50
hex_gap = 5
# Get the button rectangles using the function from button_bundle.py
button_rectangles = create_button_bundles(
    screen, button_width, button_height, button_gap, bundle_gap, bundle_colors
)

left_side_buttons = create_left_side_button_bundle(screen)


# Function to center the board on the screen
def center_board(screen_width, screen_height, cols, rows):
    board_width = (3 / 2) * hex_size * (cols + 1)
    board_height = math.sqrt(3) * hex_size * (rows + 1)

    x_offset = (screen_width - board_width) // 2
    y_offset = (screen_height - board_height) // 2

    return x_offset, y_offset


# Main loop
running = True
clicked_tile = None
selected_color = None
small_squares = {}
small_circles = {}


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            key_pressed(main_board, clicked_tile, small_squares, small_circles)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any button is clicked
            x, y = event.pos
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
                    draw_hexagon(
                        screen, small_hexagon_size, x, y, colors[value.structure.color]
                    )
                elif value.structure.type == StructureType.SHACK:
                    draw_small_triangle(screen, row, col, colors[value.structure.color], small_triangle_size, x_offset, y_offset)

    # Draw the button bundles on the screen
    for bundle_index, button_rects in enumerate(button_rectangles):
        bundle_x = bundle_index * (button_width * 2 + button_gap * 2) + bundle_gap
        bundle_y = screen_height - button_height - bundle_gap
        for button_index, button_rect in enumerate(button_rects):
            button_x = bundle_x + (button_width + button_gap) * button_index
            button_y = bundle_y
            # print(bundle_index)
            pygame.draw.rect(
                screen,
                bundle_colors[bundle_index],
                (button_x, button_y, button_width, button_height),
            )
            font = pygame.font.Font(None, 24)
            label = "True" if button_index == 0 else "False"
            text = font.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(button_x + button_width // 2, button_y + button_height // 2)
            )
            screen.blit(text, text_rect)

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
