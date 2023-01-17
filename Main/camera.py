import pygame

class BoxCamera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        #camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_width() / 2
        self.half_h = self.display_surface.get_height() / 2

        #box
        self.camera_borders = {'left': 200, 'right': 200, 'top': 100, 'bottom': 100}
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

    def custom_draw(self, player, sprites, show_constraints=False):
        self.box_target(player)

        for key, group in sprites.items():
            for sprite in group.sprites():
                if show_constraints or key != 'Constraints':
                    offset_pos = sprite.rect.topleft - self.offset
                    self.display_surface.blit(sprite.image, offset_pos)
