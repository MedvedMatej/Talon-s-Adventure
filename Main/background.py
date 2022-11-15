import pygame
from settings import screen_width, screen_height, tile_size, scale, ntiles_x, ntiles_y

class Background:
    def __init__(self, images, surface):
        self.surface = surface

        self.sky = pygame.image.load(images[0]).convert()
        self.ground = pygame.image.load(images[1]).convert()
        self.underground = pygame.image.load(images[2]).convert()

        self.sky = pygame.transform.scale(self.sky, (screen_width, screen_height))
        #self.ground = pygame.transform.scale(self.ground, (screen_width, tile_size*scale))
        #self.underground = pygame.transform.scale(self.underground, (screen_width, tile_size*scale))

    def draw(self, level=""):
        """ for y in range(ntiles_y):
            if y < self.horizon:
                self.surface.blit(self.sky, (0, y*tile_size*scale)) """
        self.surface.blit(self.sky, (0, 0))



