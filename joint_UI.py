import pygame
from BFS import BFS_algorithm
from Dijkstra import dijkstra_algorithm
from A_Star import A_Star_Algorithm
from grid import (
    Box, make_grid, expanded_and_path,
    ROWS, COLS,
    WHITE, BLACK, GREY
)

pygame.init()

# Base layout dimensions
BASE_PANEL_WIDTH = 400
BASE_PANEL_HEIGHT = 500
BASE_LABEL_HEIGHT = 50
BASE_BOTTOM_HEIGHT = 70
BASE_SPACING = 20

ASPECT_RATIO = 2.0  # width = 2 * height

# Mutable dimensions (update on resize)
PANEL_WIDTH = BASE_PANEL_WIDTH
PANEL_HEIGHT = BASE_PANEL_HEIGHT
LABEL_HEIGHT = BASE_LABEL_HEIGHT
BOTTOM_STATS_HEIGHT = BASE_BOTTOM_HEIGHT
PANEL_SPACING = BASE_SPACING

screen = pygame.display.set_mode((1240, 620), pygame.RESIZABLE)
pygame.display.set_caption("BFS | Dijkstra | A* Comparison")

# Colors
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)


# Handle resizing and maintain aspect ratio
def handle_resize(event_w, event_h):
    global PANEL_WIDTH, PANEL_HEIGHT, LABEL_HEIGHT, BOTTOM_STATS_HEIGHT, PANEL_SPACING

    new_h = event_h
    new_w = int(new_h * ASPECT_RATIO)

    pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)

    scale = new_h / 620

    PANEL_WIDTH = int(BASE_PANEL_WIDTH * scale)
    PANEL_HEIGHT = int(BASE_PANEL_HEIGHT * scale)
    LABEL_HEIGHT = int(BASE_LABEL_HEIGHT * scale)
    BOTTOM_STATS_HEIGHT = int(BASE_BOTTOM_HEIGHT * scale)
    PANEL_SPACING = int(BASE_SPACING * scale)

# X offset for each panel
def panel_x(panel_index):
    return panel_index * (PANEL_WIDTH + PANEL_SPACING)


# Draw a centered letterboxed grid
def draw_panel(grid, panel_index):
    x_offset = panel_x(panel_index)

    # Compute cell dimensions
    box_w = PANEL_WIDTH // COLS
    box_h = PANEL_HEIGHT // ROWS
    cell = min(box_w, box_h)

    used_w = cell * COLS
    used_h = cell * ROWS

    # Letterbox padding
    pad_x = x_offset + (PANEL_WIDTH - used_w) // 2
    pad_y = LABEL_HEIGHT + (PANEL_HEIGHT - used_h) // 2

    # Draw cells
    for row in grid:
        for box in row:
            rect = pygame.Rect(
                pad_x + box.col * cell,
                pad_y + box.row * cell,
                cell, cell
            )
            pygame.draw.rect(screen, box.color, rect)

    # Draw grid lines
    for i in range(ROWS + 1):
        pygame.draw.line(
            screen, GREY,
            (pad_x, pad_y + i * cell),
            (pad_x + used_w, pad_y + i * cell)
        )

    for j in range(COLS + 1):
        pygame.draw.line(
            screen, GREY,
            (pad_x + j * cell, pad_y),
            (pad_x + j * cell, pad_y + used_h)
        )

