import pygame
from imports import import_folder, import_csv_layout, import_cut_graphics
import math

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
        self.mask = pygame.mask.from_surface(self.image)

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
        elif self.type == 'key':
            player.keys += 1

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
        self.mask = pygame.mask.from_surface(self.image)

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

class Enemy(AnimatedTile):
    def __init__(self, pos, size, path, speed=5, health=3):
        super().__init__(pos, size, path)
        self.direction = pygame.math.Vector2(0.2, 0)
        self.speed = speed
        self.health = health

    def damage(self, amount=1):
        self.health -= amount
        if self.health <= 0:
            self.kill()

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

    def update(self, shift, player):
        self.rect.x += shift
        self.animate()
        self.move()

class SaveBlock(AnimatedTile):
    def __init__(self, pos, size, path):
        super().__init__(pos, size, path)

    def effect(self, player):
        player.save()

class Portal(AnimatedTile):
    def __init__(self, pos, size, path):
        super().__init__(pos, size, path)
        self.type='portal'

    def effect(self, player):
        if player.keys > 2:
            player.win = True

class Bullet(AnimatedTile):
    def __init__(self, pos, size, path, scale=4, direction=1, speed=10, sounds=None, damage = 1):
        super().__init__(pos, size, path, scale)
        self.direction = pygame.math.Vector2(direction, 0)
        self.speed = speed
        sounds['hit'].play()
        #bullet_sound =  pygame.mixer.Sound('./assets/audio/effects/hit.wav')
        #bullet_sound.play()
        self.damage = damage

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.rect.x += self.direction.x * self.speed
class FollowingEnemy(Enemy):
    def __init__(self, pos, size, path, speed=5):
        super().__init__(pos, size, path, speed)
        self.following = False
        self.default_speed = speed
        self.barrier = False
        self.default_direction = self.direction.x
        self.default_direction = 0.2
        self._prev_pos = self.rect.x

    def move(self):
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed


    def update(self, shift, player):
        self.rect.x += shift
        self.animate()
        self.move()

        if self.distance(player):
            self.following = True
            if self.rect.x < player.rect.x:
                self.direction.x += 0.025
                
            elif self.rect.x > player.rect.x:
                self.direction.x -= 0.025
        else:
            if self.following:
                self.following = False
                self.direction.x = self.default_direction if self.direction.x > 0 else -self.default_direction
            self.barrier = False

        if self.barrier and self.following:
            self.direction.x = self.default_direction if self.rect.x < player.rect.x else -self.default_direction

        if self.rect.x != self._prev_pos:
            self.barrier = False
        self._prev_pos = self.rect.x

    def distance(self, player):
        return abs(player.rect.y - self.rect.y) < 150 and abs(player.rect.x - self.rect.x) < 200

class ShootingEnemy(Enemy):
    def __init__(self, pos, size, path, speed=5, screen=None, sounds=None):
        super().__init__(pos, size, path, speed)
        self.shoot_timer = 0
        self.shoot_time = 0.5
        self.bullets = []
        self.screen = screen
        self.sounds = sounds

    def shoot(self, player):
        if self.direction.x < 0:
            bullet = Bullet((self.rect.x - 10, self.rect.y + 25), 10, './assets/bullet/', 1, -1,5, self.sounds)
        else:
            bullet = Bullet((self.rect.x + 50, self.rect.y + 25), 10, './assets/bullet/', 1, 1,5, self.sounds)
        self.bullets.append(bullet)

    def update(self, shift, player):
        self.rect.x += shift
        self.animate()
        self.move()
        if self.player_in_range(player):
            self.shoot_timer -= 1/60
            if self.shoot_timer <= 0:
                #self.shoot_timer = 1
                self.shoot(player)
                self.shoot_timer = self.shoot_time

    def return_bullets(self):
        return self.bullets

    def clear_bullets(self):
        self.bullets = []

    def player_in_range(self, player):
        return ((player.rect.x < self.rect.x and self.direction.x < 0) or (player.rect.x > self.rect.x and self.direction.x > 0)) and abs(player.rect.y - self.rect.y) < 50 and abs(player.rect.x - self.rect.x) < 250