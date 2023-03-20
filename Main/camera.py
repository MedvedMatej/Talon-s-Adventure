import pygame
from settings import screen_height, screen_width
class BoxCamera(pygame.sprite.Group):
    def __init__(self, get_action):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.display_surface = pygame.Surface((screen_width, screen_height))
        self.get_action = get_action

        #camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_width() / 2
        self.half_h = self.display_surface.get_height() / 2

        #box
        self.camera_borders = {'left': 200, 'right': 200, 'top': 200, 'bottom': 200} #{'left': 624, 'right': 624, 'top': 350, 'bottom': 350}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_width() - self.camera_borders['left'] - self.camera_borders['right']
        h = self.display_surface.get_height() - self.camera_borders['top'] - self.camera_borders['bottom']
        self.camera_rect = pygame.Rect(l, t, w, h)

    def box_target(self, target):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom
        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def custom_draw(self, player, sprites, ui, show_constraints=False):
        self.box_target(player)

        for key, group in sprites.items():
            for sprite in group.sprites():
                #Skip sprites that are not on screen
                #X-axis
                if sprite.rect.right < self.offset.x or sprite.rect.left > self.offset.x + self.display_surface.get_width():
                    continue
                #Y-axis
                if sprite.rect.bottom < self.offset.y or sprite.rect.top > self.offset.y + self.display_surface.get_height():
                    continue

                if show_constraints or key != 'Constraints':
                    offset_pos = sprite.rect.topleft - self.offset
                    self.display_surface.blit(sprite.image, offset_pos)
        
        ui.buttons.draw(self.display_surface)
        ui.texts.draw(self.display_surface)

        self.screen.blit(pygame.transform.scale(self.display_surface, self.screen.get_rect().size), (0, 0))
        self.display_surface.fill((162, 235, 250))

