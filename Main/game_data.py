from level_data import *
from menu_items import Text, Button
import pygame
#pygame.init()
pygame.font.init()

levels = {
    1: {'position': (625, 325), 'path': 'assets/levels/level_1', 'data': level_1},
    2: {'position': (1050, 325), 'path': 'assets/levels/level_2', 'data': level_2},
    3: {'position': (1475, 325), 'path': 'assets/levels/level_3', 'data': level_3},
    4: {'position': (1900, 325), 'path': 'assets/levels/level_4', 'data': level_4},
    5: {'position': (2325, 325), 'path': 'assets/levels/level_4'},
    6: {'position': (2750, 325), 'path': 'assets/levels/level_4'},
    7: {'position': (3175, 325), 'path': 'assets/levels/level_4'},
    8: {'position': (3600, 325), 'path': 'assets/levels/level_4'},
    9: {'position': (4025, 325), 'path': 'assets/levels/level_4'},
    10: {'position': (4450, 325), 'path': 'assets/levels/level_4'},
}

#Main Menu
mm_texts = [
    Text(position=(625, 125), text="Talon's Adventure", size=100, color=(255,255,255)),
]

mm_buttons = [
    Button(position=(625, 400), text="Play", action="to_overworld", image=("assets/menu_assets/button_long.png"), offset=(-25, -25)),
    Button(position=(625, 500), text="Options", action="to_options", image=("assets/menu_assets/button_long.png"), offset=(-25, -25)),
    Button(position=(625, 600), text="Credits", action="to_credits", image=("assets/menu_assets/button_long.png"), offset=(-25, -25)),
    Button(position=(625, 700), text="Quit", action="quit_game", image=("assets/menu_assets/button_long.png"), offset=(-25, -25)),
]

#Options menu
op_texts = [
    Text(position=(625, 75), text="Options", size=70),
    #Text(position=(625, 300), text="Inputs", size=40),
    Text(position=(625, 200), text="SFX Volume", size=40),
    Text(position=(625, 250), text="100", size=40, id="sfx_volume"),
    Text(position=(625, 350), text="Music Volume", size=40),
    Text(position=(625, 400), text="100", size=40, id="music_volume"),
]
op_buttons = [
    Button(position=(625, 550), text="Main Menu", action="to_main_menu", image=("assets/menu_assets/button_long.png"), offset=(-25, -25)),
    Button(position=(625, 700), text="Back To Game", action="to_level", image=("assets/menu_assets/button_long.png"), offset=(-25, -25), id="back_to_game"),
    Button(position=(625, 625), text="Level Selection", action="to_overworld", image=("assets/menu_assets/button_long.png"), offset=(-25, -25)),
    Button(position=(550, 250), text="-", action="sfx_down", image=("assets/menu_assets/button_short_left.png")),
    Button(position=(550, 400), text="-", action="music_down", image=("assets/menu_assets/button_short_left.png")),
    Button(position=(700, 250), text="+", action="sfx_up", image=("assets/menu_assets/button_short_right.png")),
    Button(position=(700, 400), text="+", action="music_up", image=("assets/menu_assets/button_short_right.png")),
]

#UI overlay
ui_texts = [
    Text(position=(10,10), text="Time: 00:00", size=30, color=(0,0,0), position_type='topleft', id='timer'),
    Text(position=(10,30), text="Deaths: 0", size=30, color=(0,0,0), position_type='topleft', id='deaths'),
    Text(position=(10,50), text="Keys: 0", size=30, color=(0,0,0), position_type='topleft', id='keys'),
]

#Name input
ni_texts = [
    Text((625, 75), "Enter your name", 70),
]

ni_buttons = [
    Button(position=(625,650), text="Main Menu", action="to_main_menu", image=("assets/menu_assets/button_long.png"), offset=(-25, -25)),
    Button(position=(625,550), text="Play", action="to_tutorial", image=("assets/menu_assets/button_long.png"), offset=(-25, -25)),
]

#Leaderboard
lb_texts = [
    Text((625, 75), "Leaderboard", 70),
]

lb_buttons = [
    Button(position=(625, 725), text="Level Selection", action="to_overworld", image=("assets/menu_assets/button_long.png"), offset=(-25, -25)),
]

#Credits menu
cr_texts = [
    Text((625, 75), "Credits", 70),
]

with open('./assets/credits.txt', 'r') as f:
    credits = f.read().splitlines()

    for i, line in enumerate(credits):
        text = Text((100, 150 + (i * 50)), line, 30, position_type='topleft')
        cr_texts.append(text)


cr_buttons = [
    Button(position=(625, 725), text="Main Menu", action="to_main_menu", image=("assets/menu_assets/button_long.png"), offset=(-25, -25)),
]

#Menus
menus = {
    'main_menu': {'texts': mm_texts, 'buttons': mm_buttons, 'background': ''}, #./assets/background/background2.png
    'options': {'texts': op_texts, 'buttons': op_buttons, 'background': ''},
    'ui_overlay': {'texts': ui_texts, 'buttons': [], 'background': ''},
    'name_input': {'texts': ni_texts, 'buttons': ni_buttons, 'background': ''},
    'leaderboard': {'texts': lb_texts, 'buttons': lb_buttons, 'background': ''},
    'credits': {'texts': cr_texts, 'buttons': cr_buttons, 'background': ''},
}