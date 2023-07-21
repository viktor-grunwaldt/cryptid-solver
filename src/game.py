import pygame
import math
from buttons import create_button_bundles
from board import Board
from enums import Biome, StructureColor, StructureType, Territory

# Rest of the code remains the same...

# Initialize pygame
pygame.init()

# Define the screen dimensions
screen_width, screen_height = 1400, 1000

# main_board = [
#     ["w", "d", "w", "f"],
#     ["w", "m", "f", "s"],
#     ["d", "m", "w", "d"],
#     ["f", "w", "s", "s"],
# ]

main_board = Board().grid

cols = Board.width
rows = Board.height

small_square_size = 10
small_circle_size = 10
small_triangle_size = 10
small_hexagon_size = 10


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


def draw_small_triangle(screen, row, col, color):
    x, y = odd_q_to_pixel(col, row)
    x += x_offset
    y += y_offset

    # Define the points of the triangle
    triangle_points = [
        (x, y - small_triangle_size),                          # Top vertex
        (x - small_triangle_size * math.sqrt(3) / 2, y + small_triangle_size / 2),  # Bottom-left vertex
        (x + small_triangle_size * math.sqrt(3) / 2, y + small_triangle_size / 2),  # Bottom-right vertex
    ]

    # Draw the black outline first (optional, you can adjust the outline size)
    outline_size = 2
    pygame.draw.polygon(screen, (0, 0, 0), triangle_points, outline_size)

    # Draw the filled triangle on top of the outline
    pygame.draw.polygon(screen, color, triangle_points)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hexagonal Map with Buttons")

# Define button dimensions
button_width, button_height = 100, 40  # Adjust button size as needed

# Define the gap between button bundles and between buttons within a bundle
bundle_gap = 50
button_gap = 20

# Define the size of each hexagon and the gap between hexagons
hex_size = 40
hex_gap = 5

bundle_colors = [
    (223, 66, 59),  # Red
    (253, 201, 27),  # Orange
    (52, 199, 206),  # Cyan
    (174, 228, 255),  # Light blue
    (126, 85, 207),  # Violet
]

# colors = {
#     "w": (0, 0, 255),  # blue for water
#     "d": (244, 164, 96),  # sandy brown for desert
#     "m": (139, 69, 19),  # brown for mountain
#     "s": (128, 0, 128),  # dark purple for swamp
#     "f": (0, 100, 0),  # dark green for forest
# }

colors = {
    Biome.WATER: (97, 150, 202),  # blue for water
    Biome.DESERT: (255, 212, 81),  # sandy brown for desert
    Biome.MOUNTAIN: (185, 185, 185),  # brown for mountain
    Biome.SWAMP: (117, 87, 115),  # dark purple for swamp
    Biome.FOREST: (113, 173, 103),  # dark green for forest
    
    StructureColor.BLACK: (0, 0, 0),      # black
    StructureColor.BLUE: (0, 0, 255),     # blue
    StructureColor.WHITE: (255, 255, 255),# white
    StructureColor.GREEN: (0, 128, 0),    # green

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

def draw_lines_close_to_hexagon_edges(screen, hex_size, x, y, line_length, line_color):
    hex_size = hex_size * 0.8
    points = [
        (x + hex_size, y),
        (x + hex_size / 2, y - math.sqrt(3) / 2 * hex_size),
        (x - hex_size / 2, y - math.sqrt(3) / 2 * hex_size),
        (x - hex_size, y),
        (x - hex_size / 2, y + math.sqrt(3) / 2 * hex_size),
        (x + hex_size / 2, y + math.sqrt(3) / 2 * hex_size),
    ]

    for i in range(6):
        pygame.draw.line(screen, line_color, points[i], points[(i + 1) % 6], line_length)



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
            # print(f'{row}/{rows}', f'{col}/{cols}')
            value = main_board[row][col]
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
                    draw_lines_close_to_hexagon_edges(screen, hex_size, x, y, 2, (255, 0, 0))
                elif value.territory == Territory.BEAR:
                    draw_lines_close_to_hexagon_edges(screen, hex_size, x, y, 2, (0, 0, 0))
            if value.structure is not None:
                if value.structure.type == StructureType.STONE:
                    draw_hexagon(screen, small_hexagon_size, x, y, colors[value.structure.color])
                elif value.structure.type == StructureType.SHACK:
                    draw_small_triangle(screen, row, col, colors[value.structure.color])

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
