import pygame # Import Pygame library
import sys # Import sys for system-specific parameters and functions
import time # Import time for time-related functions
from grid import (
    Box, make_grid, recolor_path,
    ROWS, COLS,
    WHITE, BLACK, GREY, GREEN, RED, TURQUOISE, PURPLE, ORANGE
)

pygame.init() # Initialize Pygame

WINDOW_WIDTH = 700 # Width of the window
WINDOW_HEIGHT = 700 # Height of the window

box_width = WINDOW_WIDTH // COLS # Width of each box
box_height = WINDOW_HEIGHT // ROWS # Height of each box

# Manhattan distance
def heuristic(a, b): 
    return abs(a.row - b.row) + abs(a.col - b.col)

# A*'s algorithm implementation
def A_Star_Algorithm(draw, grid, start, end):
    start_time = time.time()
    count = 0
    open_set = []
    open_set.append((0, count, start))
    came_from = {}

    g_score = {box: float("inf") for row in grid for box in row}
    g_score[start] = 0

    f_score = {box: float("inf") for row in grid for box in row}
    f_score[start] = heuristic(start, end)

    open_set_hash = {start}

    while open_set:
        open_set.sort(key=lambda x: x[0])
        current = open_set.pop(0)[2]
        open_set_hash.remove(current)

        if current == end:
            recolor_path(came_from, end, draw)
            end.set_end()
            start.set_start()
            elapsed_time = time.time() - start_time
            return round(elapsed_time, 3)

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + current.weight

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor, end)

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.append((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.color = GREEN

        draw()

        if current != start:
            current.color = RED

    return False

# Function to get the position of the mouse click
def get_clicked_pos(pos):
    x, y = pos
    row = y // box_height
    col = x // box_width

    row = max(0, min(row, ROWS - 1))
    col = max(0, min(col, COLS - 1))
    return row, col

def main(): # Main function to run the visualization
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("A*'s Algorithm Visualization")
    elapsed_time = None
    font = pygame.font.SysFont("Arial", 24)
    grid = make_grid()
    start = end = None
    running = True

    def draw():
        screen.fill(WHITE)
        for row in grid:
            for box in row:
                rect = pygame.Rect(
                    box.col * box_width,
                    box.row * box_height,
                    box_width,
                    box_height
                )
                pygame.draw.rect(screen, box.color, rect)
        for i in range(ROWS + 1):
            pygame.draw.line(screen, GREY, (0, i * box_height), (WINDOW_WIDTH, i * box_height))
        for j in range(COLS + 1):
            pygame.draw.line(screen, GREY, (j * box_width, 0), (j * box_width, WINDOW_HEIGHT))

        if elapsed_time is not None:
            text = font.render(f"Time: {elapsed_time} sec", True, BLACK)
            screen.blit(text, (10, 10))

        pygame.display.update()


    while running:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row_list in grid:
                        for box in row_list:
                            box.update_neighbors(grid)
                    elapsed_time = A_Star_Algorithm(draw, grid, start, end)

                if event.key == pygame.K_c:
                    start = end = None
                    grid = make_grid()

        if pygame.mouse.get_pressed()[0]:  # Left click
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos)
            box = grid[row][col]
            if not start and box != end and not box.is_wall:
                start = box
                start.set_start()
            elif not end and box != start and not box.is_wall:
                end = box
                end.set_end()
            elif box != end and box != start:
                box.set_wall()

        elif pygame.mouse.get_pressed()[2]:  # Right click
            pos = pygame.mouse.get_pos()
            row, col = get_clicked_pos(pos)
            box = grid[row][col]
            was_start = (box == start)
            was_end = (box == end)
            box.reset()
            if was_start:
                start = None
            if was_end:
                end = None

    pygame.quit()

# Run the main function
if __name__ == "__main__":
    main()