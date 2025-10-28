import pygame

pygame.init() # Initialize Pygame

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20
GRID_COLOR = (200, 200, 200) # Light gray
BG_COLOR = (30, 30, 30) # White

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm Visualization")

clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y))

# screen = pygame.display.set_mode((800, 600)) # Width: 800, Height: 600
# pygame.display.set_caption("Dijkstra's Algorithm Visualization") # Set window title
# clock = pygame.time.Clock()
# font = pygame.font.SysFont("Arial", 20)
# BLACK = (0, 0, 0) #000000
# WHITE = (255, 255, 255) #FFFFFF
# GRAY = (128, 128, 128) #808080
# screen.fill(WHITE)
# baclkground = pygame.Surface(screen.get_size()) # Create background surface
# baclkground = baclkground.convert() # Convert for faster blitting
# baclkground.fill(GRAY) # Fill background with white
# pygame.display.flip() # Update the display

running = True
while running:
    for event in pygame.event.get(): # Event handling
        if event.type == pygame.QUIT:
            running = False
    screen.fill(BG_COLOR) # Fill background


    draw_grid() # Draw the grid

    pygame.display.flip() # Update the display
    clock.tick(60) # Limit to 60 FPS

pygame.quit()