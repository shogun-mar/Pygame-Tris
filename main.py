from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' #Hides the welcome message of pygame
import pygame, random #Importing pygame has to be done after modifying the environment variable

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGTH = 600, 600
CELL_WIDTH, CELL_HEIGTH = SCREEN_WIDTH // 3, SCREEN_HEIGTH // 3
MAX_FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
clock = pygame.time.Clock()
pygame.display.set_caption("Tris")
pygame.display.set_icon(pygame.image.load('window_icon.png').convert_alpha())
is_player_one_turn = True #Bool variable to control the switching of turns
grid = [[0, 0, 0], 
        [0, 0, 0],
        [0, 0, 0]] # 0 = empty, 1 = player 1, 2 = player 2

#end screens
player_one_win_text = pygame.font.SysFont('Arial', 50).render('Player 1 wins!', True, 'white')
player_two_win_text = pygame.font.SysFont('Arial', 50).render('Player 2 wins!', True, 'white')
draw_text = pygame.font.SysFont('Arial', 50).render('Draw!', True, 'white')
end_message_rect = player_one_win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGTH//2 - 50))

# Draw grid
colors = 'greenyellow goldenrod2 fuchsia deeppink4 cornflowerblue darkred darkslategrey blueviolet mediumpurple3 indigo crimson seagreen1 salmon1 purple2 plum3 palevioletred violetred springgreen4 \
                          steelblue4 steelblue slateblue4 slateblue sienna2 cyan skyblue purple magenta red green blue yellow \
                          white'.split()
selected_color = random.choice(colors)
screen.fill(selected_color)
for i in range(1, 3):
    pygame.draw.line(screen, 'white', (i*200, 0), (i*200, SCREEN_HEIGTH), 5)
    pygame.draw.line(screen, 'white', (0, i*200), (SCREEN_WIDTH, i*200), 5)

def find_cell(x, y):
    return (int(x // (CELL_WIDTH)), int(y // (CELL_HEIGTH)))

def quit_game():
    pygame.quit()
    exit()

def handle_mouse_input():
    global is_player_one_turn
    x, y = pygame.mouse.get_pos()
    selected_cell = find_cell(x, y)
    if grid[selected_cell[1]][selected_cell[0]] == 0:
        grid[selected_cell[1]][selected_cell[0]] = 1 if is_player_one_turn else 2
        is_player_one_turn = not is_player_one_turn
    return selected_cell

def update_visualized_grid(selected_cell):
    x = selected_cell[0] * 200
    y = selected_cell[1] * 200
    if grid[selected_cell[1]][selected_cell[0]] == 1:
        pygame.draw.line(screen, 'white', (x, y), (x+CELL_WIDTH, y+CELL_HEIGTH), 5)
        pygame.draw.line(screen, 'white', (x+CELL_WIDTH, y), (x, y+CELL_HEIGTH), 5)
    elif grid[selected_cell[1]][selected_cell[0]] == 2:
        pygame.draw.circle(screen, 'white', (x+100, y+100), 100, 5)

def check_victory(grid):
    # Check rows
    for row in grid:
        if len(set(row)) == 1 and row[0] != 0:
            return row[0]

    # Check columns
    for col in zip(*grid):
        if len(set(col)) == 1 and col[0] != 0:
            return col[0]

    # Check diagonals
    if len({grid[i][i] for i in range(3)}) == 1 and grid[0][0] != 0:
        return grid[0][0]
    if len({grid[i][2-i] for i in range(3)}) == 1 and grid[0][2] != 0:
        return grid[0][2]

    # Check for draw if all cells are filled
    if all(cell != 0 for row in grid for cell in row):
        return 'Draw'

    return 'Continue'

def show_end_screen(result):
    screen.fill(selected_color)
    if result == 1:
        screen.blit(player_one_win_text, end_message_rect)
    elif result == 2:
        screen.blit(player_two_win_text, end_message_rect)
    else:
        screen.blit(draw_text, end_message_rect)
    pygame.display.flip()
    pygame.time.wait(3000)
    quit_game()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: quit_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
           selected_cell = handle_mouse_input()
           update_visualized_grid(selected_cell)
           result = check_victory(grid)
           if result != 'Continue':
               show_end_screen(result)

    pygame.display.flip()
    clock.tick(60)

    
