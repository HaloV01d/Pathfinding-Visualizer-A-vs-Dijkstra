# Number of rows and columns
ROWS = 25
COLS = 25

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
        self.color = WHITE
        self.neighbors = []
        self.is_wall = False

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
        if self.row < ROWS - 1 and not grid[self.row + 1][self.col].is_wall:
            self.neighbors.append(grid[self.row + 1][self.col])
        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall:
            self.neighbors.append(grid[self.row - 1][self.col])
        # Right
        if self.col < COLS - 1 and not grid[self.row][self.col + 1].is_wall:
            self.neighbors.append(grid[self.row][self.col + 1])
        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall:
            self.neighbors.append(grid[self.row][self.col - 1])

# Function to recolor the final path purple and return its length in steps
def recolor_path(came_from, current, draw):
    length = 0
    while current in came_from:
        current = came_from[current]
        current.color = PURPLE
        draw()
        length += 1
    return length

# Function to create the grid
def make_grid():
    return [[Box(r, c) for c in range(COLS)] for r in range(ROWS)]

def expanded_and_path(grid):
    expanded = 0     # number of closed (RED) nodes
    path_len = 0     # number of purple tiles

    for row in grid:
        for box in row:
            if box.is_closed():
                expanded += 1
            if box.is_path():
                path_len += 1

    return expanded, path_len
