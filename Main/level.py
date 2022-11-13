import pygame
from tile import Tile, StaticTile
from player import Player
from settings import tile_size, player_speed, screen_width, screen_height
from collections import defaultdict
class Level:
    def __init__(self, level_data, surface):
        self.sprites = defaultdict(pygame.sprite.Group)
        self.sprites_graphics = defaultdict(list)
        self.sprites_scale = defaultdict(int)
        self.display_surface = surface

        #Set world layout and scale
        self.terrain_layout = self.import_csv_layout(level_data['Terrain'])
        self.sprites_scale['Terrain'] = 4
        self.decoration_layout = self.import_csv_layout(level_data['Decorations'])
        self.sprites_scale['Decorations'] = 4
        self.collectables_layout = self.import_csv_layout(level_data['Collectables'])
        self.sprites_scale['Collectables'] = 4
        
        #Import graphics
        self.sprites_graphics['Terrain'] = self.import_cut_graphics('./assets/background/tileset.png')
        self.sprites_graphics['Decorations'] = self.import_cut_graphics('./assets/background/tileset.png')
        self.sprites_graphics['Collectables'] = self.import_cut_graphics('./assets/background/tileset.png')
        
        #Create tile groups
        self.create_tile_group(self.terrain_layout, 'Terrain')
        self.create_tile_group(self.decoration_layout, 'Decorations')
        self.create_tile_group(self.collectables_layout, 'Collectables')

        self.world_shift = 0

    def import_csv_layout(self, file_path):
        layout = []
        with open(file_path, 'r') as file:
            for line in file:
                layout.append(line.strip().split(','))
        return layout

    def import_cut_graphics(self, file_path, width=tile_size, height=tile_size, scale=4):
        tiles = []
        sheet = pygame.image.load(file_path).convert_alpha()
        for row in range(sheet.get_height()//height):
            for column in range(sheet.get_width()//width):
                new_sheet = pygame.Surface((width, height))
                new_sheet.blit(sheet, (0,0), (column*width, row*height, column*width+width, row*height+height))
                new_sheet = pygame.transform.scale(new_sheet, (width*scale, height*scale))
                tiles.append(new_sheet)
        return tiles

    def create_tile_group(self, layout, tile_type):
        sprite_group = pygame.sprite.Group()

        for row, tiles in enumerate(layout):
            for column, tile in enumerate(tiles):
                if tile != '-1':
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
    
    def run(self):
        """
        self.scroll_x()

        self.player.update()
        self.vertical_collisions()
        self.horizontal_collisions()
        self.player.draw(self.display_surface) """
        for key, group in self.sprites.items():
            group.update(self.world_shift)
            group.draw(self.display_surface)
