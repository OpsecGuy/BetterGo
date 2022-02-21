import PySimpleGUI as gui
import random

class GUI():
    def __init__(self) -> None:
        gui.theme_text_color('white')
        self.screen_size = gui.Window.get_screen_size()
    
    def set_random_name(self) -> None:
        strings = ['A',
        'B', 'C', 'D', 'E', 'F','G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'U', 'P', 'R', 'S', 'T', 'W', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f','g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'u', 'p', 'r', 's', 't', 'w', 'y', 'z',
        '1','2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '^', '&', '&', '(', ')', '-', '_', '=', '+']
        return ''.join(random.choice(strings) for _ in range(10, 15))

    def main_gui_layout(self):
        return[
            [gui.Checkbox('Glow ESP', default=False, key='glow_esp_checkbox')],
            [gui.Checkbox('Auto Pistol', default=True, key='auto_pistol_checkbox')],
            [gui.Checkbox('TriggerBot', default=False, key='trigger_bot_checkbox')],
            [gui.Checkbox('BunnyHop', default=True, key='bunny_hop_checkbox')],
            [gui.Checkbox('RadarHack', default=True, key='radar_hack_checkbox')],
            [gui.Checkbox('No Smoke', default=False, key='no_smoke_checkbox')],
            [gui.Checkbox('Hit Sound', default=False, key='hit_sound_checkbox')],
            # [gui.Text('', key='whitespace_text')],
            [gui.Text('FOV:', key='fov_text', justification='left'), gui.Text('', key='print_fov_value')],
            [gui.Slider(range=(70,160), disable_number_display=True, default_value=90, orientation ='horizontal', size=(20, 8), key='fov_value')],
            ]
    	
    def create_main_gui(self):
        gui.theme('Dark')
        window = gui.Window(self.set_random_name(), self.main_gui_layout(),
            resizable=True, no_titlebar=False, finalize=True,
            grab_anywhere=True, keep_on_top=False, alpha_channel=1,
            location=(self.screen_size[0] / 2, self.screen_size[1] / 2))
        return window

    def spectator_list_layout(self):
        return[
            [gui.Text('Spectator list', key='spec_list_text')],
            [gui.Text('', key='spec_list')]]

    def create_spectator_list(self):
        gui.theme('DarkTeal4')
        window = gui.Window(self.set_random_name(), self.spectator_list_layout(),
            resizable=True, no_titlebar=True,
            finalize=True, grab_anywhere=True, keep_on_top=True, 
            alpha_channel=0.7, element_justification='center',
            location=(5, self.screen_size[1] / 2))
        return window