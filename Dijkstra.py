import pygame # Import Pygame library
import sys # Import sys for system-specific parameters and functions

pygame.init() # Initialize Pygame

WINDOW_WIDTH = 700 # Width of the window
WINDOW_HEIGHT = 700 # Height of the window

columns = 25 # Number of columns
rows = 25 # Number of rows

box_width = WINDOW_WIDTH // columns # Width of each box
box_height = WINDOW_HEIGHT // rows # Height of each box

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TURQUOISE = (64, 224, 208)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Box class representing each cell in the grid
class Box:
    def __init__(self, row, col): # Initialize box with row and column
        self.row = row
        self.col = col
        self.x = col * box_width
        self.y = row * box_height
        self.color = WHITE
        self.neighbors = []
        self.is_wall = False

    def draw(self, screen): # Draw the box on the screen
        pygame.draw.rect(screen, self.color, (self.x, self.y, box_width, box_height))
        # pygame.draw.rect(screen, BLACK, (self.x, self.y, box_width, box_height), 1) # Border

    def set_start(self): # Set box as start
        self.color = ORANGE

    def set_end(self): # Set box as end
        self.color = TURQUOISE

    def set_wall(self): # Set box as wall
        self.color = BLACK
        self.is_wall = True

    def reset(self): # Reset box to default
        self.color = WHITE
        self.is_wall = False

    def is_start(self): # Check if box is start
        return self.color == ORANGE
    
    def is_end(self): # Check if box is end
        return self.color == TURQUOISE
    
    def is_closed(self): # Check if box is closed
        return self.color == RED
    
    def is_open(self): # Check if box is open
        return self.color == GREEN
    
    def is_path(self): # Check if box is part of the path
        return self.color == PURPLE
    
    def update_neighbors(self, grid): # Update neighbors of the box
        self.neighbors = []
        # Down
        if self.row < rows - 1 and not grid[self.row + 1][self.col].is_wall:
            self.neighbors.append(grid[self.row + 1][self.col])
        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall:
            self.neighbors.append(grid[self.row - 1][self.col])
        # Right
        if self.col < columns - 1 and not grid[self.row][self.col + 1].is_wall:
            self.neighbors.append(grid[self.row][self.col + 1])
        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall:
            self.neighbors.append(grid[self.row][self.col - 1])

# Function to recolor the path from start to end
def recolor_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.color = PURPLE
        draw()

# Placeholder for Dijkstra's algorithm implementation
def dijkstra_algorithm(draw, grid, start, end):
    pass  # Placeholder for Dijkstra's algorithm implementation

# Function to create the grid
def make_grid():
    grid = []
    for r in range(rows):
        grid.append([])
        for c in range(columns):
            grid[r].append(Box(r, c))
    return grid

# Function to get the position of the mouse click
def get_clicked_pos(pos):
    x, y = pos
    row = y // box_height
    col = x // box_width
    return row, col

# Main function
def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Dijkstra's Algorithm Visualization")
    grid = make_grid() # Create the grid
    start = end = None # Start and end boxes
    running = True

    def draw():
        screen.fill(WHITE)
        for row in grid:
            for box in row:
                box.draw(screen)
        
        for i in range(rows + 1):
            y = i * box_height
            pygame.draw.line(screen, GREY, (0, i * box_height), (WINDOW_WIDTH, i * box_height))
        for j in range(columns + 1):
            x = j * box_width
            pygame.draw.line(screen, GREY, (j * box_width, 0), (j * box_width, WINDOW_HEIGHT))

        pygame.display.update()

    while running:
        draw() # Draw the grid
        for event in pygame.event.get(): # Event handling
            if event.type == pygame.QUIT:
                running = False

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

            # Keyboard events   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for box in row:
                            box.update_neighbors(grid)
                    dijkstra_algorithm(lambda: draw(), grid, start, end)

                if event.key == pygame.K_c:
                    start = end = None
                    grid = make_grid()

    pygame.quit() # Quit Pygame

# Run the main function
if __name__ == "__main__":
    main()