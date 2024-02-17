import pygame
import sys
import os
from pygame.locals import *
import solver
from pygame_menu import Menu, themes


def main():
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((500, 300))

    pygame.display.set_caption("Cryptid Solver")

    # Set up fonts
    font = pygame.font.Font(None, 36)

    # Set up colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Initial number of players
    num_players = 3
    difficulty = 1

    # Create a menu
    menu = Menu("Cryptid Solver", 500, 300, theme=themes.THEME_BLUE)

    # Function to set the number of players
    def set_num_players(value):
        nonlocal num_players
        num_players = value
    def set_difficulty(value):
        nonlocal difficulty
        difficulty = value

    # Add a dropdown for number of players
    menu.add.selector("Number of Players: ", [('2', 2), ('3', 3), ('4', 4), ('5', 5)], onchange=lambda _, value: set_num_players(value), default=1)
    menu.add.selector('Difficulty :', [('Easy', 1), ('Hard', 2)], onchange=lambda _, value: set_difficulty(value), default=0)
    # Function to start the game
    def start_game():
        solver.create_board(num_players, difficulty)
        menu.disable()

    # Add a confirm button
    menu.add.button("Confirm", start_game)

    

    

    while True:
        screen.fill(white)

        # Draw the menu
        events = pygame.event.get()
        menu.update(events)
        menu.draw(screen)

        pygame.display.flip()

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
