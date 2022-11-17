import pygame, sys
from settings import *
from tile import Tile
from level import Level
from level_data import *

#Initialize pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Talon's Adventure")
clock = pygame.time.Clock()

level = Level(level_0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        """ elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for sprite in level.sprites['Player']:
                    sprite.rect.x = pygame.mouse.get_pos()[0]
                    sprite.rect.y = pygame.mouse.get_pos()[1] """
    
    screen.fill((162, 235, 250))
    level.run()

    pygame.display.update()
    clock.tick(60)