import pygame

pygame.init()

# Definitions
width = 800
height = 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Suika Game')

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    pygame.display.flip()