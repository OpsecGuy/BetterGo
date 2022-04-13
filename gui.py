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

    def visuals_tab_layout(self):
        return[
            [gui.Checkbox('Player ESP', default=True, key='player_esp_checkbox')],
            [gui.Checkbox('Item ESP', default=False, key='item_esp_checkbox')],
            ]

    def aim_tab_layout(self):
        return[
            [gui.Checkbox('RCS', default=False, key='rcs_checkbox')],
            [gui.Text('RCS:', key='rcs_text', justification='left'), gui.Text('', key='print_smooth_value')],
            [gui.Slider(range=[0.0, 2.0], resolution=0.1, disable_number_display=True, default_value=1.6, orientation ='horizontal', size=(20, 8), key='rcs_smooth_value')],
            [gui.Text('RCS after x shots', size=(15, 1)), gui.Spin(values=[i for i in range(0, 100)], initial_value=2, size=(4, 1), key='rcs_shots_fired')],
            [gui.HorizontalSeparator(color='Black')],
            [gui.Checkbox('TriggerBot', default=True, key='trigger_bot_checkbox')],
            [gui.Text('Delay (sec):', key='triggerbot_delay_text', justification='left'), gui.Text('', key='print_triggerbot_delay')],
            [gui.Checkbox('Humanization', default=False, key='trigger_bot_humanization_checkbox')],
            [gui.Slider(range=[0.01, 0.1], resolution=0.005, disable_number_display=True, default_value=0.025, orientation ='horizontal', size=(20, 8), key='triggerbot_delay_value')],]

    def misc_tab_layout(self):
        return[
            [gui.Checkbox('Auto Pistol', default=True, key='auto_pistol_checkbox')],
            [gui.Checkbox('RadarHack', default=False, key='radar_hack_checkbox')],
            [gui.Checkbox('Hit Sound', default=False, key='hit_sound_checkbox')],
            [gui.Checkbox('BunnyHop', default=True, key='bunny_hop_checkbox')],
            [gui.Checkbox('No Smoke', default=False, key='no_smoke_checkbox')],

            [gui.Checkbox('No Flash', default=False, key='no_flash_checkbox')],
            [gui.Text('Strength:', key='no_flash_text', justification='left'), gui.Text('', key='print_no_flash_value')],
            [gui.Slider(range=[0.0, 255.0], resolution=1.0, disable_number_display=True, default_value=80.0, orientation ='horizontal', size=(20, 8), key='no_flash_strength')],

            [gui.Checkbox('Night Mode', default=False, key='nightmode_checkbox')],
            [gui.Text('Strength:', key='nightmode_text', justification='left'), gui.Text('', key='print_nightmode_value')],
            [gui.Slider(range=[0.1, 3.0], resolution=0.1, disable_number_display=True, default_value=1.0, orientation ='horizontal', size=(20, 8), key='nightmode_strength')],
            # [gui.Text('', key='whitespace_text')],
            [gui.Text('FOV:', key='fov_text', justification='left'), gui.Text('', key='print_fov_value')],
            [gui.Slider(range=(70, 160), disable_number_display=True, default_value=90.0, orientation ='horizontal', size=(20, 8), key='fov_value')],
            [gui.HorizontalSeparator(color='Black')],
            [gui.Text('Panic Key: DEL', key='panic_key_text')],]

    def main_gui_layout(self):
        return[
            [gui.TabGroup([[gui.Tab('Visuals', self.visuals_tab_layout()), gui.Tab('Aim', self.aim_tab_layout()), 
            gui.Tab('Misc', self.misc_tab_layout())]])],]
            
    def spectator_list_layout(self):
        return[
            [gui.Text('Spectator list', key='spec_list_text')],
            [gui.Text('', key='spec_list')]]
    
    def player_info_layout(self):
        return[
            [gui.Text('Player info', key='playerinfo_text')],
            [gui.Text('', key='playerinfo')]]
    	
    def create_main_gui(self):
        gui.theme('Dark')
        window = gui.Window(self.set_random_name(), self.main_gui_layout(),
            resizable=True, no_titlebar=False, finalize=True,
            grab_anywhere=True, keep_on_top=False, alpha_channel=1,
            location=(self.screen_size[0] / 2, self.screen_size[1] / 2))
        return window

    def create_spectator_list(self):
        gui.theme('DarkTeal4')
        window = gui.Window(self.set_random_name(), self.spectator_list_layout(),
            resizable=True, no_titlebar=True,
            finalize=True, grab_anywhere=True, keep_on_top=True, 
            alpha_channel=0.7, element_justification='center',
            location=(5, self.screen_size[1] / 2))
        return window
    
    def create_playerinfo_table(self):
        gui.theme('DarkTeal4')
        window = gui.Window(self.set_random_name(), self.player_info_layout(),
            resizable=True, no_titlebar=True,
            finalize=True, grab_anywhere=True, keep_on_top=True, 
            alpha_channel=0.7, element_justification='center',
            location=(5, self.screen_size[1] / 2))
        return window