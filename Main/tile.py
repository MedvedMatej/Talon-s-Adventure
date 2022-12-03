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
        self.image_hidden = image

class TerrainTile(StaticTile):
    def __init__(self, pos,size, image, type):
        super().__init__(pos,size, image)
        self.type = type
        self.effects = {}

        if type == 'Water':
            self.effects["speed_multiplier"] = 0.5
            self.effects["jump_multiplier"] = 0.5
        elif type == 'Spike':
            self.effects["damage"] = 1

class Spike(TerrainTile):
    def __init__(self, pos, size, image, type):
        super().__init__(pos, size, image, type)
        self.rect = self.image.get_rect(topleft= (pos[0], pos[1] + size/2))

class CollectableTile(StaticTile):
    def __init__(self, pos, size, image, respawnable=True, type='jump_boost', despawn=True):
        super().__init__(pos, size, image)
        self.type = type
        self.respawnable = respawnable
        self.active = True
        self.respawn_time = 1.5
        self.respawn_timer = 0
        self.despawn = despawn
        #Shift to middle of tile
        self.rect = self.image.get_rect(center = (pos[0] + size, pos[1] + size))

    def effect(self, player):
        if self.type == 'jump_boost':
            player.available_jumps += 1
        elif self.type == 'portal':
            print(player.keys)
            if player.keys > 2:
                print("Portal")
                player.win = True
        elif self.type == 'key':
            player.keys += 1
            print("Keys: ", player.keys)

    def hide(self):
        if self.despawn:
            self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

    def collect(self):
        self.respawn_timer = self.respawn_time
        self.active = False
        self.hide()

    def update(self, shift):
        self.rect.x += shift
        if not self.active:
            self.respawn_timer -= 1/60
            if self.respawn_timer <= 0:
                self.active = True
                self.image = self.image_hidden


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
        self.animations = import_folder(path, scale)
        self.selected_animation = 'idle' if 'idle' in self.animations.keys() else list(self.animations.keys())[0]
        self.index = 0
        self.image = self.animations[self.selected_animation][self.index]

    def set_animation(self, animation):
        if animation != self.selected_animation:
            self.index = 0
            self.selected_animation = animation

    def animate(self):
        self.index += 0.1
        if self.index >= len(self.animations[self.selected_animation]):
            self.index = 0
        self.image = self.animations[self.selected_animation][int(self.index)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift

from random import randint
class Enemy(AnimatedTile):
    def __init__(self, pos, size, path, speed=5):
        super().__init__(pos, size, path)
        self.direction = pygame.math.Vector2(0.2, 0)
        self.speed = speed

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

class SaveBlock(AnimatedTile):
    def __init__(self, pos, size, path):
        super().__init__(pos, size, path)

    def effect(self, player):
        player.save()

class Bullet(AnimatedTile):
    def __init__(self, pos, size, path, scale=4, direction=1):
        super().__init__(pos, size, path, scale)
        self.direction = pygame.math.Vector2(direction, 0)
        self.speed = 10

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.rect.x += self.direction.x * self.speed