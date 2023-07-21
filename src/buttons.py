import pygame

# Function to create a button with a given color, position, and label
def create_button(screen, x, y, width, height, color, label):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, button_rect)
    font = pygame.font.Font(None, 36)
    text = font.render(label, True, (255, 255, 255))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)
    return button_rect

# Function to create button bundles and return their rectangles
def create_button_bundle(screen, bundle_x, bundle_y, button_width, button_height, button_gap, bundle_color):
    button_rectangles = []
    font = pygame.font.Font(None, 24)
    
    for index, label in enumerate(["True", "False"]):
        button_x = bundle_x + (button_width + button_gap) * index
        button_y = bundle_y
        pygame.draw.rect(screen, bundle_color, (button_x, button_y, button_width, button_height))
        text = font.render(label, True, (255, 255, 255))
        text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(text, text_rect)
        button_rectangles.append(pygame.Rect(button_x, button_y, button_width, button_height))
    
    return button_rectangles

def create_button_bundles(screen, button_width, button_height, button_gap, bundle_gap, bundle_colors):
    button_rectangles_list = []
    bundle_x = bundle_gap
    bundle_y = screen.get_height() - button_height - bundle_gap

    for bundle_color in bundle_colors:
        button_rectangles = create_button_bundle(screen, bundle_x, bundle_y, button_width, button_height, button_gap, bundle_color)
        button_rectangles_list.append(button_rectangles)
        bundle_x += len(button_rectangles) * (button_width + button_gap)

    return button_rectangles_list

def create_left_side_button_bundle(screen):
    button_width = 100
    button_height = 50
    button_gap = 10
    bundle_gap = 20
    bundle_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

    # Create two columns and four rows of button bundles
    create_button_bundles(screen, button_width, button_height, button_gap, bundle_gap, bundle_colors[:2])
    create_button_bundles(screen, button_width, button_height, button_gap, bundle_gap + (button_height + button_gap) * 2, bundle_colors[2:])
