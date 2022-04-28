import dearpygui.dearpygui as dpg
import helper as h
import random, win32gui

class GUI():
    def __init__(self) -> None:
        self.v1 = self.get_random_string()
        
    def get_random_string(self) -> None:
        strings = ['A',
        'B', 'C', 'D', 'E', 'F','G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'U', 'P', 'R', 'S', 'T', 'W', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f','g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'u', 'p', 'r', 's', 't', 'w', 'y', 'z',
        '1','2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '^', '&', '&', '(', ')', '-', '_', '=', '+']
        return ''.join(random.choice(strings) for _ in range(10, 15))
    
    def _log(self, sender, app_data, user_data):
        print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")
    
    def menu(self):
        dpg.create_context()
        dpg.create_viewport(title=self.v1, width=615, height=615)
        dpg.setup_dearpygui()
        
        with dpg.window(label='Menu', user_data='menu', tag='#menu', width=600, height=600, no_close=True, no_move=True):
            with dpg.collapsing_header(label="Aimbot"):
                dpg.add_checkbox(label='RCS', user_data='rcs_checkbox', tag='rcs_checkbox')
                dpg.add_slider_float(label='RCS Strength', default_value=0.0, min_value=0.0, max_value=2.0, user_data='rcs_strength', tag='rcs_strength')
                dpg.add_slider_int(label='Shot after x bullets', default_value=0, min_value=0, max_value=30, user_data='rcs_get_bullets', tag='rcs_get_bullets')
                dpg.add_separator()
                dpg.add_checkbox(label='TriggerBot', user_data='triggerbot_checkbox', tag='triggerbot_checkbox')
                dpg.add_checkbox(label='Humanization', user_data='humanization_checkbox', tag='humanization_checkbox')
                dpg.add_combo(label='Key', items=tuple(h._gui_keys_list.keys()), default_value='MOUSE 5', user_data='triggerbot_key', tag='triggerbot_key')
                dpg.add_slider_float(label='TriggerBot Delay', default_value=0.025, min_value=0.01, max_value=0.1, user_data='triggerbot_delay', tag='triggerbot_delay')
                dpg.add_separator()
                dpg.add_checkbox(label='Auto Pistol', user_data='autopistol_checkbox', tag='autopistol_checkbox')
                dpg.add_combo(label='Key', items=tuple(h._gui_keys_list.keys()), default_value='MOUSE 4', user_data='autopistol_key', tag='autopistol_key')
            with dpg.collapsing_header(label='Visuals'):
                dpg.add_checkbox(label='Player ESP', user_data='player_esp', tag='player_esp')
                dpg.add_checkbox(label='Team Check', user_data='player_esp_temates', tag='player_esp_temates')
                dpg.add_checkbox(label='Item ESP', user_data='item_esp', tag='item_esp')
                dpg.add_color_edit(label='Enemy team color', default_value=[124, 12, 51, 44], user_data='enemy_glow_color', tag='enemy_glow_color')
                dpg.add_color_edit(label='Team color', default_value=[42, 196, 15, 44], user_data='temates_glow_color', tag='temates_glow_color')
                dpg.add_separator()
                dpg.add_checkbox(label='Grenade Trajectory', user_data='grenade_checkbox', tag='grenade_checkbox')
            with dpg.collapsing_header(label='Misc'):
                dpg.add_checkbox(label='Radar Hack', user_data='radarhack_checkbox', tag='radarhack_checkbox')
                dpg.add_checkbox(label='Hit Sound', user_data='hitsound_checkbox', tag='hitsound_checkbox')
                dpg.add_checkbox(label='BunnyHop', user_data='bunnyhop_checkbox', tag='bunnyhop_checkbox')
                dpg.add_checkbox(label='No Smoke', user_data='nosmoke_checkbox', tag='nosmoke_checkbox')
                dpg.add_checkbox(label='No Flash', user_data='noflash_checkbox', tag='noflash_checkbox')
                dpg.add_slider_float(label='No Flash strength', default_value=255.0, min_value=0.0, max_value=255.0, user_data='noflash_strength', tag='noflash_strength')
                dpg.add_checkbox(label='Night Mode', user_data='nightmode_checkbox', tag='nightmode_checkbox')
                dpg.add_slider_float(label='Night Mode strength', default_value=0.3, min_value=0.01, max_value=3.0, user_data='nightmode_strength', tag='nightmode_strength')
                dpg.add_slider_int(label='FOV', default_value=90, min_value=60, max_value=160, user_data='fov', tag='fov')
                dpg.add_checkbox(label='Show FPS', user_data='fps_checkbox', tag='fps_checkbox')
            
            dpg.add_button(label='Unload', width=150, height=50, tag='unload_button')
            
        # with dpg.window(label='Spectators', user_data='menu2', tag='#menu2', autosize=True, no_background=True, no_close=True, pos=[5, h.ScreenSize().y / 2]): 
        #     dpg.add_text(label='spectator_list', tag='spectator_list')
        
        dpg.show_viewport()
