import pygame
import math
from buttons import create_button_bundles
from board import Board

# Rest of the code remains the same...

# Initialize pygame
pygame.init()

# Define the screen dimensions
screen_width, screen_height = 1400, 600

main_board = [
    ["w", "d", "w", "f"],
    ["w", "m", "f", "s"],
    ["d", "m", "w", "d"],
    ["f", "w", "s", "s"],
]

cols = 4
rows = 4

small_square_size = 10
small_circle_size = 10


def draw_small_square(screen, row, col, color):
    x, y = odd_q_to_pixel(col, row)
    x += x_offset
    y += y_offset
    square_x = x - small_square_size // 2
    square_y = y - small_square_size // 2

    # Draw the black outline first
    outline_size = 2  # You can adjust this value as needed
    outline_x = square_x - outline_size
    outline_y = square_y - outline_size
    outline_width = small_square_size + outline_size * 2
    outline_height = small_square_size + outline_size * 2
    pygame.draw.rect(
        screen, (0, 0, 0), (outline_x, outline_y, outline_width, outline_height)
    )

    # Draw the filled square on top of the outline
    pygame.draw.rect(
        screen, color, (square_x, square_y, small_square_size, small_square_size)
    )


def draw_small_circle(screen, row, col, color):
    x, y = odd_q_to_pixel(col, row)
    x += x_offset
    y += y_offset

    # Draw the black outline first
    outline_size = 2  # You can adjust this value as needed
    pygame.draw.circle(screen, (0, 0, 0), (x, y), small_circle_size + outline_size)

    # Draw the filled circle on top of the outline
    pygame.draw.circle(screen, color, (x, y), small_circle_size)


# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hexagonal Map with Buttons")

# Define button dimensions
button_width, button_height = 100, 40  # Adjust button size as needed

# Define the gap between button bundles and between buttons within a bundle
bundle_gap = 50
button_gap = 20

# Define the size of each hexagon and the gap between hexagons
hex_size = 30
hex_gap = 5

bundle_colors = [
    (255, 0, 0),  # Red
    (255, 165, 0),  # Orange
    (0, 128, 0),  # Green
    (173, 216, 230),  # Light blue
    (238, 130, 238),  # Violet
]

colors = {
    "w": (0, 0, 255),  # blue for water
    "d": (244, 164, 96),  # sandy brown for desert
    "m": (139, 69, 19),  # brown for mountain
    "s": (128, 0, 128),  # dark purple for swamp
    "f": (0, 100, 0),  # dark green for forest
}

# Get the button rectangles using the function from button_bundle.py
button_rectangles = create_button_bundles(
    screen, button_width, button_height, button_gap, bundle_gap, bundle_colors
)


# Function to center the board on the screen
def center_board(screen_width, screen_height, cols, rows):
    board_width = (3 / 2) * hex_size * (cols + 1)
    board_height = math.sqrt(3) * hex_size * (rows + 1)

    x_offset = (screen_width - board_width) // 2
    y_offset = (screen_height - board_height) // 2

    return x_offset, y_offset


def odd_q_to_pixel(q, r):
    x = (3 / 2) * hex_size * q
    y = math.sqrt(3) * hex_size * (r + 0.5 * (q % 2))
    return int(x), int(y)


# Main loop
running = True
clicked_tile = None
selected_color = None
small_squares = {}
small_circles = {}


def draw_hexagon(screen, hex_size, x, y, color):
    pygame.draw.polygon(
        screen,
        color,
        [
            (x + hex_size, y),
            (x + hex_size / 2, y - math.sqrt(3) / 2 * hex_size),
            (x - hex_size / 2, y - math.sqrt(3) / 2 * hex_size),
            (x - hex_size, y),
            (x - hex_size / 2, y + math.sqrt(3) / 2 * hex_size),
            (x + hex_size / 2, y + math.sqrt(3) / 2 * hex_size),
        ],
    )


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
            value = main_board[row][col]
            # print(main_board.grid)
            color = colors.get(value, (255, 255, 255))
            x, y = odd_q_to_pixel(col, row)
            x += x_offset
            y += y_offset

            if clicked_tile == (row, col):
                lighter_color = [min(c + 50, 255) for c in color]
                draw_hexagon(screen, hex_size, x, y, lighter_color)
            else:
                draw_hexagon(screen, hex_size, x, y, color)

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
        draw_small_square(screen, tile[0], tile[1], color)
    for small_circle in small_circles.keys():
        tile, color = small_circle, small_circles[small_circle]
        draw_small_circle(screen, tile[0], tile[1], color)

    # Update the display
    pygame.display.flip()

# Quit pygame and exit the program
pygame.quit()
