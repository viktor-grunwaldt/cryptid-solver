import pygame
import pygame_menu

# Initialize Pygame
pygame.init()

# Set up display
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Grid with Selector Boxes and Checkboxes")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create a Pygame_menu theme
theme = pygame_menu.themes.THEME_SOLARIZED.copy()

# Create Pygame_menu
menu = pygame_menu.Menu("Grid Menu", width, height, theme=theme)


# Function to print the selected values and checkboxes
def print_values():
    print("Selected values:")
    for row in range(2):
        for col in range(3):
            selector_value = menu.get_widget(f"selector_{row}_{col}").get_value()[0][0]
            checkbox_value = menu.get_widget(
                f"selector_{row}_{col}_checkbox"
            ).get_value()[0]
            print(
                f"Row {row + 1}, Column {col + 1}: Selector - {selector_value}, Checkbox - {checkbox_value}"
            )


# Add cells to the menu
for row in range(2):
    for col in range(3):
        # Add selector box (with a single option to simulate checkbox behavior)
        selector = menu.add.selector(
            f"Selector {row + 1},{col + 1}:",
            [("1", 1)],
            default=0,
            onchange=None,
            selector_id=f"selector_{row}_{col}",
        )

        # Add checkbox (simulated with a single option selector)
        checkbox = menu.add.selector(
            f"Checkbox {row + 1},{col + 1}",
            [("False", False), ("True", True)],
            default=0,
            selector_id=f"selector_{row}_{col}_checkbox",
        )

# Add a button to print values
menu.add.button("Print Values", print_values)

# Run the menu
menu.mainloop(screen)

# Quit Pygame
pygame.quit()
