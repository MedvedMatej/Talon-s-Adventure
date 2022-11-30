import pygame
from game_data import levels

class Text(pygame.sprite.Sprite):
    def __init__(self, position, text, size=30, color=(255, 255, 255)):
        super().__init__()
        self.font = pygame.font.SysFont('Arial', size)
        self.text = self.font.render(text, True, color)
        self.size = self.text.get_size()
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=position)
        self.image.blit(self.text, (0, 0))

class Button(pygame.sprite.Sprite):
    def __init__(self, position, image, text, action=None, get_action=None, *args):
        super().__init__()

        self.action = action
        self.args = args
        self.get_action = get_action
        self.call_action = get_action(action)

        self.font = pygame.font.SysFont('Arial', 30)
        self.text = self.font.render(text, True, (255, 255, 255))
        self.size = self.text.get_size()
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(center=position)
        self.image.fill((0, 0, 0))
        self.image.blit(self.text, (0, 0))

    def click(self):
        if self.action:
            if self.action == 'create_level':
                selected_level = self.get_action('get_selected_level')()
                self.call_action(selected_level, *self.args)
            else:
                self.call_action(*self.args)

class Node(pygame.sprite.Sprite):
    def __init__(self, position, unlocked=False, speed=5, image=None):
        super().__init__()
        self.image = image if image else pygame.Surface((350, 250))
        self.unlocked = unlocked
        self.pos = position
        self.speed = speed
        self.target = None

        if not unlocked:
            self.image = pygame.image.load('assets/levels/level_banner_locked.png').convert_alpha()
        self.rect = self.image.get_rect(center=position)


    def update(self):
        self.rect.center = self.pos
        if self.target:
            if (self.target[0] - self.pos[0]) != 0:
                dir = (self.target[0] - self.pos[0]) / abs((self.target[0] - self.pos[0]))
                self.pos = (self.pos[0] + self.speed * dir, self.pos[1])
                if (dir < 0 and self.pos[0] <= self.target[0]) or (dir > 0 and self.pos[0] >= self.target[0]):
                    self.pos = self.target
                    self.target = None
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
        self.buttons.add(Button((625,625), None, "PLAY", "create_level", get_action, self.surface))
        self.buttons.add(Button((625,675), None, "OPTIONS", "open_options", get_action))
        self.buttons.add(Button((625,725), None, "BACK TO MAIN MENU", "to_main_menu", get_action))
        
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