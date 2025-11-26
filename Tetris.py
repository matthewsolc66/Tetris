# Importing necessary modules
import sys
import random
from tkinter import font
import pygame
import time

# Drawing the game window
pygame.init()
WIDTH, HEIGHT = 500, 900
MIN_WIDTH, MIN_HEIGHT = 500, 900
GRID_WIDTH, GRID_HEIGHT = 10, 20
BORDER = 2
TOP_SPACE = 100
BOTTOM_SPACE = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Matthew's Tetris")

# SHAPES and COLORS can be defined here for Tetronimos
SHAPES = [
    # I-piece rotations
    [[(0, 0), (1, 0), (2, 0), (3, 0)], [(0, 0), (0, 1), (0, 2), (0, 3)]],
    # O-piece (no rotation)
    [[(0, 0), (1, 0), (0, 1), (1, 1)]],
    # T-piece rotations
    [[(0, 0), (1, 0), (2, 0), (1, 1)], [(1, 0), (1, 1), (1, 2), (0, 1)], [(0, 1), (1, 1), (2, 1), (1, 0)], [(1, 0), (1, 1), (1, 2), (2, 1)]],
    # S-piece rotations
    [[(1, 0), (2, 0), (0, 1), (1, 1)], [(0, 0), (0, 1), (1, 1), (1, 2)]],
    # Z-piece rotations
    [[(0, 0), (1, 0), (1, 1), (2, 1)], [(1, 0), (1, 1), (0, 1), (0, 2)]],
    # J-piece rotations
    [[(0, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (1, 2), (0, 2)], [(0, 0), (1, 0), (2, 0), (2, 1)], [(1, 0), (0, 0), (0, 1), (0, 2)]],
    # L-piece rotations
    [[(2, 0), (0, 1), (1, 1), (2, 1)], [(1, 0), (1, 1), (1, 2), (2, 2)], [(0, 0), (1, 0), (2, 0), (0, 1)], [(0, 0), (1, 0), (1, 1), (1, 2)]]
]
COLORS = [
    (0, 255, 255),  # Cyan for I
    (255, 255, 0),  # Yellow for O
    (128, 0, 128),  # Purple for T
    (0, 255, 0),    # Green for S
    (255, 0, 0),    # Red for Z
    (0, 0, 255),    # Blue for J
    (255, 165, 0)   # Orange for L
]

# Initial variables
CELL_SIZE = 0
grid_pixel_width = 0
grid_pixel_height = 0 
grid_x_offset = 0
grid_y_offset = 0
score = 0
elapsed_time = 0
current_piece_shape = None
current_piece_pos = [GRID_WIDTH // 2, 0]
board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]  # 0 = empty, 1-7 = shape index +1
fall_speed = 30  # Frames between drops (adjust for difficulty)
fall_counter = 0
current_rotation = 0
next_piece_shape = random.randint(0, len(SHAPES) - 1)
held_piece_shape = None
game_over = False

# Setting up the clock for frame rate
clock = pygame.time.Clock()
start_time = time.time()

#Defining Functions
def handle_events():
    global WIDTH, HEIGHT, current_rotation, current_piece_pos, held_piece_shape, current_piece_shape, next_piece_shape, game_over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            WIDTH = max(event.w, MIN_WIDTH)
            HEIGHT = max(event.h, MIN_HEIGHT)
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            calculate_grid()
        elif event.type == pygame.KEYDOWN:
            if current_piece_shape is None:
                return
            if event.key == pygame.K_LEFT and can_move(-1, 0):
                current_piece_pos[0] -= 1
            elif event.key == pygame.K_RIGHT and can_move(1, 0):
                current_piece_pos[0] += 1
            elif event.key == pygame.K_DOWN and can_move(0, 1):
                current_piece_pos[1] += 1
            elif event.key == pygame.K_UP:  # Rotate
                if current_piece_shape is not None:
                    new_rot = (current_rotation + 1) % len(SHAPES[current_piece_shape])
                    old_rot = current_rotation
                    current_rotation = new_rot
                    if not can_move(0, 0):  # Check if fits
                        current_rotation = old_rot
            elif event.key == pygame.K_c: # Hold piece
                if current_piece_shape is not None:
                    global held_piece_shape
                    if held_piece_shape is None:
                        held_piece_shape = current_piece_shape
                        current_piece_shape = next_piece_shape
                        next_piece_shape = random.randint(0, len(SHAPES) - 1)
                    else:
                        temp = current_piece_shape
                        current_piece_shape = held_piece_shape
                        held_piece_shape = temp
                    current_piece_pos = [GRID_WIDTH // 2, 0]  
                    current_rotation = 0
            elif event.key == pygame.K_r and game_over:
                board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                score = 0
                current_piece_shape = None
                held_piece_shape = None
                next_piece_shape = random.randint(0, len(SHAPES) - 1)
                game_over = False
                start_time = time.time()

def calculate_grid():
    global CELL_SIZE, grid_pixel_width, grid_pixel_height, grid_x_offset, grid_y_offset
    # Calculate available space for the grid
    available_width = WIDTH - 2 * BORDER
    available_height = HEIGHT - TOP_SPACE - BOTTOM_SPACE - 2 * BORDER
    CELL_SIZE = min(available_width // GRID_WIDTH, available_height // GRID_HEIGHT)
    grid_pixel_width = GRID_WIDTH * CELL_SIZE
    grid_pixel_height = GRID_HEIGHT * CELL_SIZE
    # Center the grid in the available space
    grid_x_offset = BORDER + (available_width - grid_pixel_width) // 2
    grid_y_offset = TOP_SPACE + BORDER + (available_height - grid_pixel_height) // 2

def can_move(dx, dy):
    shape = SHAPES[current_piece_shape][current_rotation]
    for dx2, dy2 in shape:
        x = current_piece_pos[0] + dx2 + dx
        y = current_piece_pos[1] + dy2 + dy
        if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or (y >= 0 and board[y][x] != 0):
            return False
    return True

def lock_piece():
    shape = SHAPES[current_piece_shape][current_rotation]
    for dx, dy in shape:
        x = current_piece_pos[0] + dx
        y = current_piece_pos[1] + dy
        if y >= 0:
            board[y][x] = current_piece_shape + 1  # Store shape index

def check_lines():
    global score, board
    lines_cleared = 0
    for y in range(GRID_HEIGHT):
        if all(board[y][x] != 0 for x in range(GRID_WIDTH)):
            # Clear the row
            del board[y]
            board.insert(0, [0] * GRID_WIDTH)  # Add empty row at top
            lines_cleared += 1
    if lines_cleared > 0:
        score += lines_cleared * 100  # 100 points per line

def update():
    global elapsed_time, current_piece_shape, current_piece_pos, fall_counter, current_rotation, next_piece_shape, score, held_piece_shape, game_over
    elapsed_time = time.time() - start_time
    if current_piece_shape is not None:
        fall_counter += 1
        if fall_counter >= fall_speed:
            fall_counter = 0
            if can_move(0, 1):  # Try move down
                current_piece_pos[1] += 1
            else:
                lock_piece()
                check_lines()
                current_piece_shape = None  # Spawn new piece next frame
    else:
        # Spawn new piece
        current_piece_shape = next_piece_shape
        next_piece_shape = random.randint(0, len(SHAPES) - 1)
        current_piece_pos = [GRID_WIDTH // 2, 0]
        current_rotation = 0
        if not can_move(0, 0):
            game_over = True

def render():
    global current_piece_shape, current_piece_pos, current_rotation, held_piece_shape
    screen.fill((0, 0, 0))
    #Draws vertical grid lines
    for x in range(GRID_WIDTH + 1):
        start_pos = (grid_x_offset + x * CELL_SIZE, grid_y_offset)
        end_pos = (grid_x_offset + x * CELL_SIZE, grid_y_offset + grid_pixel_height)
        pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos)
    #Draws horizontal grid lines
    for y in range(GRID_HEIGHT + 1):
        start_pos = (grid_x_offset, grid_y_offset + y * CELL_SIZE)
        end_pos = (grid_x_offset + grid_pixel_width, grid_y_offset + y * CELL_SIZE)
        pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos)
    # Draw score and timer
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, HEIGHT - BOTTOM_SPACE + 10))
    timer_text = font.render(f"Time: {int(elapsed_time)}s", True, (255, 255, 255))
    screen.blit(timer_text, (WIDTH - 150, HEIGHT - BOTTOM_SPACE + 10))
   # Draw next piece
    next_text = font.render("Next:", True, (255, 255, 255))
    screen.blit(next_text, (10, 10))
    if next_piece_shape is not None:
        next_shape = SHAPES[next_piece_shape][0]  # First rotation
        next_color = COLORS[next_piece_shape]
        preview_size = CELL_SIZE // 2
        for dx, dy in next_shape:
            nx = 10 + dx * preview_size  # Move further left
            ny = 50 + dy * preview_size  # Adjust y if needed
            pygame.draw.rect(screen, next_color, (nx, ny, preview_size, preview_size))
    # Draw held piece
    hold_text = font.render("Hold:", True, (255, 255, 255))
    screen.blit(hold_text, (WIDTH - 150, 10))  # Top right
    if held_piece_shape is not None:
        held_shape = SHAPES[held_piece_shape][0]
        held_color = COLORS[held_piece_shape]
        for dx, dy in held_shape:
            hx = WIDTH - 140 + dx * preview_size
            hy = 50 + dy * preview_size
            pygame.draw.rect(screen, held_color, (hx, hy, preview_size, preview_size))
    # Draw Tetronimo
    if current_piece_shape is not None:
        shape = SHAPES[current_piece_shape][current_rotation]
        color = COLORS[current_piece_shape]
        for dx, dy in shape:
            x = grid_x_offset + (current_piece_pos[0] + dx) * CELL_SIZE
            y = grid_y_offset + (current_piece_pos[1] + dy) * CELL_SIZE
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if board[y][x] != 0:
                color = COLORS[board[y][x] - 1]
                px = grid_x_offset + x * CELL_SIZE
                py = grid_y_offset + y * CELL_SIZE
                pygame.draw.rect(screen, color, (px, py, CELL_SIZE, CELL_SIZE))
    if game_over:
        game_over_text = font.render("GAME OVER! Press R to Restart", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 -150, HEIGHT // 2))
    pygame.display.flip()

calculate_grid()

while True: handle_events(); update(); render(); clock.tick(60);

