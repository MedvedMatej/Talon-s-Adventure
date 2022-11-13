import pygame
from os import walk

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, speed, size):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pygame.Vector2(0, 0)
        self.speed = speed
        self.traction = 0.9
        self.gravity = 0.08
        self.jump_speed = -1.3

    def import_character_assets(self):
        character_path = './assets/character/'
        self.animations = {'idle': [], 'walk': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation + '/'
            self.animations[animation] = []

            for _, _, files in walk(full_path):
                for file in files:
                    self.animations[animation].append(pygame.image.load(full_path + "/" + file).convert_alpha())

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations['idle']):
            self.frame_index = 0

        self.image = self.animations['idle'][int(self.frame_index)]

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_w]:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.animate()
        #self.apply_gravity()
        #self.rect.x += self.direction.x * self.speed
        #self.rect.y += self.direction.y * self.speed