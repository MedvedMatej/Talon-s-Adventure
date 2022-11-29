import pygame, sys
from settings import *
from tile import Tile
from level import Level
from level_data import *
from overworld import Overworld

class Game:
    def __init__(self):
        self.overworld = Overworld(surface=screen)

    def run(self):
        self.overworld.run()

#Initialize pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Talon's Adventure")
clock = pygame.time.Clock()

level = Level(level_0, screen)
game = Game()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((162, 235, 250))
    #level.run()
    game.run()
    
    pygame.display.update()
    clock.tick(60)