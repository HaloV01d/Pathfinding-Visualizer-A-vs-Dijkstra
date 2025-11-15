import pygame
from BFS import BFS_algorithm, Box
from Dijkstra import dijkstra_algorithm
from A_Star import A_Star_Algorithm

pygame.init()

# Panel and window settings
PANEL_WIDTH = 400
PANEL_HEIGHT = 500
LABEL_HEIGHT = 50
BOTTOM_STATS_HEIGHT = 70
PANEL_SPACING = 20

WINDOW_WIDTH = PANEL_WIDTH * 3 + PANEL_SPACING * 2
WINDOW_HEIGHT = LABEL_HEIGHT + PANEL_HEIGHT + BOTTOM_STATS_HEIGHT

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("BFS | Dijkstra | A* Comparison")

# Colors
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

# Grid settings
ROWS = 25
COLS = 25
BOX_WIDTH = PANEL_WIDTH // COLS
BOX_HEIGHT = PANEL_HEIGHT // ROWS


# Make a clean grid
def make_grid():
    grid = []
    for r in range(ROWS):
        grid.append([])
        for c in range(COLS):
            grid[r].append(Box(r, c))
    return grid


# Compute X offset for each panel
def panel_x(panel_index):
    return panel_index * (PANEL_WIDTH + PANEL_SPACING)


# Draw grid lines
def draw_grid_lines(panel_index):
    x_offset = panel_x(panel_index)

    for i in range(ROWS + 1):
        pygame.draw.line(
            screen, GREY,
            (x_offset, LABEL_HEIGHT + i * BOX_HEIGHT),
            (x_offset + PANEL_WIDTH, LABEL_HEIGHT + i * BOX_HEIGHT)
        )

    for j in range(COLS + 1):
        pygame.draw.line(
            screen, GREY,
            (x_offset + j * BOX_WIDTH, LABEL_HEIGHT),
            (x_offset + j * BOX_WIDTH, LABEL_HEIGHT + PANEL_HEIGHT)
        )


# Draw a full panel
def draw_panel(grid, panel_index):
    x_offset = panel_x(panel_index)

    for row in grid:
        for box in row:
            rect = pygame.Rect(
                x_offset + box.col * BOX_WIDTH,
                LABEL_HEIGHT + box.row * BOX_HEIGHT,
                BOX_WIDTH,
                BOX_HEIGHT
            )
            pygame.draw.rect(screen, box.color, rect)

    draw_grid_lines(panel_index)


# Draw top labels
def draw_labels():
    font = pygame.font.SysFont("Arial", 28, bold=True)
    labels = ["BFS", "Dijkstra", "A*"]

    for i, text in enumerate(labels):
        center_x = panel_x(i) + PANEL_WIDTH // 2
        label_surface = font.render(text, True, BLACK)
        label_rect = label_surface.get_rect(center=(center_x, LABEL_HEIGHT // 2))
        screen.blit(label_surface, label_rect)


# Convert mouse position → (row, col) for the CENTER panel only
def get_center_grid_pos(mouse_x, mouse_y):
    panel_index = 1  # middle panel
    x_offset = panel_x(panel_index)

    panel_left = x_offset
    panel_top = LABEL_HEIGHT
    panel_right = panel_left + PANEL_WIDTH
    panel_bottom = panel_top + PANEL_HEIGHT

    # only accept clicks inside middle panel grid
    if not (panel_left <= mouse_x < panel_right and
            panel_top <= mouse_y < panel_bottom):
        return None

    local_x = mouse_x - panel_left
    local_y = mouse_y - panel_top

    row = local_y // BOX_HEIGHT
    col = local_x // BOX_WIDTH
    return (row, col)


# Apply edit to ALL THREE grids, using row/col from center panel
def apply_edit(row, col, button, start, end,
               bfs_grid, dij_grid, astar_grid):

    b1 = bfs_grid[row][col]
    b2 = dij_grid[row][col]
    b3 = astar_grid[row][col]
    boxes = [b1, b2, b3]

    if button == 1:  # left click
        # Start
        if start is None and not b1.is_wall:
            for b in boxes:
                b.set_start()
            start = (row, col)

        # End
        elif end is None and not b1.is_wall and (row, col) != start:
            for b in boxes:
                b.set_end()
            end = (row, col)

        # Wall
        elif (row, col) != start and (row, col) != end:
            for b in boxes:
                b.set_wall()

    elif button == 3:  # right click
        for b in boxes:
            b.reset()

        if start == (row, col):
            start = None
        if end == (row, col):
            end = None

    return start, end


def main():
    running = True

    # Three mirrored editable grids
    bfs_grid = make_grid()
    dij_grid = make_grid()
    astar_grid = make_grid()

    start = None
    end = None

    while running:

        screen.fill(WHITE)
        draw_labels()

        # Draw all panels
        draw_panel(bfs_grid, 0)
        draw_panel(dij_grid, 1)
        draw_panel(astar_grid, 2)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Mouse editing only in middle panel, mirrored to all grids
        mouse = pygame.mouse.get_pressed()
        if mouse[0] or mouse[2]:  # left or right
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


if __name__ == "__main__":
    main()
