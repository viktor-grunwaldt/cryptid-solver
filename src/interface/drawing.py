import pygame
import math
from interface.support import odd_q_to_pixel

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
    
def draw_pentagon(screen, pentagon_size, x, y, color):
    pentagon_points = [
        (x + pentagon_size * math.cos(2 * math.pi * i / 5), y + pentagon_size * math.sin(2 * math.pi * i / 5))
        for i in range(5)
    ]
    pygame.draw.polygon(screen, color, pentagon_points)
    
def draw_square(screen, square_size, x, y, color):
    half_size = square_size / 2
    square_points = [
        (x - half_size, y - half_size),
        (x + half_size, y - half_size),
        (x + half_size, y + half_size),
        (x - half_size, y + half_size),
    ]
    pygame.draw.polygon(screen, color, square_points)


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
        pygame.draw.line(
            screen, line_color, points[i], points[(i + 1) % 6], line_length
        )


def draw_small_square(screen, row, col, color, square_size, x_offset, y_offset):
    x, y = odd_q_to_pixel(col, row)
    x += x_offset
    y += y_offset
    square_x = x - square_size // 2
    square_y = y - square_size // 2

    # Draw the black outline first
    outline_size = 2  # You can adjust this value as needed
    outline_x = square_x - outline_size
    outline_y = square_y - outline_size
    outline_width = square_size + outline_size * 2
    outline_height = square_size + outline_size * 2
    pygame.draw.rect(
        screen, (0, 0, 0), (outline_x, outline_y, outline_width, outline_height)
    )

    # Draw the filled square on top of the outline
    pygame.draw.rect(screen, color, (square_x, square_y, square_size, square_size))


def draw_small_circle(screen, row, col, color, circle_size, x_offset, y_offset):
    x, y = odd_q_to_pixel(col, row)
    x += x_offset
    y += y_offset

    # Draw the black outline first
    outline_size = 2  # You can adjust this value as needed
    pygame.draw.circle(screen, (0, 0, 0), (x, y), circle_size + outline_size)

    # Draw the filled circle on top of the outline
    pygame.draw.circle(screen, color, (x, y), circle_size)


def draw_small_triangle(screen, row, col, color, triangle_size, x_offset, y_offset):
    x, y = odd_q_to_pixel(col, row)
    x += x_offset
    y += y_offset

    # Define the points of the triangle
    triangle_points = [
        (x, y - triangle_size),  # Top vertex
        (
            x - triangle_size * math.sqrt(3) / 2,
            y + triangle_size / 2,
        ),  # Bottom-left vertex
        (
            x + triangle_size * math.sqrt(3) / 2,
            y + triangle_size / 2,
        ),  # Bottom-right vertex
    ]

    # Draw the black outline first (optional, you can adjust the outline size)
    outline_size = 2
    pygame.draw.polygon(screen, (0, 0, 0), triangle_points, outline_size)

    # Draw the filled triangle on top of the outline
    pygame.draw.polygon(screen, color, triangle_points)
