import PySimpleGUI as gui

class GUI():
    def __init__(self) -> None:
        gui.theme_text_color('white')
        self.screen_size = gui.Window.get_screen_size()
        
    def main_gui_layout(self):
        return[
            [gui.Text('BetterGo by MaGicSuR', key='main_gui_title', justification='center')],
            [gui.Checkbox('Glow ESP', default=False, key='glow_esp_checkbox')],
            [gui.Checkbox('Auto Pistol', default=False, key='auto_pistol_checkbox')],
            [gui.Checkbox('TriggerBot', default=False, key='trigger_bot_checkbox')],
            [gui.Checkbox('BunnyHop', default=False, key='bunny_hop_checkbox')],
            [gui.Checkbox('RadarHack', default=False, key='radar_hack_checkbox')],
            [gui.Checkbox('No Smoke', default=False, key='no_smoke_checkbox')],
            [gui.Checkbox('Hit Sound', default=False, key='hit_sound_checkbox')],
            # [gui.Text('', key='whitespace_text')],
            [gui.Text('FOV:', key='fov_text', justification='left'), gui.Text('', key='print_fov_value')],
            [gui.Slider(range=(70,160), disable_number_display=True, default_value=90, orientation ='horizontal', size=(20, 5), key='fov_value')],
            [gui.Text('Exit key: DEL', key='whitespace_text')],
            ]
    	
    def create_main_gui(self):
        gui.theme('Dark')
        window = gui.Window('_', self.main_gui_layout(),
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
        window = gui.Window('_', self.spectator_list_layout(),
            resizable=True, no_titlebar=True,
            finalize=True, grab_anywhere=True, keep_on_top=True, 
            alpha_channel=0.7, element_justification='center',
            location=(5, self.screen_size[1] / 2))
        return window