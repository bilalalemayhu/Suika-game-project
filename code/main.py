import pygame

pygame.init()

width = 800
height = 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pygame.display.set_caption('Suika')

k = "hh"
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    pygame.display.flip()