import pygame
import sys
import project1 as algorithms

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

GRID_LENGTH = 8
BLOCK_HEIGHT = round(SCREEN_HEIGHT/GRID_LENGTH)
BLOCK_WIDTH = round(SCREEN_WIDTH/GRID_LENGTH)

BLACK = (0, 0, 0)
ORANGE = (252, 103, 28)
BRIGHTORANGE = (254, 159, 0)
GREEN = (2, 168, 2)
BRIGHTGREEN = (7, 250, 7)
PURPLE = (132, 2, 168)
BRIGHTPURPLE = (220, 94, 255)
PINK = (227, 25, 176)
BLUE = (4, 106, 222)
WHITE = (255, 255, 255)

def initialize_game():
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface.fill(BLACK)
    return surface


def get_square_color(square):
    square_color = BLACK
    if square == "wh":
        square_color = WHITE
    if square == "or":
        square_color = ORANGE
    if square == "gr":
        square_color = GREEN
    if square == "pu":
        square_color = PURPLE
    if square == "bor":
        square_color = BRIGHTORANGE
    if square == "bgr":
        square_color = BRIGHTGREEN
    if square == "bpu":
        square_color = BRIGHTPURPLE
    if square == "pi":
        square_color = PINK
    if square == "bl":
        square_color = BLUE
    return square_color

def draw_grid(surface, grid_colors):
    for j in range(GRID_LENGTH):
        for i in range(GRID_LENGTH):
            my_rect = pygame.Rect(i*BLOCK_WIDTH, j*BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT)
            pygame.draw.rect(surface, get_square_color(grid_colors[j][i]), my_rect)
    for i in range(GRID_LENGTH):
        new_height = round(i * BLOCK_HEIGHT)
        new_width = round(i * BLOCK_WIDTH)
        pygame.draw.line(surface, BLACK, (0, new_height), (SCREEN_WIDTH, new_height), 1)
        pygame.draw.line(surface, BLACK, (new_width, 0), (new_width, SCREEN_HEIGHT), 1)

def get_optimal_path(grid_colors):
    all_bfs_paths = algorithms.bfs(algorithms.start_state, algorithms.goal_state, grid_colors)
    bfs_shortest_path = None
    bfs_shortest_path_length = None

    if all_bfs_paths:
        for color, bfs_path in all_bfs_paths:
            if bfs_shortest_path_length == None or len(bfs_path) < bfs_shortest_path_length:
                bfs_shortest_path = bfs_path
                bfs_shortest_path_length = len(bfs_shortest_path)
    return bfs_shortest_path

def gameloop(surface, grid_colors):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    optimal_path = get_optimal_path(grid_colors)
                    for node in optimal_path:
                        if grid_colors[node[0]][node[1]] != "wh":
                            grid_colors[node[0]][node[1]] = "b" + grid_colors[node[0]][node[1]]
        draw_grid(surface, grid_colors)
        pygame.display.update()


surface = initialize_game()
gameloop(surface, algorithms.grid_colors2)