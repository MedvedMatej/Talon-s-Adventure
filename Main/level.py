import pygame
from tile import Tile, StaticTile, AnimatedTile, Player, Enemy
from settings import tile_size, player_speed, screen_width, screen_height
from collections import defaultdict
from imports import import_csv_layout, import_cut_graphics, import_folder
from background import Background
class Level:
    def __init__(self, level_data, surface):
        self.sprites = defaultdict(pygame.sprite.Group)
        self.sprites_graphics = defaultdict(list)
        self.sprites_scale = defaultdict(int)
        self.display_surface = surface
        self.background = Background(level_data['background'], self.display_surface)

        #Set world layout and scale
        self.terrain_layout = import_csv_layout(level_data['Terrain'])
        self.sprites_scale['Terrain'] = 4
        self.decoration_layout = import_csv_layout(level_data['Decorations'])
        self.sprites_scale['Decorations'] = 4
        self.collectables_layout = import_csv_layout(level_data['Collectables'])
        self.sprites_scale['Collectables'] = 4
        self.constraints_layout = import_csv_layout(level_data['Constraints'])
        self.sprites_scale['Constraints'] = 4
        #Animated
        self.player_layout = import_csv_layout(level_data['Player'])
        self.sprites_scale['Player'] = 4
        self.enemy_layout = import_csv_layout(level_data['Enemy'])
        self.sprites_scale['Enemy'] = 4
        
        #Import graphics
        self.sprites_graphics['Terrain'] = import_cut_graphics('./assets/background/tileset.png')
        self.sprites_graphics['Decorations'] = import_cut_graphics('./assets/background/tileset.png')
        self.sprites_graphics['Collectables'] = import_cut_graphics('./assets/background/tileset.png')
        self.sprites_graphics['Constraints'] = import_cut_graphics('./assets/background/tileset.png')
        #Animated
        
        #Create tile groups
        self.create_tile_group(self.terrain_layout, 'Terrain')
        self.create_tile_group(self.decoration_layout, 'Decorations')
        self.create_tile_group(self.collectables_layout, 'Collectables')
        self.create_tile_group(self.constraints_layout, 'Constraints')
        #Animated
        self.create_tile_group(self.player_layout, 'Player', animated=True)
        self.create_tile_group(self.enemy_layout, 'Enemy', animated=True)

        self.world_shift = 0

    def create_tile_group(self, layout, tile_type, animated=False):
        sprite_group = pygame.sprite.Group()

        for row, tiles in enumerate(layout):
            for column, tile in enumerate(tiles):
                if tile != '-1':
                    if animated:
                        tileClass = globals()[tile_type]
                        sprite = tileClass((column*tile_size*self.sprites_scale[tile_type], row*tile_size*self.sprites_scale[tile_type]), tile_size*self.sprites_scale[tile_type], f'./assets/{tile_type.lower()}/walk')
                        self.sprites[tile_type].add(sprite)
                    else:
                        tile_surface = self.sprites_graphics[tile_type][int(tile)]
                        sprite = StaticTile((column*tile_size*self.sprites_scale[tile_type], row*tile_size*self.sprites_scale[tile_type]),tile_size*self.sprites_scale[tile_type], tile_surface)
                        self.sprites[tile_type].add(sprite)

        return sprite_group

    def scroll_x(self):
        player = self.player.sprite
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

    def horizontal_collisions(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                elif player.direction.x < 0:
                    player.rect.left = sprite.rect.right
    
    def vertical_collisions(self):
        player = self.player.sprite
        player.apply_gravity()
        player.rect.y += player.direction.y * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
    
    def enemy_collisions(self):
        for enemy in self.sprites['Enemy']:
            #enemy.apply_gravity()
            #enemy.rect.y += enemy.direction.y * enemy.speed
            if pygame.sprite.spritecollide(enemy, self.sprites['Constraints'], False):
                enemy.reverse()
                enemy.direction.y = 0
            

    def run(self):
        """
        self.scroll_x()

        self.player.update()
        self.vertical_collisions()
        self.horizontal_collisions()
        self.player.draw(self.display_surface) """
        #self.background.draw()
        #Update
        for key, group in self.sprites.items():
            group.update(self.world_shift)
            if key == 'Enemy':
                self.enemy_collisions()

        #Draw
        for key, group in self.sprites.items():
            if key != 'Constraints':
                group.draw(self.display_surface)
