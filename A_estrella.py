import pygame

pygame.init() # Initialize Pygame

screen = pygame.display.set_mode((800, 600)) # Set window size
pygame.display.set_caption("A* Algorithm Visualization") # Set window title
clock = pygame.time.Clock() # Create clock object
font = pygame.font.SysFont("Arial", 20) # Set font
BLACK = (0, 0, 0) #000000
WHITE = (255, 255, 255) #FFFFFF
GRAY = (128, 128, 128) #808080
screen.fill(WHITE) # Fill screen with white
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(GRAY)
pygame.display.flip() # Update the display

running = True # Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
pygame.quit()