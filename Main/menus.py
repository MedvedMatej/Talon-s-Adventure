import pygame
from menu_items import Text, Button, Node
from game_data import levels, menus
from background import Background

class Menu:
    def __init__(self, surface, get_action, menu, transparent=False):
        self.surface = surface
        self.get_action = get_action
        self.menu = menu
        self.transparent = transparent

        #Init
        self.buttons = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()

        #Setup
        self.show_hidden = False
        self.setup()

    def setup(self):
        for text in menus[self.menu]["texts"]:
            if len(text) == 2:
                pos, text = text
                self.texts.add(Text(pos, text))
            elif len(text) == 3:
                pos, text, size = text
                self.texts.add(Text(pos, text, size))
            elif len(text) == 4:
                pos, text, size, color = text
                self.texts.add(Text(pos, text, size, color))
            elif len(text) == 5:
                pos, text, size, color, position_type = text
                self.texts.add(Text(pos, text, size, color, position_type))
            elif len(text) == 6:
                pos, text, size, color, position_type, id = text
                self.texts.add(Text(pos, text, size, color, position_type, id))
            #self.texts.add(Text(pos, text, size, color))

        for pos,text,hidden,action in menus[self.menu]["buttons"]:
            self.buttons.add(Button(pos, None, text, hidden, action, self.get_action))

        if menus[self.menu]["background"]:
            self.background = Background([menus[self.menu]["background"]],self.surface)
        #self.background = Background([menus[self.menu]["background"]],self.surface)
        #menus[self.menu]["background"]
    
    def input(self, clicks=None):
        if not clicks:
            return

        for click in clicks:
            for button in self.buttons:
                if button.rect.collidepoint(click):
                    button.click()

    def run(self, clicks=None):
        self.input(clicks)
        self.buttons.update(self.show_hidden)
        #self.nodes.update()
        #self.update()

        if not self.transparent:
            self.surface.fill((20, 20, 20))
            if self.background:
                self.background.draw()
        self.buttons.draw(self.surface)
        self.texts.draw(self.surface)

class InputMenu(Menu):
    def __init__(self, surface, get_action, menu, transparent=False):
        super().__init__(surface, get_action, menu, transparent)
        self.input_text = ""
        self.input_field = Text((355, 300), self.input_text, 50, (255, 255, 255), 'topleft', "input_field")
        self.texts.add(self.input_field)

        self.input_rect = pygame.Rect(350, 300, 550, 62)
        self.rect_color = (255, 255, 255)

    def run(self, clicks = None, text = None):
        self.input_field.update(text)
        self.input(clicks)
        self.buttons.update(self.show_hidden)
        #self.nodes.update()
        #self.update()

        if not self.transparent:
            self.surface.fill((20, 20, 20))
        pygame.draw.rect(self.surface, self.rect_color, self.input_rect, 2)
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

        #Start time
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer = 500

    def input_timer(self):
        print(self.start_time, pygame.time.get_ticks())
        if not self.allow_input:
            if pygame.time.get_ticks() - self.start_time > self.timer:
                self.allow_input = True
        
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

            ##TODO: Check click on level nodes

        keys = pygame.key.get_pressed()
        if not self.moving and self.allow_input:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.moving = True
                if self.selected_level < len(levels.keys()):
                    self.shift = 1
                    self.direction = self.set_movement()
                    self.selected_level += 1
            
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
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

        self.input_timer()

    def run(self, clicks=None):
        self.input(clicks)
        self.nodes.update()
        self.update()

        self.surface.fill((20, 20, 20))
        self.nodes.draw(self.surface)
        self.buttons.draw(self.surface)
        self.texts.draw(self.surface)