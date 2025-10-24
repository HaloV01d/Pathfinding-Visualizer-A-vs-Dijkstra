import pygame

pygame.init() # Initialize Pygame

screen = pygame.display.set_mode((800, 600)) # Width: 800, Height: 600
pygame.display.set_caption("Dijkstra's Algorithm Visualization") # Set window title
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
BLACK = (0, 0, 0) #000000
WHITE = (255, 255, 255) #FFFFFF
GRAY = (128, 128, 128) #808080
screen.fill(WHITE)
baclkground = pygame.Surface(screen.get_size()) # Create background surface
baclkground = baclkground.convert() # Convert for faster blitting
baclkground.fill(GRAY) # Fill background with white
pygame.display.flip() # Update the display

running = True
while running:
    for event in pygame.event.get(): # Event handling
        if event.type == pygame.QUIT:
            running = False

pygame.quit()