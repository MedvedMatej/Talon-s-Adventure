import pygame, sys
from settings import *
from level import Level
from level_data import *
from overworld import Overworld

class Game:
    def __init__(self):
        #Starting values
        self.max_level = 2
        self.selected_level = 1

        #Setup states
        self.main_menu = None
        self.options = None
        self.level = None
        self.overworld = Overworld(screen, self.selected_level, self.max_level, level_method = self.create_level, get_action = self.get_action)
        self.status = 'overworld'
        
        #Event data
        self.clicks = []

    def create_level(self, level, surface):
        self.selected_level = level
        self.level = Level(level,surface, self.create_overworld)
        self.status = 'level'

    def create_overworld(self, surface, current_level, max_level):
        if self.max_level < max_level:
            self.max_level = max_level
        self.overworld = Overworld(surface, current_level, self.max_level, level_method = self.create_level, get_action = self.get_action)
        self.status = 'overworld'
    
    def get_action(self, action):
        return getattr(self, action)

    def get_selected_level(self):
        return self.overworld.selected_level

    def open_options(self):
        print("open options")

    def to_main_menu(self):
        print("to main menu")
        #self.status = 'main_menu'

    def run(self):
        if self.status == 'main_menu':
            self.main_menu.run(self.clicks)
        elif self.status == 'options':
            self.options.run(self.clicks)
        elif self.status == 'overworld':
            self.overworld.run(self.clicks)
        elif self.status == 'level':
            self.level.run()
        self.clicks = []

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                game.clicks.append(mouse_pos)
    
    game.run()

    pygame.display.update()
    clock.tick(60)