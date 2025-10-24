import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("A* Algorithm Visualization")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
pygame.quit()