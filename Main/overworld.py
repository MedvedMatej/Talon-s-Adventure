import pygame
from game_data import levels

class Node(pygame.sprite.Sprite):
    def __init__(self, position, unlocked=False, speed=5):
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

class Overworld:
    def __init__(self, surface, start_level=1, max_level=2):
        self.surface = surface
        self.selected_level = start_level
        self.max_level = max_level

        self.direction = pygame.math.Vector2(0,0)
        self.shift = 0
        self.speed = 3
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
                if self.selected_level < len(levels.keys()): #self.max_level:
                    self.shift = 1
                    self.direction = self.get_movement()
                    self.selected_level += 1
                    print(self.selected_level)
            
            if keys[pygame.K_LEFT]:
                self.moving = True
                if self.selected_level > 1:
                    self.shift = -1
                    self.direction = self.get_movement()
                    self.selected_level -= 1
                    print(self.selected_level)
    
    def get_movement(self):
        start = pygame.math.Vector2(self.nodes.sprites()[self.selected_level-1].rect.center)
        end = pygame.math.Vector2(self.nodes.sprites()[self.selected_level-1+self.shift].rect.center)
        print(self.selected_level, "-->", self.selected_level+self.shift)
        print(end-start)
        return -1*(end - start).normalize()

    def update_levels(self):
        for i,node in enumerate(self.nodes):
            if not node.target:
                node.target = (node.pos[0] + self.shift*500, node.pos[1])
            node.pos += self.direction * self.speed
            print(node.target, node.pos)
            if node.detection_radius.collidepoint(node.target):
                node.pos = node.target
                self.moving = False
                self.direction = pygame.math.Vector2(0,0)
                #node.target = None

    def run(self):
        self.input()
        self.nodes.update()
        self.update_levels()
        self.nodes.draw(self.surface)
        #self.level.run()