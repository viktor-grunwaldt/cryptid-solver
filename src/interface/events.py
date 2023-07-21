import pygame
from interface.support import draw_player_choice, remove_structure
from enums import StructureType, StructureColor
from interface.support import bundle_colors



def key_pressed(main_board, clicked_tile, squares, circles):
    
    # Define the combinations and their corresponding actions here
    combinations = {
        ('r', 't'): lambda: draw_player_choice(clicked_tile, squares, circles, "True", bundle_colors[0]),
        ('r', 'f'): lambda: draw_player_choice(clicked_tile, squares, circles, "False", bundle_colors[0]),
        
        ('y', 't'): lambda: draw_player_choice(clicked_tile, squares, circles, "True", bundle_colors[1]),
        ('y', 'f'): lambda: draw_player_choice(clicked_tile, squares, circles, "False", bundle_colors[1]),
        
        ('c', 't'): lambda: draw_player_choice(clicked_tile, squares, circles, "True", bundle_colors[2]),
        ('c', 'f'): lambda: draw_player_choice(clicked_tile, squares, circles, "False", bundle_colors[2]),
        
        ('b', 't'): lambda: draw_player_choice(clicked_tile, squares, circles, "True", bundle_colors[3]),
        ('b', 'f'): lambda: draw_player_choice(clicked_tile, squares, circles, "False", bundle_colors[3]),
        
        ('v', 't'): lambda: draw_player_choice(clicked_tile, squares, circles, "True", bundle_colors[4]),
        ('v', 'f'): lambda: draw_player_choice(clicked_tile, squares, circles, "False", bundle_colors[4]),
        
        ('w', 'o'): lambda: main_board.add_structure(clicked_tile, StructureColor.WHITE, StructureType.STONE),
        ('b', 'o'): lambda: main_board.add_structure(clicked_tile, StructureColor.BLUE, StructureType.STONE),
        ('g', 'o'): lambda: main_board.add_structure(clicked_tile, StructureColor.GREEN, StructureType.STONE),
        ('k', 'o'): lambda: main_board.add_structure(clicked_tile, StructureColor.BLACK, StructureType.STONE),
        
        ('w', 's'): lambda: main_board.add_structure(clicked_tile, StructureColor.WHITE, StructureType.SHACK),
        ('b', 's'): lambda: main_board.add_structure(clicked_tile, StructureColor.BLUE, StructureType.SHACK),
        ('g', 's'): lambda: main_board.add_structure(clicked_tile, StructureColor.GREEN, StructureType.SHACK),
        ('k', 's'): lambda: main_board.add_structure(clicked_tile, StructureColor.BLACK, StructureType.SHACK),
        
        ('c', 's'): lambda: remove_structure(clicked_tile),
    }
    
    keys_pressed = pygame.key.get_pressed()
    button_combination = [
        'r' if keys_pressed[pygame.K_r] else '',
        'y' if keys_pressed[pygame.K_y] else '',
        'c' if keys_pressed[pygame.K_c] else '',
        'b' if keys_pressed[pygame.K_b] else '',
        'v' if keys_pressed[pygame.K_v] else '',
        't' if keys_pressed[pygame.K_t] else '',
        'f' if keys_pressed[pygame.K_f] else '',
        
        'w' if keys_pressed[pygame.K_w] else '',
        'g' if keys_pressed[pygame.K_g] else '',
        'k' if keys_pressed[pygame.K_k] else '',
        
        's' if keys_pressed[pygame.K_s] else '',
        'o' if keys_pressed[pygame.K_o] else '',
        
    ]
    button_combination = tuple(filter(None, button_combination))
    print(button_combination)
    # Check if the current button combination is in the combinations dictionary
    if button_combination in combinations:
        combinations[button_combination]()  # Execute the corresponding action