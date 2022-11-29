import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):
    def __init__(self, position, unlocked=False, speed=15):
        super().__init__()
        self.image = pygame.Surface((350, 250))
        self.unlocked = unlocked
        self.pos = position
        self.speed = speed
        self.target = None

        if unlocked:
            self.image.fill((160, 0, 0))
        else:
            self.image.fill((45, 45, 45))
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
    def __init__(self, surface, start_level=1, max_level=2):
        self.surface = surface
        self.selected_level = start_level
        self.max_level = max_level

        self.direction = pygame.math.Vector2(0,0)
        self.shift = 0
        self.speed = 10
        self.moving = False

        self.setup_nodes()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for key, value in levels.items():
            if key <= self.max_level:
                self.nodes.add(Node(value['position'], unlocked=True, speed=self.speed))
            else:  
                self.nodes.add(Node(value['position'], speed=self.speed))

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.moving:
            if keys[pygame.K_RIGHT]:
                self.moving = True
                if self.selected_level < len(levels.keys()):
                    self.shift = 1
                    self.direction = self.set_movement()
                    self.selected_level += 1
            
            if keys[pygame.K_LEFT]:
                self.moving = True
                if self.selected_level > 1:
                    self.shift = -1
                    self.direction = self.set_movement()
                    self.selected_level -= 1
    
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

        self.nodes.draw(self.surface)