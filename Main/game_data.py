from level_data import *
from menu_items import Text, Button
import pygame
#pygame.init()
pygame.font.init()

levels = {
    1: {'position': (625, 400), 'path': 'assets/levels/level_1', 'data': level_1},
    2: {'position': (1050, 400), 'path': 'assets/levels/level_2', 'data': level_2},
    3: {'position': (1475, 400), 'path': 'assets/levels/level_3', 'data': level_3},
    4: {'position': (1900, 400), 'path': 'assets/levels/level_4'},
}

#Main Menu
mm_texts = [
    Text(position=(625, 125), text="Talon's Adventure", size=100, color=(255,255,255)),
]

mm_buttons = [
    Button(position=(625, 400), text="Play", action="to_overworld"),
    Button(position=(625, 500), text="Options", action="to_options"),
    Button(position=(625, 600), text="Quit", action="quit_game"),
]

#Options menu
op_texts = [
    Text(position=(625, 75), text="Options", size=70),
    Text(position=(625, 300), text="Inputs", size=40),
    Text(position=(625, 400), text="SFX Volume", size=40),
    Text(position=(625, 430), text="100", size=40, id="sfx_volume"),
    Text(position=(625, 500), text="Music Volume", size=40),
    Text(position=(625, 530), text="100", size=40, id="music_volume"),
]
op_buttons = [
    Button(position=(625, 600), text="Main Menu", action="to_main_menu"),
    Button(position=(625, 700), text="Back To Game", action="to_level"),
    Button(position=(625, 650), text="Level Selection", action="to_overworld"),
    Button(position=(580, 430), text="-", action="sfx_down"),
    Button(position=(580, 530), text="-", action="music_down"),
    Button(position=(670, 430), text="+", action="sfx_up"),
    Button(position=(670, 530), text="+", action="music_up"),
]

#UI overlay
ui_texts = [
    Text(position=(10,10), text="Time: 00:00", size=20, color=(0,0,0), position_type='topleft', id='timer'),
    Text(position=(10,30), text="Deaths: 0", size=20, color=(0,0,0), position_type='topleft', id='deaths'),
    Text(position=(10,50), text="Keys: 0", size=20, color=(0,0,0), position_type='topleft', id='keys'),
]

#Name input
ni_texts = [
    Text((625, 75), "Enter your name", 40),
]

ni_buttons = [
    Button(position=(625,650), text="Main Menu", action="to_main_menu"),
    Button(position=(625,600), text="Play", action="to_overworld"),
]

#Menus
menus = {
    'main_menu': {'texts': mm_texts, 'buttons': mm_buttons, 'background': ''}, #./assets/background/background2.png
    'options': {'texts': op_texts, 'buttons': op_buttons, 'background': ''},
    'ui_overlay': {'texts': ui_texts, 'buttons': [], 'background': ''},
    'name_input': {'texts': ni_texts, 'buttons': ni_buttons, 'background': ''},
}