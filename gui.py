import dearpygui.dearpygui as dpg
import helper as h
import random, time

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
        dpg.create_viewport(title=self.v1, decorated=True, min_width=425, min_height=620, width=430, height=640)
        dpg.setup_dearpygui()

        with dpg.window(label='Menu', tag='menu', min_size=[425, 620], no_close=True, no_move=True, no_title_bar=True, horizontal_scrollbar=True):
            with dpg.collapsing_header(label="Aimbot", tag='aimbot_header'):
                dpg.add_checkbox(label='RCS', tag='rcs_checkbox')
                dpg.add_slider_float(label='RCS Strength', default_value=0.0, min_value=0.0, max_value=2.0, width=215, tag='rcs_strength')
                dpg.add_slider_int(label='Shot After x Bullets', default_value=0, min_value=0, max_value=30, width=215, tag='rcs_get_bullets')
                dpg.add_separator()
                dpg.add_checkbox(label='TriggerBot', tag='triggerbot_checkbox')
                dpg.add_checkbox(label='Humanization', tag='humanization_checkbox')
                dpg.add_combo(label='Key', items=tuple(h.gui_keys_list.keys()), default_value='MOUSE 5', width=215, tag='triggerbot_key')
                dpg.add_slider_float(label='TriggerBot Delay', default_value=0.025, min_value=0.01, max_value=0.1, width=215, tag='triggerbot_delay')
            with dpg.collapsing_header(label='Visuals', tag='visuals_header'):
                dpg.add_checkbox(label='Player ESP', tag='player_esp')
                dpg.add_checkbox(label='Team Check', tag='player_esp_temates')
                dpg.add_checkbox(label='Item ESP', tag='item_esp')
                dpg.add_color_edit(label='Enemy Team Color', default_value=[124, 12, 51, 44], tag='enemy_glow_color')
                dpg.add_color_edit(label='Team color', default_value=[42, 196, 15, 44], tag='mates_glow_color')
                dpg.add_separator()
                dpg.add_checkbox(label='Grenade Trajectory', tag='grenade_checkbox')
                dpg.add_checkbox(label='Night Mode', tag='nightmode_checkbox')
                dpg.add_slider_float(label='Night Mode Strength', default_value=0.3, min_value=0.01, max_value=3.0, width=215, tag='nightmode_strength')
                dpg.add_checkbox(label='No Flash', tag='noflash_checkbox')
                dpg.add_slider_float(label='No Flash Strength', default_value=255.0, min_value=0.0, max_value=255.0, width=215, tag='noflash_strength')
                dpg.add_slider_int(label='FOV', default_value=90, min_value=60, max_value=160, width=215, tag='fov')
                dpg.add_combo(label='Sky', items=list(h.sky_list), default_value='', width=215, tag='sky_name')
            with dpg.collapsing_header(label='Misc', tag='misc_header'):
                dpg.add_checkbox(label='Auto Pistol', tag='autopistol_checkbox')
                dpg.add_combo(label='Key', items=tuple(h.gui_keys_list.keys()), default_value='MOUSE 4', width=215, tag='autopistol_key')
                dpg.add_checkbox(label='Radar Hack', tag='radarhack_checkbox')
                dpg.add_checkbox(label='Hit Sound', tag='hitsound_checkbox')
                dpg.add_checkbox(label='BunnyHop', tag='bunnyhop_checkbox')
                dpg.add_checkbox(label='No Smoke', tag='nosmoke_checkbox')
                dpg.add_checkbox(label='Show FPS', tag='fps_checkbox')
                dpg.add_checkbox(label='Chat Spam', tag='chat_spam_checkbox')
                dpg.add_input_text(label='Command', width=215, tag='chat_spam_input')
                dpg.add_checkbox(label='Fake Lag', tag='fakelag_checkbox')
                dpg.add_slider_float(label='Fake Lag Strength', default_value=0.001, min_value=0.001, max_value=0.016, width=215, tag='fakelag_strength')
            dpg.add_button(label='Unload', width=150, height=30, tag='unload_button')
            
        # with dpg.window(label='Spectators', user_data='menu2', tag='#menu2', autosize=True, no_background=True, no_close=True, pos=[5, h.ScreenSize().y / 2]): 
        #     dpg.add_text(label='spectator_list', tag='spectator_list')
        
        dpg.show_viewport()

    def make_interactive(self):
        x2 = 0
        y2 = 0
        while True:
            try:
                dpg.hide_item('rcs_strength') if dpg.get_value('rcs_checkbox') == False else dpg.show_item('rcs_strength')
                dpg.hide_item('rcs_get_bullets') if dpg.get_value('rcs_checkbox') == False else dpg.show_item('rcs_get_bullets')
                dpg.hide_item('humanization_checkbox') if dpg.get_value('triggerbot_checkbox') == False else dpg.show_item('humanization_checkbox')
                dpg.hide_item('triggerbot_key') if dpg.get_value('triggerbot_checkbox') == False else dpg.show_item('triggerbot_key')
                dpg.hide_item('triggerbot_delay') if dpg.get_value('triggerbot_checkbox') == False else dpg.show_item('triggerbot_delay')
                dpg.hide_item('autopistol_key') if dpg.get_value('autopistol_checkbox') == False else dpg.show_item('autopistol_key')
                dpg.hide_item('chat_spam_input') if dpg.get_value('chat_spam_checkbox') == False else dpg.show_item('chat_spam_input')
                dpg.hide_item('fakelag_strength') if dpg.get_value('fakelag_checkbox') == False else dpg.show_item('fakelag_strength')
                dpg.hide_item('nightmode_strength') if dpg.get_value('nightmode_checkbox') == False else dpg.show_item('nightmode_strength')
                dpg.hide_item('noflash_strength') if dpg.get_value('noflash_checkbox') == False else dpg.show_item('noflash_strength')
                
                x1 = dpg.get_viewport_width()
                y1 = dpg.get_viewport_height()

                if x1 != x2 or y1 != y2:
                    dpg.set_item_width('menu', x1 - 15)
                    dpg.set_item_height('menu', y1 - 5)
                    x2 = x1
                    y2 = y1

            except Exception as err:
                pass
            time.sleep(0.01)