# Draw panel labels
def draw_labels():
    font = pygame.font.SysFont("Arial", 28, bold=True)
    labels = ["BFS", "Dijkstra", "A*"]

    for i, text in enumerate(labels):
        center_x = panel_x(i) + PANEL_WIDTH // 2
        surf = font.render(text, True, BLACK)
        rect = surf.get_rect(center=(center_x, LABEL_HEIGHT // 2))
        screen.blit(surf, rect)

def draw_stats(timers, expanded, path_lengths):
    font = pygame.font.SysFont("Arial", 20)
    labels = ["BFS", "Dijkstra", "A*"]

    for i, label in enumerate(labels):
        center_x = panel_x(i) + PANEL_WIDTH // 2
        y_base = LABEL_HEIGHT + PANEL_HEIGHT + 10

        # Time
        if timers[i] is not None:
            t_string = f"Time: {timers[i]:.3f}s"
            t_color = BLACK
        else:
            t_string = "Time: --"
            t_color = GREY
        surf = font.render(t_string, True, t_color)
        rect = surf.get_rect(center=(center_x, y_base))
        screen.blit(surf, rect)

        # Expanded
        if expanded[i] is not None:
            e_string = f"Expanded: {expanded[i]}"
            e_color = BLACK
        else:
            e_string = "Expanded: --"
            e_color = GREY
        surf = font.render(e_string, True, e_color)
        rect = surf.get_rect(center=(center_x, y_base + 25))
        screen.blit(surf, rect)

        # Path Length
        if path_lengths[i] is not None:
            p_string = f"Path Length: {path_lengths[i]}"
            p_color = BLACK
        else:
            p_string = "Path Length: --"
            p_color = GREY
        surf = font.render(p_string, True, p_color)
        rect = surf.get_rect(center=(center_x, y_base + 50))
        screen.blit(surf, rect)


# Map mouse click into centered grid
def get_center_grid_pos(mx, my):
    panel_index = 1
    x_offset = panel_x(panel_index)

    cell = min(PANEL_WIDTH // COLS, PANEL_HEIGHT // ROWS)
    used_w = cell * COLS
    used_h = cell * ROWS

    pad_x = x_offset + (PANEL_WIDTH - used_w) // 2
    pad_y = LABEL_HEIGHT + (PANEL_HEIGHT - used_h) // 2

    # Must click inside the grid area
    if not (pad_x <= mx < pad_x + used_w and
            pad_y <= my < pad_y + used_h):
        return None

    local_x = mx - pad_x
    local_y = my - pad_y

    col = local_x // cell
    row = local_y // cell

    if 0 <= row < ROWS and 0 <= col < COLS:
        return row, col
    return None

# Apply edits (set start, end, wall, reset) to all three grids
def apply_edit(row, col, button, start, end, g1, g2, g3):
    boxes = [g1[row][col], g2[row][col], g3[row][col]]

    if button == 1:  # left click
        # Set start
        if start is None and not boxes[0].is_wall:
            for b in boxes:
                b.set_start()
            return (row, col), end

        # Set end
        if end is None and not boxes[0].is_wall and (row, col) != start:
            for b in boxes:
                b.set_end()
            return start, (row, col)

        # Set wall
        if (row, col) != start and (row, col) != end:
            for b in boxes:
                b.set_wall()

    elif button == 3:  # right
        for b in boxes:
            b.reset()

        if start == (row, col):
            start = None
        if end == (row, col):
            end = None

    return start, end

# Main function to run the visualization
def main(): 
    running = True

    bfs_grid = make_grid()
    dij_grid = make_grid()
    astar_grid = make_grid()

    start = None
    end = None
    
    # Store stats for each algorithm [BFS, Dijkstra, A*]
    timers = [None, None, None]
    expanded = [None, None, None]
    path_lengths = [None, None, None]

    while running:
        screen.fill(WHITE)
        draw_labels()

        draw_panel(bfs_grid, 0)
        draw_panel(dij_grid, 1)
        draw_panel(astar_grid, 2)
        
        draw_stats(timers, expanded, path_lengths)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.VIDEORESIZE:
                handle_resize(event.w, event.h)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    
                    # Convert stored coords into actual Box objects
                    sr, sc = start
                    er, ec = end

                    bfs_start  = bfs_grid[sr][sc]
                    bfs_end    = bfs_grid[er][ec]
                    dij_start  = dij_grid[sr][sc]
                    dij_end    = dij_grid[er][ec]
                    ast_start  = astar_grid[sr][sc]
                    ast_end    = astar_grid[er][ec]

                    # Define per-panel draw functions
                    def draw_bfs():
                        screen.fill(WHITE)
                        draw_labels()
                        draw_panel(bfs_grid, 0)
                        draw_panel(dij_grid, 1)
                        draw_panel(astar_grid, 2)
                        draw_stats(timers, expanded, path_lengths)
                        pygame.display.update()

                    def draw_dij():
                        screen.fill(WHITE)
                        draw_labels()
                        draw_panel(bfs_grid, 0)
                        draw_panel(dij_grid, 1)
                        draw_panel(astar_grid, 2)
                        draw_stats(timers, expanded, path_lengths)
                        pygame.display.update()

                    def draw_ast():
                        screen.fill(WHITE)
                        draw_labels()
                        draw_panel(bfs_grid, 0)
                        draw_panel(dij_grid, 1)
                        draw_panel(astar_grid, 2)
                        draw_stats(timers, expanded, path_lengths)
                        pygame.display.update()

                    # Update neighbors for all grids before running algorithms
                    for r in range(ROWS):
                        for c in range(COLS):
                            bfs_grid[r][c].update_neighbors(bfs_grid)
                            dij_grid[r][c].update_neighbors(dij_grid)
                            astar_grid[r][c].update_neighbors(astar_grid)

                    # Run all three algorithms and capture stats
                    timers[0] = BFS_algorithm(draw_bfs, bfs_grid, bfs_start, bfs_end)
                    expanded[0], path_lengths[0] = expanded_and_path(bfs_grid)

                    timers[1] = dijkstra_algorithm(draw_dij, dij_grid, dij_start, dij_end)
                    expanded[1], path_lengths[1] = expanded_and_path(dij_grid)

                    timers[2] = A_Star_Algorithm(draw_ast, astar_grid, ast_start, ast_end)
                    expanded[2], path_lengths[2] = expanded_and_path(astar_grid)

                if event.key == pygame.K_r:
                    # Reset grids and start/end points
                    bfs_grid = make_grid()
                    dij_grid = make_grid()
                    astar_grid = make_grid()
                    start = None
                    end = None
                    timers = [None, None, None]  # Reset timers
                    expanded = [None, None, None] # Reset expanded nodes
                    path_lengths = [None, None, None] # Reset path length


        # Mouse editing (center panel only)
        mouse = pygame.mouse.get_pressed()
        if mouse[0] or mouse[2]:
            mx, my = pygame.mouse.get_pos()
            pos = get_center_grid_pos(mx, my)
            if pos is not None:
                row, col = pos
                start, end = apply_edit(
                    row, col,
                    1 if mouse[0] else 3,
                    start, end,
                    bfs_grid, dij_grid, astar_grid
                )

    pygame.quit()

#  Main entry point
if __name__ == "__main__":
    main()
