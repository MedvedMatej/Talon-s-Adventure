import pygame, sys
from settings import *
from level import Level
from level_data import *
from overworld import Overworld

class Game:
    def __init__(self):
        self.overworld = Overworld(surface=screen, level_method = self.create_level)
        self.level = None
        self.max_level = 2
        self.status = 'overworld'

    def create_level(self, level, surface):
        self.level = Level(level,surface, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, surface, current_level, max_level):
        if self.max_level < max_level:
            self.max_level = max_level
        self.overworld = Overworld(surface, current_level, self.max_level, level_method = self.create_level)
        self.status = 'overworld'

    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        elif self.status == 'level':
            self.level.run()

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