import pygame, sys
from settings import *
from level import Level
from menus import Overworld, Menu, Button, Text, InputMenu

import json

class Game:
    def __init__(self):
        #Starting values
        self.max_level = 2
        self.selected_level = 1

        #Audio
        self.sounds = {}
        self.music = None
        self.set_sounds()
        self.music.play(loops=-1)

        #Setup states
        self.level = None
        self.overworld = Overworld(screen, self.selected_level, self.max_level, level_method = self.create_level, get_action = self.get_action)
        self.main_menu = Menu(screen, self.get_action, 'main_menu')
        self.options = Menu(screen, self.get_action, 'options')
        self.name_input = InputMenu(screen, self.get_action, 'name_input')
        self.input_text = ""
        
        self.status = 'main_menu'
        
        #Event data
        self.clicks = []

        #settings
        self.sfx_volume = 1
        self.music_volume = 1
        self.controls = {}
        self.load_settings()
        self.apply_settings()

    def set_sounds(self):
        self.sounds['hit'] = pygame.mixer.Sound('./assets/audio/effects/hit.wav')
        self.sounds['jump'] = pygame.mixer.Sound('./assets/audio/effects/jump.wav')
        self.sounds['coin'] = pygame.mixer.Sound('./assets/audio/effects/coin.wav')

        self.music = pygame.mixer.Sound('./assets/audio/ambient_music.wav')

    def get_sounds(self):
        return self.sounds

    def set_sound_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)
        self.save_settings()

        #Update label
        for text in self.options.texts:
            if text.id == 'sfx_volume':
                text.update(str(round(volume*100)))
                print("sfx")
                print(self.sfx_volume)

    def set_music_volume(self, volume):
        self.music.set_volume(volume)
        self.save_settings()

        #Update label
        for text in self.options.texts:
            if text.id == 'music_volume':
                text.update(str(round(volume*100)))

    def music_down(self):
        self.music_volume -= 0.05

        if self.music_volume < 0:
            self.music_volume = 0

        self.set_music_volume(self.music_volume)

    def music_up(self):
        self.music_volume += 0.05

        if self.music_volume > 1:
            self.music_volume = 1

        self.set_music_volume(self.music_volume)

    def sfx_down(self):
        self.sfx_volume -= 0.05

        if self.sfx_volume < 0:
            self.sfx_volume = 0

        self.set_sound_volume(self.sfx_volume)

    def sfx_up(self):
        self.sfx_volume += 0.05
        
        if self.sfx_volume > 1:
            self.sfx_volume = 1

        self.set_sound_volume(self.sfx_volume)


    def load_settings(self):
        with open('settings.json', 'r') as f:
            data = json.load(f)
        if 'sfx_volume' in data:
            self.sfx_volume = data['sfx_volume']
        
        if 'music_volume' in data:
            self.music_volume = data['music_volume']

        if 'controls' in data:
            self.controls = data['controls']

    def save_settings(self):
        data = {
            'sfx_volume': self.sfx_volume,
            'music_volume': self.music_volume,
            'controls': self.controls
        }
        with open('settings.json', 'w') as f:
            json.dump(data, f)

    def apply_settings(self):
        self.set_sound_volume(self.sfx_volume)
        self.set_music_volume(self.music_volume)
        self.set_controls(self.controls)
    
    def set_controls(self, controls):
        #TODO
        pass
    
    def create_level(self, level, surface):
        self.selected_level = level
        self.level = Level(level, surface, self.create_overworld, self.get_action)
        self.status = 'level'

    def create_overworld(self, surface, current_level, max_level):
        if self.max_level < max_level:
            self.max_level = max_level
        self.overworld = Overworld(surface, current_level, self.max_level, level_method = self.create_level, get_action = self.get_action)
        self.status = 'overworld'
    
    def quit_game(self):
        pygame.quit()
        sys.exit()

    def get_action(self, action):
        return getattr(self, action)

    def get_selected_level(self):
        return self.overworld.selected_level

    def to_options(self, show_hidden=False):
        self.options.show_hidden = show_hidden
        self.status = 'options'

    def to_main_menu(self):
        self.status = 'main_menu'
    
    def to_overworld(self):
        if self.input_text:
            self.status = 'overworld'
        else:
            self.status = 'name_input'

    def to_level(self):
        self.status = 'level'

    def run(self):
        if self.status == 'name_input':
            self.name_input.run(self.clicks, self.input_text)
        elif self.status == 'main_menu':
            self.main_menu.run(self.clicks)
        elif self.status == 'options':
            self.options.run(self.clicks)
        elif self.status == 'overworld':
            self.overworld.run(self.clicks)
        elif self.status == 'level':
            self.level.run()
        self.clicks = []

#Initialize pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Talon's Adventure")
clock = pygame.time.Clock()
game = Game()
#bullet_sound  = pygame.mixer.Sound('./assets/audio/effects/hit.wav')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.quit_game()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                game.clicks.append(mouse_pos)
        if event.type == pygame.KEYDOWN:
            if game.status == 'name_input':
                if event.key == pygame.K_BACKSPACE:
                    game.input_text = game.input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(game.input_text) >= 3:
                        game.create_overworld(screen, game.selected_level, game.max_level)
                elif len(game.input_text) < 16:
                    game.input_text += event.unicode
            
    game.run()
    pygame.display.update()
    clock.tick(60)