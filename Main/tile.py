import pygame
from imports import import_folder, import_csv_layout, import_cut_graphics

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, shift):
        self.rect.x += shift

class StaticTile(Tile):
    def __init__(self, pos, size, image):
        super().__init__(pos, size)
        self.image = image
    
    def effect(self, player):
        print("#TODO - Collected")
        player.available_jumps += 1

class PlatformTile(StaticTile):
    def __init__(self, pos, size, image, direction=(0,0), speed=1):
        super().__init__(pos, size, image)
        self.direction = pygame.math.Vector2(direction)
        self.speed = speed

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def reverse(self):
        self.direction.x = -self.direction.x
        self.direction.y = -self.direction.y

    def update(self, shift):
        self.rect.x += shift
        self.move()

class AnimatedTile(Tile):
    def __init__(self, pos, size, path, scale=4):
        super().__init__(pos, size)
        self.frames = import_folder(path, scale)
        self.index = 0
        self.image = self.frames[self.index]

    def animate(self):
        self.index += 0.1
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift

class Player(AnimatedTile):
    def __init__(self, pos, size, path):
        super().__init__(pos, size, path)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.08
        self.jump_speed = -1.3
        self.shoot_cooldown = False
        self.flipped = False
        self.on_ground = False

        self.max_jumps = 2
        self.available_jumps = self.max_jumps
        self.jump_cooldown = False

    def update(self, shift):
        self.animate()
        self.rect.x += shift
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.on_ground:
            self.available_jumps = self.max_jumps

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        if self.available_jumps > 0:
            self.direction.y = self.jump_speed
            self.on_ground = False

    def get_input(self, sprites):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.flipped = False
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.flipped = True
        else:
            self.direction.x = 0

        if keys[pygame.K_w]:
            if not self.jump_cooldown:
                self.jump()
                self.jump_cooldown = True
                if self.available_jumps > 0:
                    self.available_jumps -= 1
        else:
            self.jump_cooldown = False
        
        if keys[pygame.K_SPACE]:
            if not self.shoot_cooldown:
                sprites['Bullet'].add(Bullet((self.rect.centerx, self.rect.centery), 1, './assets/player/bullet',1, -1 if self.flipped else 1))
                self.shoot_cooldown = True
        else:
            self.shoot_cooldown = False


from random import randint
class Enemy(AnimatedTile):
    def __init__(self, pos, size, path):
        super().__init__(pos, size, path)
        self.direction = pygame.math.Vector2(0.2, 0)
        self.speed = 5

    def move(self):
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def apply_gravity(self):
        self.direction.y += 0.2
        if self.direction.y > 10:
            self.direction.y = 10

    def reverse(self):
        self.direction.x = -self.direction.x

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()

class Bullet(AnimatedTile):
    def __init__(self, pos, size, path, scale=4, direction=1):
        super().__init__(pos, size, path, scale)
        self.direction = pygame.math.Vector2(direction, 0)
        self.speed = 10

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.rect.x += self.direction.x * self.speed