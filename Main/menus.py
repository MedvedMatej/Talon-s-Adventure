import pygame
from menu_items import Text, Button, Node
from game_data import levels, menus
from background import Background
import json

class Menu:
    def __init__(self, surface, get_action, menu, transparent=False):
        self.surface = surface
        self.get_action = get_action
        self.menu = menu
        self.transparent = transparent

        #Init
        self.buttons = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()
        self.background = None

        #Setup
        self.show_hidden = False
        self.setup()

    def setup(self):
        for text in menus[self.menu]["texts"]:
            self.texts.add(text)

        for button in menus[self.menu]["buttons"]:
            button.set_action(self.get_action)
            self.buttons.add(button)

        if menus[self.menu]["background"]:
            self.background = Background([menus[self.menu]["background"]],self.surface)
    
    def input(self, clicks=None):
        if not clicks:
            return
        resize_scale = self.get_action("resize_scale")
        for click in clicks:
            for button in self.buttons:
                if button.actual_rect.collidepoint([click[0]/resize_scale, click[1]/resize_scale]):
                    button.click()

    def run(self, clicks=None):
        self.input(clicks)
        self.buttons.update(self.show_hidden, pygame.mouse.get_pos())
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
        self.input_field = Text((368, 300), self.input_text, 50, (0, 0, 0), 'topleft', "input_field")
        self.texts.add(self.input_field)

        #self.input_rect = pygame.Rect(350, 285, 550, 62)
        #self.rect_color = (255, 255, 255)
        self.name_input_rect = pygame.image.load("assets/menu_assets/name_input.png")

    def run(self, clicks = None, text = None):
        self.input_field.update(text)
        self.input(clicks)
        self.buttons.update(self.show_hidden, pygame.mouse.get_pos())
        #self.nodes.update()
        #self.update()

        if not self.transparent:
            self.surface.fill((20, 20, 20))
        #pygame.draw.rect(self.surface, self.rect_color, self.input_rect, 2)
        self.surface.blit(self.name_input_rect, (350, 285))
        self.buttons.draw(self.surface)
        self.texts.draw(self.surface)

class LeaderboardMenu(Menu):
    def __init__(self, surface, get_action, menu, transparent=False, level=1):
        super().__init__(surface, get_action, menu, transparent)
        self.transparent = transparent
        
        self.leaderboard = None
        #Read JSON file
        try:
            with open(f"./scoreboards/scoreboard_{level}.json", "r") as f:
                self.leaderboard = json.load(f)
                #Sort by time and deaths
                self.leaderboard.sort(key=lambda x: (x["time"], x["deaths"]))
                self.leaderboard = self.leaderboard[:10]
        except:
            with open(f"./scoreboards/scoreboard_{level}.json", "w") as f:
                json.dump([], f)
            self.leaderboard = []

        self.scoreboard = pygame.image.load("./assets/menu_assets/scoreboard.png")

        self.font_color = (0, 0, 0)
        self.texts.add(Text((625, 150), f"Level {level}", 40, (255, 255, 255)))
        self.texts.add(Text((300, 200), "#", 30, self.font_color, 'topleft'))
        self.texts.add(Text((355, 200), "Name", 30, self.font_color, 'topleft'))
        self.texts.add(Text((700, 200), "Time", 30, self.font_color, 'topleft'))
        self.texts.add(Text((875, 200), "Deaths", 30, self.font_color, 'topleft'))
        for i,player in enumerate(self.leaderboard):
            self.texts.add(Text((300, 235+ i*35), f"{i+1}", 30, self.font_color, 'topleft'))
            self.texts.add(Text((355, 235+ i*35), f"{player['name']}", 30, self.font_color, 'topleft'))
            self.texts.add(Text((700, 235+ i*35), f"{player['time']}", 30, self.font_color, 'topleft'))
            self.texts.add(Text((875, 235+ i*35), f"{player['deaths']}", 30, self.font_color, 'topleft'))

        #self.leaderboard_rect = pygame.Rect(275, 185, 700, 400)
        #self.rect_color = (255, 255, 255)
        self.level = level

    def run(self, clicks = None):
        self.input(clicks)
        self.buttons.update(self.show_hidden, pygame.mouse.get_pos())


        self.surface.fill((20, 20, 20))
        if self.background:
            self.background.draw()
        #pygame.draw.rect(self.surface, self.rect_color, self.leaderboard_rect, 2)
        self.surface.blit(self.scoreboard, (265, 169))
        self.buttons.draw(self.surface)
        self.texts.draw(self.surface)

