import pygame
from tile import AnimatedTile, Bullet
import copy

class Player(AnimatedTile):
    def __init__(self, pos, size, path):
        super().__init__(pos, size, path)
        #Animations

        #General movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.08
        self.jump_speed = -1.3
        self.flipped = False
        self.shoot_cooldown = False
        self.reset_cooldown = False

        #Effects
        self.on_effected_tile = False
        self.next_to_effected_tile = False
        self.effects = {}

        #Jumping
        self.on_ground = False
        self.max_jumps = 2
        self.available_jumps = self.max_jumps
        self.jump_cooldown = False
        
        #Outside movement
        self.platform = (0,0,0)

        #Save
        self.saved_player = {}
        self.save()

    def update(self, shift):
        self.animate()
        self.rect.x += shift
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        if self.on_ground:
            self.available_jumps = self.max_jumps
        
        if 'damage' in self.effects:
            self.load_save()

    def save(self):
        for key,value in self.__dict__.items():
            if key not in ['_Sprite__g', 'image', 'animations', 'reset_cooldown', 'saved_player']:
                self.saved_player[key] = copy.deepcopy(value)
        self.saved_player['reset_cooldown'] = True
            

    def load_save(self):
        for key,value in self.saved_player.items():
            self.__dict__[key] = copy.deepcopy(value)

    def clear_effects(self):
        self.effects = {}

    def give_effects(self, effects):
        self.effects = effects

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    def jump(self):
        if self.available_jumps > 0:
            self.direction.y = self.jump_speed if not 'jump_multiplier' in self.effects else self.jump_speed*self.effects['jump_multiplier']
            self.on_ground = False
            self.platform = (0,0,0)

    def get_input(self, sprites):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.flipped = False
            if self.on_ground:
                self.set_animation('walk')
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.flipped = True
            if self.on_ground:
                self.set_animation('walk')
        else:
            self.direction.x = 0
            if self.selected_animation != 'jump' or self.on_ground:
                self.set_animation('idle')

        if keys[pygame.K_w]:
            if not self.jump_cooldown:
                self.set_animation('jump')
                self.jump()
                self.jump_cooldown = True
                if self.available_jumps > 0:
                    self.available_jumps -= 1
        else:
            self.jump_cooldown = False
        
        if keys[pygame.K_SPACE]:
            if not self.shoot_cooldown:
                sprites['Bullet'].add(Bullet((self.rect.centerx, self.rect.centery), 1, './assets/bullet/',1, -1 if self.flipped else 1))
                self.shoot_cooldown = True
        else:
            self.shoot_cooldown = False

        if keys[pygame.K_r]:
            if not self.reset_cooldown:
                self.load_save()
        else:
            self.reset_cooldown = False

    def animate(self):
        if self.selected_animation == 'jump':
            if self.direction.y > 0:
                self.index = 0
            else:
                self.index = 1
        else:
            self.index += 0.1
            if self.index >= len(self.animations[self.selected_animation]):
                self.index = 0
        self.image = self.animations[self.selected_animation][int(self.index)]
