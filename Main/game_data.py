from level_data import *
from menu_items import Text, Button

levels = {
    1: {'position': (625, 400), 'path': 'assets/levels/level_1', 'data': level_1},
    2: {'position': (1050, 400), 'path': 'assets/levels/level_2', 'data': level_2},
    3: {'position': (1475, 400), 'path': 'assets/levels/level_3', 'data': level_3},
    4: {'position': (1900, 400), 'path': 'assets/levels/level_4'},
}

#Main Menu
mm_texts = [
    ((625, 75), "Talon's Adventure", 100),
]

mm_buttons = [
    ((625, 400), "Play", False, 'to_overworld'),
    ((625, 500), "Options", False, 'to_options'),
    ((625, 600), "Quit", False, 'quit_game')
]

#Options menu
op_texts = [
    ((625, 75), "Options", 40),
    ((625, 300), "Inputs", 40),
    ((625, 400), "Sound", 40),
    ((625, 500), "Resolution", 40),
]
op_buttons = [
    ((625, 600), "To Main Menu", False, 'to_main_menu'),
    ((625, 700), "Back To Game", True, 'to_level'),
    ((625, 650), "To Level Selection", False, 'to_overworld'),
]

#UI overlay
ui_texts = [
    ((10, 10), "Time: 00:00", 20, (0,0,0), 'topleft', 'timer'),
    ((10, 30), "Deaths: 0", 20, (0,0,0), 'topleft', 'deaths'),
    ((10, 50), "Keys: 0", 20, (0,0,0), 'topleft', 'keys'),
]

#Name input
ni_texts = [
    ((625, 75), "Enter your name", 40),
]

ni_buttons = [
    ((625, 650), "Back To Main Menu", False, 'to_main_menu'),
    ((625, 600), "Play", False, 'to_overworld'),
]

#Menus
menus = {
    'main_menu': {'texts': mm_texts, 'buttons': mm_buttons, 'background': ''},
    'options': {'texts': op_texts, 'buttons': op_buttons, 'background': ''},
    'ui_overlay': {'texts': ui_texts, 'buttons': [], 'background': ''},
    'name_input': {'texts': ni_texts, 'buttons': ni_buttons, 'background': ''},
}