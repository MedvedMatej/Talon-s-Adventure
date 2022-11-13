import pygame, sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Talon's Adventure")
clock = pygame.time.Clock()

class Object(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, image_path) -> None:
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)

background = pygame.image.load("assets/background.png")
monster = pygame.image.load("assets/monster.png")
player = pygame.image.load("assets/character.png")
BLACK = (0, 0, 0)

def get_image(sprite, x, y, width, height, scale, color):
    image = pygame.Surface((width, height))
    image.blit(sprite, (0, 0), (x, y, x+width, y+height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    return image

player = get_image(player, 0, 0, 30, 50, 4, BLACK)
monster = get_image(monster, 0, 0, 30, 50, 2, BLACK)
background_tile = get_image(background,130 ,20 , 90, 50, 1, BLACK)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((255, 255, 255))
    screen.blit(player, (0, 0))
    screen.blit(monster, (190, 110))

    screen.blit(background_tile, (50, 150))
    screen.blit(background_tile, (150, 210))
    screen.blit(background_tile, (200, 210))

    #screen.blit(background, (0, 0))
    pygame.display.update()
    clock.tick(60)