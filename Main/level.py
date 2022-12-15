import pygame
from tile import *
from settings import tile_size, player_speed, screen_width, screen_height, global_scale, default_graphics_scale
from collections import defaultdict
from imports import import_csv_layout, import_cut_graphics, import_folder
from background import Background
from player import Player
from game_data import levels
from menus import Menu

class Level:
    def __init__(self, selected_level, surface, overworld_method=None, get_action=None):
        self.create_overworld = overworld_method
        self.get_action = get_action
        level_data = levels[selected_level]['data']
        self.sprites = defaultdict(pygame.sprite.Group)
        self.sprites_graphics = defaultdict(list)
        self.sprites_scale = defaultdict(lambda:default_graphics_scale)
        self.surface = surface
        self.background = Background(level_data['background'], self.surface)
        self.selected_level = selected_level
        self.win = False

        #Set world layout and scale
        self.terrain_layout = import_csv_layout(level_data['Terrain'])
        self.decoration_layout = import_csv_layout(level_data['Decorations'])
        self.collectables_layout = import_csv_layout(level_data['Collectables'])
        self.constraints_layout = import_csv_layout(level_data['Constraints'])
        self.show_constraints = False
        #Animated
        self.player_layout = import_csv_layout(level_data['Player'])
        self.enemy_layout = import_csv_layout(level_data['Enemy'])
        
        #Import graphics
        self.sprites_graphics['Terrain'] = import_cut_graphics('./assets/background/tileset.png')
        self.sprites_graphics['Decorations'] = import_cut_graphics('./assets/background/tileset.png')
        self.sprites_graphics['Constraints'] = import_cut_graphics('./assets/background/tileset.png')
        self.sprites_graphics['Collectables'] = import_cut_graphics('./assets/background/tileset.png',scale=2)
        self.sprites_scale['Collectables'] = 2
        #Animated
        
        #Create tile groups
        self.create_tile_group(self.terrain_layout, 'Terrain')
        self.create_tile_group(self.decoration_layout, 'Decorations')
        self.create_tile_group(self.collectables_layout, 'Collectables')
        self.create_tile_group(self.constraints_layout, 'Constraints')
        #Animated
        self.create_tile_group(self.player_layout, 'Player', animated=True)
        self.player = [x for x in self.sprites['Player']][0]
        self.create_tile_group(self.enemy_layout, 'Enemy', animated=True)

        self.world_shift = 0

        self.sprites['Bullet']

        #Level timer
        self.start_time = pygame.time.get_ticks()/1000

        #UI overlay
        self.ui_overlay = Menu(self.surface, self.get_action, 'ui_overlay', True)


    def create_tile_group(self, layout, tile_type, animated=False):
        for row, tiles in enumerate(layout):
            for column, tile in enumerate(tiles):
                if tile != '-1':
                    if animated:
                        if tile_type == 'Player':
                            sprite = Player((column*tile_size*4*global_scale, row*tile_size*4*global_scale), tile_size*self.sprites_scale[tile_type]*global_scale, f'./assets/{tile_type.lower()}/')
                            self.sprites[tile_type].add(sprite)
                        elif tile_type == 'Enemy':
                            if int(tile) == 0:
                                sprite = Enemy((column*tile_size*4*global_scale, row*tile_size*4*global_scale), tile_size*self.sprites_scale[tile_type]*global_scale, f'./assets/{tile_type.lower()}/')
                                self.sprites[tile_type].add(sprite)
                            elif int(tile) == 1:
                                sprite = FollowingEnemy((column*tile_size*4*global_scale, row*tile_size*4*global_scale), tile_size*self.sprites_scale[tile_type]*global_scale, f'./assets/{tile_type.lower()}/')
                                self.sprites[tile_type].add(sprite)
                            elif int(tile) == 2:
                                sprite = ShootingEnemy((column*tile_size*4*global_scale, row*tile_size*4*global_scale), tile_size*self.sprites_scale[tile_type]*global_scale, f'./assets/{tile_type.lower()}/')
                                self.sprites[tile_type].add(sprite)
                    else:
                        tile_surface = self.sprites_graphics[tile_type][int(tile)]
                        if int(tile) == -2:
                            sprite = SaveBlock((column*tile_size*4*global_scale, row*tile_size*4*global_scale), tile_size*global_scale*4, './assets/saveblock/')
                            self.sprites['Terrain'].add(sprite)
                        elif int(tile) in [232,233,234]:
                            sprite = TerrainTile((column*tile_size*4*global_scale, row*tile_size*4*global_scale),tile_size*self.sprites_scale[tile_type]*global_scale, tile_surface, 'Water')
                            self.sprites['Terrain'].add(sprite)
                        elif int(tile) in [4]:
                            sprite = Spike((column*tile_size*4*global_scale, row*tile_size*4*global_scale),tile_size*self.sprites_scale[tile_type]*global_scale, tile_surface, 'Spike')
                            self.sprites['Terrain'].add(sprite)
                        elif int(tile) in [184,185,186]:
                            sprite = PlatformTile((column*tile_size*4*global_scale, row*tile_size*4*global_scale),tile_size*self.sprites_scale[tile_type]*global_scale, tile_surface, (1,0))
                            self.sprites['Platforms'].add(sprite)
                        elif int(tile) in [187]:
                            sprite = PlatformTile((column*tile_size*4*global_scale, row*tile_size*4*global_scale),tile_size*self.sprites_scale[tile_type]*global_scale, tile_surface, (0,1))
                            self.sprites['Platforms'].add(sprite)
                        elif tile_type == 'Collectables':
                            if int(tile) in [5]:
                                sprite = CollectableTile((column*tile_size*4*global_scale, row*tile_size*4*global_scale),tile_size*self.sprites_scale[tile_type]*global_scale, tile_surface, type='portal', despawn=False)
                                self.sprites['Collectables'].add(sprite)
                            elif int(tile) in [404]:
                                sprite = CollectableTile((column*tile_size*4*global_scale, row*tile_size*4*global_scale),tile_size*self.sprites_scale[tile_type]*global_scale, tile_surface, type='key', respawnable=False)
                                self.sprites['Collectables'].add(sprite)
                            else:
                                sprite = CollectableTile((column*tile_size*4*global_scale, row*tile_size*4*global_scale),tile_size*self.sprites_scale[tile_type]*global_scale, tile_surface)
                                self.sprites['Collectables'].add(sprite)
                        else:
                            sprite = StaticTile((column*tile_size*4*global_scale, row*tile_size*4*global_scale),tile_size*self.sprites_scale[tile_type]*global_scale, tile_surface)
                            self.sprites[tile_type].add(sprite)

    def scroll_x(self):
        player = self.player
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width/4 and direction_x < 0:
            self.world_shift = player_speed
            player.speed = 0
        elif player_x > screen_width*3/4 and direction_x > 0:
            self.world_shift = -player_speed
            player.speed = 0
        else:  
            self.world_shift = 0
            player.speed = player_speed

    def horizontal_collisions(self, player):
        multiplier = (1 if not 'speed_multiplier' in player.effects else player.effects['speed_multiplier'])
        player.rect.x += player.direction.x * player.speed * multiplier
        player.rect.x += player.platform[0] * player.platform[2]

        for sprite in self.sprites['Terrain']:
            if sprite.rect.colliderect(player.rect):
                ##TODO: Check for bugs
                if hasattr(sprite, 'effects'):
                    player.give_effects(sprite.effects)
                    player.on_effected_tile = True
                else:
                    player.on_effected_tile = False
                    player.clear_effects()
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                elif player.direction.x < 0:
                    player.rect.left = sprite.rect.right

        for sprite in self.sprites['Platforms']:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    if sprite.direction.x < 0:
                        player.rect.x += sprite.direction.x * sprite.speed - 1
                elif player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    if sprite.direction.x > 0:
                        player.rect.x += sprite.direction.x * sprite.speed + 1
        
        for sprite in self.sprites['Collectables']:
            if sprite.rect.colliderect(player.rect) and sprite.active:
                sprite.effect(player)
                sprite.collect()
                if not sprite.respawnable:
                    self.sprites['Collectables'].remove(sprite)

        for sprite in self.sprites['Enemy']:
            if sprite.rect.colliderect(player.rect):
                player.effects['damage'] = 1
                #player.load_save()
    
    def vertical_collisions(self, player):
        player.apply_gravity()
        player.rect.y += player.direction.y * player.speed
        player.rect.y += player.platform[1] * player.platform[2]

        for sprite in self.sprites['Terrain']:
            if sprite.rect.colliderect(player.rect):
                if hasattr(sprite, 'effects'):
                    player.give_effects(sprite.effects)
                    player.on_effected_tile = True
                else:
                    player.on_effected_tile = False
                    player.clear_effects()
                player.platform = (0,0,0)
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0

        for sprite in self.sprites['Platforms']:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.platform = (sprite.direction.x, sprite.direction.y, sprite.speed)
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    if sprite.direction.y > 0:
                        player.rect.y += sprite.direction.y * sprite.speed + 1
    
        for sprite in self.sprites['Enemy']:
            if sprite.rect.colliderect(player.rect):
                player.effects['damage'] = 1
                #player.load_save()

    def enemy_collisions(self):
        for enemy in self.sprites['Enemy']:
            #enemy.apply_gravity()
            #enemy.rect.y += enemy.direction.y * enemy.speed
            sprite = pygame.sprite.spritecollide(enemy, self.sprites['Constraints'], False)
            if sprite:
                sprite = sprite[0]
                if enemy.direction.x > 0:
                    enemy.rect.right = sprite.rect.left
                elif enemy.direction.x < 0:
                    enemy.rect.left = sprite.rect.right

                if hasattr(enemy, 'following') and enemy.following:
                    enemy.barrier = True
                else:
                    enemy.reverse()
                enemy.direction.y = 0

    def platform_collisions(self):
        for platform in self.sprites['Platforms']:
            if pygame.sprite.spritecollide(platform, self.sprites['Constraints'], False):
                platform.reverse()
            
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            self.show_constraints = not self.show_constraints
        
        if keys[pygame.K_ESCAPE]:
            self.get_action('to_options')(True)
        if keys[pygame.K_p]:
            for text in self.ui_overlay.texts:
                text.update('Paused')
    
    def update(self):
        if self.win:
            self.create_overworld(self.surface,self.selected_level+1, self.selected_level+1)

        for text in self.ui_overlay.texts:
            if text.id == 'keys':
                text.update('Keys: {}'.format(self.player.keys))
            elif text.id == 'deaths':
                text.update('Deaths: {}'.format(self.player.death_counter))
            elif text.id == 'timer':
                seconds = (pygame.time.get_ticks()-self.start_time)//1000
                minutes = seconds//60
                seconds = seconds%60
                text.update(f'Time: {str(int(minutes)).zfill(2)}:{str(int(seconds)).zfill(2)}')

        for enemy in self.sprites['Enemy']:
            if hasattr(enemy, 'bullets') and enemy.bullets:
                for bullet in  enemy.return_bullets():
                    self.sprites['Bullet'].add(bullet)
                enemy.clear_bullets()
    
    def run(self):
        self.input()

        #Update
        self.update()
        for key, group in self.sprites.items():
            if key == 'Enemy':
                group.update(self.world_shift, self.player)
                self.enemy_collisions()
            else:
                group.update(self.world_shift)
            if key == 'Player':
                #self.scroll_x()
                for player in group:
                    player.get_input(self.sprites)
                    self.vertical_collisions(player)
                    self.horizontal_collisions(player)

                    if player.win:
                        self.win = True
            if key == 'Bullet':
                for bullet in group:

                    if pygame.sprite.spritecollide(bullet, self.sprites['Enemy'], False):
                        group.remove(bullet)
                    if pygame.sprite.spritecollide(bullet, self.sprites['Terrain'], False):
                        for entity in pygame.sprite.spritecollide(bullet, self.sprites['Terrain'], False):
                            if type(entity) == SaveBlock:
                                entity.effect(player)
                        group.remove(bullet)
                    ##TODO: extend range?
                    if bullet.rect.x > screen_width or bullet.rect.x < 0:
                        group.remove(bullet)
            if key == 'Platforms':
                self.platform_collisions()

        self.surface.fill((162, 235, 250))
        #Draw
        for key, group in self.sprites.items():
            if self.show_constraints or key != 'Constraints':
                group.draw(self.surface)

        self.ui_overlay.run()
