import pygame
import os
from settings import *

def import_csv_layout(file_path):
    layout = []
    with open(file_path, 'r') as file:
        for line in file:
            layout.append(line.strip().split(','))
    return layout

def import_cut_graphics(file_path, width=tile_size, height=tile_size, scale=4):
    tiles = []
    sheet = pygame.image.load(file_path).convert_alpha()
    for row in range(sheet.get_height()//height):
        for column in range(sheet.get_width()//width):
            new_sheet = pygame.Surface((width, height), flags=pygame.SRCALPHA)
            new_sheet.blit(sheet, (0,0), (column*width, row*height, column*width+width, row*height+height))
            new_sheet = pygame.transform.scale(new_sheet, (width*scale*global_scale, height*scale*global_scale))
            tiles.append(new_sheet)
    return tiles

def import_folder(folder_path, scale=4):
    animations = {}
    for root, _, files in (os.walk(folder_path)):
        if len(files) > 0:
            images = []
            for file in files:
                if file.endswith('.png'):
                    image = pygame.image.load(os.path.join(root, file)).convert_alpha()
                    image = pygame.transform.scale(image, (tile_size*scale*global_scale, tile_size*scale*global_scale))
                    images.append(image)
            animations[root.split("/")[-1]] = images

    return animations

            