class SlidesMenu:
    def __init__(self, surface, get_action, path, slides):
        self.surface = surface
        self.get_action = get_action
        self.path = path
        self.slides = slides
        self.current_slide = 1
        self.slide = pygame.image.load(self.path + str(self.current_slide)+".png")

    def input(self, clicks):
        if clicks:
            self.current_slide += 1
            if self.current_slide >= self.slides:
                self.get_action("to_overworld")()
            self.slide = pygame.image.load(self.path + str(self.current_slide)+".png")

    def run(self, clicks = None):
        self.input(clicks)
        self.surface.blit(self.slide, (0, 0))

class Overworld:
    def __init__(self, surface, start_level=1, max_level=2, speed= 16, level_method=None, get_action=None):
        self.surface = surface
        self.selected_level = start_level
        self.max_level = max_level
        self.create_level = level_method
        self.get_action = get_action

        self.direction = pygame.math.Vector2(0,0)
        self.shift = 0
        self.speed = speed
        self.moving = False

        self.setup_nodes()
        #Texts
        self.texts = pygame.sprite.Group()
        self.texts.add(Text((625, 100), 'Level Selection', 70, (255, 255, 255)))

        #Buttons
        self.buttons = pygame.sprite.Group()
        self.buttons.add(Button(position=(625,575), text="Play", action="create_level", get_action = get_action, image=("assets/menu_assets/button_long.png"), offset=(-25, -25), screen=[self.surface]))
        self.buttons.add(Button(position=(625,650), text="Options", action="to_options", get_action = get_action, image=("assets/menu_assets/button_long.png"), offset=(-25, -25)))
        self.buttons.add(Button(position=(625,725), text="Main Menu", action="to_main_menu", get_action = get_action, image=("assets/menu_assets/button_long.png"), offset=(-25, -25)))

        #Start time
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer = 500

    def input_timer(self):
        if not self.allow_input:
            if pygame.time.get_ticks() - self.start_time > self.timer:
                self.allow_input = True
        
    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for key, value in levels.items():
            if key <= self.max_level:
                self.nodes.add(Node((value['position'][0] - 425*(self.selected_level-1),value['position'][1]), unlocked=True, speed=self.speed, image=pygame.image.load('./assets/menu_assets/level_board.png').convert_alpha(), id=key, get_action=self.get_action))
            else:  
                self.nodes.add(Node((value['position'][0] - 425*(self.selected_level-1),value['position'][1]), speed=self.speed, id=key, get_action=self.get_action))

    def input(self, clicks=None):
        resize_scale = self.get_action("resize_scale")
        for click in clicks:
            for button in self.buttons:
                if button.actual_rect.collidepoint([click[0]/resize_scale, click[1]/resize_scale]):
                    button.click()

            for node in self.nodes:
                for button in node.buttons:
                    if button.actual_rect.collidepoint([click[0]/resize_scale, click[1]/resize_scale]):
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
        self.buttons.update(mouse_pos = pygame.mouse.get_pos())
        self.update()

        self.surface.fill((20, 20, 20))
        self.nodes.draw(self.surface)
        for node in self.nodes:
            node.buttons.draw(self.surface)
        self.buttons.draw(self.surface)
        self.texts.draw(self.surface)