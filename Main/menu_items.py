import pygame

class Text(pygame.sprite.Sprite):
    def __init__(self, position, text, size=30, color=(255, 255, 255), position_type='center', id=None):
        super().__init__()
        self.id = id
        self.color = color
        self.position_type = position_type
        self.position = position
        self.font = pygame.font.SysFont('Klavika Bd', size)
        self._text = text
        self.text = self.font.render(text, True, color)
        self.size = self.text.get_size()
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)

        if self.position_type == 'topleft':
            self.rect = self.image.get_rect(topleft=self.position)
        else:
            self.rect = self.image.get_rect(center=self.position)

        self.image.blit(self.text, (0, 0))

    def update(self, text):
        self.text = self.font.render(text, True, self.color)
        self.size = self.text.get_size()
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        #self.rect = self.image.get_rect(center=self.position)
        self.image.blit(self.text, (0, 0))


class Button(pygame.sprite.Sprite):
    def __init__(self, position, image=None, text=None, hidden=False, action=None, get_action=None, offset=(0,0), screen=[], id=None):
        super().__init__()

        self.action = action
        self.args = screen
        self.id = id
        
        self.color = (0,0,0)
        self.hover_color = (255,255,255)
        self.offset = offset

        if get_action:
            self.get_action = get_action
            self.call_action = get_action(action)
        else:
            self.get_action = None
            self.call_action = None

        self.font = pygame.font.SysFont('Klavika Bd', 45)
        self.text = text
        self._text = self.font.render(self.text, True, self.color)
        self._htext = self.font.render(self.text, True, self.hover_color)



        if not image:
            self.size = self._text.get_size()
            self.image = pygame.Surface(self.size)
            self.rect = self.image.get_rect(center=position)
            self.image.fill((0, 0, 0))
            self.image.blit(self._text, (0, 0))
            self.actual_rect = self.rect
        else:
            
            self._image = pygame.image.load(image)
            self._himage = pygame.image.load(image)
            self.rect = self._image.get_rect(center=position)
            self.rect[0] += offset[0]/2
            self.rect[1] += offset[1]
            x,y,w,h = self.rect
            self.actual_rect = pygame.Rect(x-offset[0],y-offset[1],w+offset[0],h+offset[1])

            self._image.blit(self._text, (-self.offset[0]/2 + ((self.rect[2]-self._text.get_size()[0])/2), -self.offset[1]+12))
            self._himage.blit(self._htext, (-self.offset[0]/2 + ((self.rect[2]-self._htext.get_size()[0])/2), -self.offset[1]+12))

            self.image = self._himage

        #Hide functionality
        self.hidden = False

    def set_action(self, get_action):
        self.get_action = get_action
        self.call_action = get_action(self.action)
    
    def update(self, show_hidden=False, mouse_pos=None):
        if len(mouse_pos) == 2 and self.actual_rect.collidepoint(mouse_pos):
            self.image = self._himage
        else:
            self.image = self._image

        if self.id == 'back_to_game' and not self.get_action('level'):
            self.hidden = True
            self.image = pygame.Surface((0,0), pygame.SRCALPHA)
        else:
            self.hidden = False

    def click(self):
        if self.action and (not self.hidden):
            if self.action == 'create_level':
                selected_level = self.get_action('get_selected_level')()
                self.call_action(selected_level, *self.args)
            elif self.action == 'create_leaderboard':
                self.call_action(self.id, *self.args)
            else:
                self.call_action(*self.args)

class Node(pygame.sprite.Sprite):
    def __init__(self, position, unlocked=False, speed=5, image=None, id=None, get_action=None):
        super().__init__()
        self.image = image if image else pygame.Surface((350, 250))
        self.unlocked = unlocked
        self.pos = position
        self.speed = speed
        self.target = None
        self.id = id
        self.get_action = get_action
        
        #Leaderboard button
        self.buttons = pygame.sprite.Group()
        self.buttons.add(Button(position=(self.pos[0]+100, self.pos[1]-45), image='assets/menu_assets/leaderboard_icon.png', action='create_leaderboard', get_action=self.get_action, id = (self.id)))

        if not unlocked:
            self.image = pygame.image.load('assets/menu_assets/level_board_locked.png').convert_alpha()
        else:
            self.font = pygame.font.SysFont('Klavika Bd', 75)
            self.text = self.font.render(f'Level {str(self.id)}', True, (0,0,0))
            self.image.blit(self.text, (self.image.get_size()[0]/2 - self.text.get_size()[0]/2, 100))
        self.rect = self.image.get_rect(center=position)


    def update(self):
        self.rect.center = self.pos
        if self.target:
            if (self.target[0] - self.pos[0]) != 0:
                dir = (self.target[0] - self.pos[0]) / abs((self.target[0] - self.pos[0]))
                self.pos = (self.pos[0] + self.speed * dir, self.pos[1])

                if (dir < 0 and self.pos[0] <= self.target[0]) or (dir > 0 and self.pos[0] >= self.target[0]):
                    self.pos = self.target
                    self.target = None

        #self.buttons.update(mouse_pos=pygame.mouse.get_pos())
        for button in self.buttons:
            button.rect.center = (self.rect.center[0]+125, self.rect.center[1]-75)
            button.actual_rect = button.rect
