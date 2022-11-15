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
            new_sheet = pygame.transform.scale(new_sheet, (width*scale, height*scale))
            tiles.append(new_sheet)
    return tiles

def import_folder(folder_path, scale=4):
    files = []
    for file in os.listdir(folder_path):
        if file.endswith('.png'):
            image = pygame.image.load(os.path.join(folder_path, file)).convert_alpha()
            image = pygame.transform.scale(image, (tile_size*scale, tile_size*scale))
            files.append(image)
    return files

            