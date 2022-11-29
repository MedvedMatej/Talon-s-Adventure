import pygame, sys
from settings import *
from level import Level
from level_data import *
from overworld import Overworld

class Game:
    def __init__(self):
        self.overworld = Overworld(surface=screen)
        self.level = Level(self.overworld.selected_level,screen)

    def run(self):
        #self.level.run()
        self.overworld.run()

#Initialize pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Talon's Adventure")
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    game.run()

    pygame.display.update()
    clock.tick(60)