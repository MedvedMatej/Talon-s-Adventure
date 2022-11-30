import pygame
from menu_items import Text, Button, Node
from game_data import levels, menus

class Menu:
    def __init__(self, surface, get_action, menu):
        self.surface = surface
        self.get_action = get_action
        self.menu = menu

        #Init
        self.buttons = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()

        #Setup
        self.show_hidden = False
        self.setup()

    def setup(self):
        for pos,text,size in menus[self.menu]["texts"]:
            self.texts.add(Text(pos, text, size))

        for pos,text,hidden,action in menus[self.menu]["buttons"]:
            self.buttons.add(Button(pos, None, text, hidden, action, self.get_action))
    
    def input(self, clicks=None):
        for click in clicks:
            for button in self.buttons:
                if button.rect.collidepoint(click):
                    button.click()

    def run(self, clicks=None):
        self.input(clicks)
        self.buttons.update(self.show_hidden)
        #self.nodes.update()
        #self.update()

        self.surface.fill((20, 20, 20))
        self.buttons.draw(self.surface)
        self.texts.draw(self.surface)

class Overworld:
    def __init__(self, surface, start_level=1, max_level=2, speed= 10, level_method=None, get_action=None):
        self.surface = surface
        self.selected_level = start_level
        self.max_level = max_level
        self.create_level = level_method

        self.direction = pygame.math.Vector2(0,0)
        self.shift = 0
        self.speed = speed
        self.moving = False

        self.setup_nodes()
        #Texts
        self.texts = pygame.sprite.Group()
        self.texts.add(Text((625, 100), 'LEVEL SELECTION', 70, (255, 255, 255)))

        #Buttons
        self.buttons = pygame.sprite.Group()
        self.buttons.add(Button((625,625), None, "PLAY", False, "create_level", get_action, self.surface))
        self.buttons.add(Button((625,675), None, "OPTIONS", False, "to_options", get_action))
        self.buttons.add(Button((625,725), None, "BACK TO MAIN MENU", False, "to_main_menu", get_action))
        
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for key, value in levels.items():
            if key <= self.max_level:
                self.nodes.add(Node((value['position'][0] - 425*(self.selected_level-1),value['position'][1]), unlocked=True, speed=self.speed, image=pygame.image.load(value['path']+ '/level_banner.png').convert_alpha()))
            else:  
                self.nodes.add(Node((value['position'][0] - 425*(self.selected_level-1),value['position'][1]), speed=self.speed))

    def input(self, clicks=None):
        for click in clicks:
            for button in self.buttons:
                if button.rect.collidepoint(click):
                    button.click()

        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_RIGHT]:
                self.moving = True
                if self.selected_level < len(levels.keys()):
                    self.shift = 1
                    self.direction = self.set_movement()
                    self.selected_level += 1
            
            elif keys[pygame.K_LEFT]:
                self.moving = True
                if self.selected_level > 1:
                    self.shift = -1
                    self.direction = self.set_movement()
                    self.selected_level -= 1

            if keys[pygame.K_RETURN] and self.selected_level <= self.max_level:
                self.create_level(self.selected_level, self.surface)
    
    def set_movement(self):
        for node in self.nodes:
            node.target = (node.pos[0] + -1*self.shift*425, node.pos[1])
    
    def update(self):
        running = False
        for node in self.nodes:
            if node.target:
                running = True
        self.moving = running

    def run(self, clicks=None):
        self.input(clicks)
        self.nodes.update()
        self.update()

        self.surface.fill((20, 20, 20))
        self.nodes.draw(self.surface)
        self.buttons.draw(self.surface)
        self.texts.draw(self.surface)