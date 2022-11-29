import pygame
from game_data import levels

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
    def __init__(self, surface, start_level=1, max_level=2, speed= 10, level_method=None):
        self.surface = surface
        self.selected_level = start_level
        self.max_level = max_level
        self.create_level = level_method

        self.direction = pygame.math.Vector2(0,0)
        self.shift = 0
        self.speed = speed
        self.moving = False

        self.setup_nodes()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for key, value in levels.items():
            if key <= self.max_level:
                self.nodes.add(Node((value['position'][0] - 425*(self.selected_level-1),value['position'][1]), unlocked=True, speed=self.speed, image=pygame.image.load(value['path']+ '/level_banner.png').convert_alpha()))
            else:  
                self.nodes.add(Node((value['position'][0] - 425*(self.selected_level-1),value['position'][1]), speed=self.speed))

    def input(self):
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

    def run(self):
        self.input()
        self.nodes.update()
        self.update()

        self.surface.fill((20, 20, 20))
        self.nodes.draw(self.surface)