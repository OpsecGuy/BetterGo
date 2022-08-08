import dearpygui.dearpygui as dpg
import helper as h
from config import Config
import random, time, webbrowser

class GUI():
    def __init__(self) -> None:
        self.v1 = self.get_random_string()
        
    def get_random_string(self) -> None:
        chars = ['A',
        'B', 'C', 'D', 'E', 'F','G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'U', 'P', 'R', 'S', 'T', 'W', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f','g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'u', 'p', 'r', 's', 't', 'w', 'y', 'z',
        '1','2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '^', '&', '&', '(', ')', '-', '_', '=', '+']
        return ''.join(random.choice(chars) for _ in range(0, 15))
    
    def _log(self, sender, app_data, user_data):
        print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")

    def menu(self):
        dpg.create_context()
        dpg.create_viewport(title=self.v1, decorated=True, width=Config.read('window','x'), height=Config.read('window','y'))
        
        with dpg.window(tag='main'):
            with dpg.collapsing_header(label="Aimbot", tag='aimbot_header'):
                dpg.add_checkbox(label='Aimbot', tag='c_aimbot')
                dpg.add_combo(label='Key', items=tuple(h.gui_keys_list.keys()), default_value='MOUSE 5', width=215, tag='k_aimbot')
                dpg.add_slider_float(label='Aimbot FOV', default_value=5.0, min_value=0.1, max_value=359.9, width=215, tag='s_aimbot_fov')
                dpg.add_slider_float(label='Aimbot Smooth', default_value=3.0, min_value=0.0, max_value=30.0, width=215, tag='s_aimbot_smooth')
                dpg.add_checkbox(label='Visible Only', tag='c_aimbot_vis')
                dpg.add_checkbox(label='Attack Team', tag='c_aimbot_team')
                dpg.add_checkbox(label='No Recoil', tag='c_aimbot_rcs')
                dpg.add_separator()
                dpg.add_checkbox(label='Standalone RCS', tag='c_rcs')
                dpg.add_slider_float(label='RCS Strength', default_value=0.0, min_value=0.0, max_value=2.0, width=215, tag='s_rcs_str')
                dpg.add_slider_int(label='Shot After x Bullets', default_value=0, min_value=0, max_value=30, width=215, tag='s_rcs_min_bullets')
                dpg.add_separator()
                dpg.add_checkbox(label='TriggerBot', tag='c_tbot')
                dpg.add_combo(label='Key', items=tuple(h.gui_keys_list.keys()), default_value='MOUSE 4', width=215, tag='k_tbot')
                dpg.add_checkbox(label='Humanization', tag='c_tbot_legit')
                dpg.add_slider_float(label='TriggerBot Delay', default_value=0.025, min_value=0.01, max_value=0.2, width=215, tag='s_tbot_delay')
            with dpg.collapsing_header(label='Visuals', tag='visuals_header'):
                dpg.add_checkbox(label='Player ESP', tag='c_esp')
                dpg.add_checkbox(label='Team Check', tag='c_esp_team')
                dpg.add_color_edit(label='Enemy Team Color', default_value=[124, 12, 51, 160], tag='e_esp_enemy')
                dpg.add_color_edit(label='Team color', default_value=[42, 196, 15, 160], tag='e_esp_team')
                dpg.add_checkbox(label='Health Based', tag='c_esp_health')
                dpg.add_checkbox(label='Item ESP', tag='c_esp_items')
                dpg.add_separator()
                dpg.add_checkbox(label='Grenade Trajectory', tag='c_gre_line')
                dpg.add_checkbox(label='Night Mode', tag='c_night')
                dpg.add_slider_float(label='Night Mode Strength', default_value=0.3, min_value=0.01, max_value=3.0, width=215, tag='s_night_str')
                dpg.add_checkbox(label='No Flash', tag='c_noflash')
                dpg.add_slider_float(label='No Flash Strength', default_value=255.0, min_value=0.0, max_value=255.0, width=215, tag='s_noflash_str')
                dpg.add_slider_int(label='FOV', default_value=90, min_value=60, max_value=160, width=215, tag='s_foc')
                dpg.add_combo(label='Sky', items=list(h.sky_list), default_value='', width=215, tag='d_sky')
            with dpg.collapsing_header(label='Misc', tag='misc_header'):
                dpg.add_checkbox(label='Auto Pistol', tag='c_autopistol')
                dpg.add_combo(label='Key', items=tuple(h.gui_keys_list.keys()), default_value='LEFT MOUSE', width=215, tag='k_autopistol')
                dpg.add_checkbox(label='Radar Hack', tag='c_radar')
                dpg.add_checkbox(label='Hit Sound', tag='c_hitsound')
                dpg.add_checkbox(label='BunnyHop', tag='c_bh')
                dpg.add_checkbox(label='Auto Strafer', tag='c_strafer')
                dpg.add_checkbox(label='Auto Zeus', tag='c_zeus')
                dpg.add_checkbox(label='Knife Bot', tag='c_knifebot')
                dpg.add_checkbox(label='No Smoke', tag='c_nosmoke')
                dpg.add_checkbox(label='Show FPS', tag='c_fps')
                dpg.add_checkbox(label='Chat Spam', tag='c_chat')
                dpg.add_input_text(label='Command', width=215, tag='i_chat')
                dpg.add_checkbox(label='Fake Lag', tag='c_fakelag')
                dpg.add_slider_float(label='Fake Lag Strength', default_value=0.001, min_value=0.001, max_value=0.016, width=215, tag='s_fakelag_str')
                dpg.add_button(label='Players Info (Console)', width=160, height=25, tag='b_pinfo')
            
            dpg.add_separator()
            dpg.add_button(label='Unload', width=160, height=25, tag='unload_button')
            dpg.add_button(label='Github', width=160, height=25, callback=lambda: webbrowser.open('https://github.com/OpsecGuy/BetterGo'))
            dpg.add_button(label='Load Config', width=160, height=25, callback=lambda: self.override())
            dpg.add_text('Version: 1.4.7.7')
        
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("main", True)
        
        
    def make_interactive(self):
        while True:
            try:
                dpg.hide_item('k_aimbot') if dpg.get_value('c_aimbot') == False else dpg.show_item('k_aimbot')
                dpg.hide_item('s_aimbot_fov') if dpg.get_value('c_aimbot') == False else dpg.show_item('s_aimbot_fov')
                dpg.hide_item('s_aimbot_smooth') if dpg.get_value('c_aimbot') == False else dpg.show_item('s_aimbot_smooth')
                dpg.hide_item('c_aimbot_vis') if dpg.get_value('c_aimbot') == False else dpg.show_item('c_aimbot_vis')
                dpg.hide_item('c_aimbot_team') if dpg.get_value('c_aimbot') == False else dpg.show_item('c_aimbot_team')
                dpg.hide_item('c_aimbot_rcs') if dpg.get_value('c_aimbot') == False else dpg.show_item('c_aimbot_rcs')
                dpg.hide_item('s_rcs_str') if dpg.get_value('c_rcs') == False else dpg.show_item('s_rcs_str')
                dpg.hide_item('s_rcs_min_bullets') if dpg.get_value('c_rcs') == False else dpg.show_item('s_rcs_min_bullets')
                dpg.hide_item('c_tbot_legit') if dpg.get_value('c_tbot') == False else dpg.show_item('c_tbot_legit')
                dpg.hide_item('k_tbot') if dpg.get_value('c_tbot') == False else dpg.show_item('k_tbot')
                dpg.hide_item('s_tbot_delay') if dpg.get_value('c_tbot') == False else dpg.show_item('s_tbot_delay')
                dpg.hide_item('c_esp_team') if dpg.get_value('c_esp') == False else dpg.show_item('c_esp_team')
                dpg.hide_item('e_esp_enemy') if dpg.get_value('c_esp') == False else dpg.show_item('e_esp_enemy')
                dpg.hide_item('e_esp_team') if dpg.get_value('c_esp') == False else dpg.show_item('e_esp_team')
                dpg.hide_item('c_esp_health') if dpg.get_value('c_esp') == False else dpg.show_item('c_esp_health')
                dpg.hide_item('s_noflash_str') if dpg.get_value('c_noflash') == False else dpg.show_item('s_noflash_str')
                dpg.hide_item('k_autopistol') if dpg.get_value('c_autopistol') == False else dpg.show_item('k_autopistol')
                dpg.hide_item('c_strafer') if dpg.get_value('c_bh') == False else dpg.show_item('c_strafer')
                dpg.hide_item('i_chat') if dpg.get_value('c_chat') == False else dpg.show_item('i_chat')
                dpg.hide_item('s_fakelag_str') if dpg.get_value('c_fakelag') == False else dpg.show_item('s_fakelag_str')
                dpg.hide_item('s_night_str') if dpg.get_value('c_night') == False else dpg.show_item('s_night_str')

            except Exception as err:
                pass
            time.sleep(0.01)
            
    def override(self):
        dpg.set_value('c_aimbot', Config.read('aimbot','switch'))
        dpg.set_value('k_aimbot', Config.read('aimbot','key'))
        if Config.read('aimbot','fov') <= dpg.get_item_configuration('s_aimbot_fov')['max_value']: dpg.set_value('s_aimbot_fov', Config.read('aimbot','fov'))
        if Config.read('aimbot','smooth') <= dpg.get_item_configuration('s_aimbot_smooth')['max_value']: dpg.set_value('s_aimbot_smooth', Config.read('aimbot','smooth'))
        dpg.set_value('c_aimbot_vis', Config.read('aimbot','visible_only'))
        dpg.set_value('c_aimbot_team', Config.read('aimbot','attack_team'))
        dpg.set_value('c_aimbot_rcs', Config.read('aimbot','no_recoil'))
        dpg.set_value('c_rcs', Config.read('standalone_rcs','switch'))
        if Config.read('standalone_rcs','strength') <= dpg.get_item_configuration('s_rcs_str')['max_value']: dpg.set_value('s_rcs_str', Config.read('standalone_rcs','strength'))
        if Config.read('standalone_rcs', 'min_bullets') <= dpg.get_item_configuration('s_rcs_min_bullets')['max_value']: dpg.set_value('s_rcs_min_bullets', Config.read('standalone_rcs', 'min_bullets'))
        dpg.set_value('c_tbot', Config.read('triggerbot','switch'))
        dpg.set_value('c_tbot_legit', Config.read('triggerbot','humanization'))
        dpg.set_value('k_tbot', Config.read('triggerbot','key'))
        dpg.set_value('s_tbot_delay', Config.read('triggerbot','delay')) if Config.read('triggerbot','delay') <= dpg.get_item_configuration('s_tbot_delay')['max_value'] else None
        dpg.set_value('c_esp', Config.read('visuals','player_esp'))
        dpg.set_value('c_esp_team', Config.read('visuals','glow_team'))
        dpg.set_value('c_esp_health', Config.read('visuals','health_mode'))
        dpg.set_value('c_esp_items', Config.read('visuals','item_esp'))
        dpg.set_value('c_gre_line', Config.read('visuals','grenade_traces'))
        dpg.set_value('c_night', Config.read('visuals','night_mode'))
        dpg.set_value('c_noflash', Config.read('visuals','noflash'))
        if Config.read('visuals','noflash_strength') <= dpg.get_item_configuration('s_noflash_str')['max_value']: dpg.set_value('s_noflash_str', Config.read('visuals','noflash_strength'))
        dpg.set_value('s_foc', Config.read('visuals','player_fov')) if Config.read('visuals','player_fov') <= dpg.get_item_configuration('s_foc')['max_value'] else None
        if Config.read('visuals','player_fov') <= dpg.get_item_configuration('s_foc')['max_value']: dpg.set_value('s_foc', Config.read('visuals','player_fov'))
        dpg.set_value('c_autopistol', Config.read('misc','auto_pistol'))
        dpg.set_value('c_radar', Config.read('misc','radar_hack'))
        dpg.set_value('c_hitsound', Config.read('misc','hit_sound'))
        dpg.set_value('c_bh', Config.read('misc','bunny_hop'))
        dpg.set_value('c_strafer', Config.read('misc','auto_strafe'))
        dpg.set_value('c_zeus', Config.read('misc','auto_zeus'))
        dpg.set_value('c_knifebot', Config.read('misc','knife_bot'))
        dpg.set_value('c_nosmoke', Config.read('misc','no_smoke'))
        dpg.set_value('c_fps', Config.read('misc','show_fps'))
        dpg.set_value('c_chat', Config.read('misc','chat_spam'))
        dpg.set_value('c_fakelag', Config.read('misc','fake_lag'))
        if Config.read('misc','lag_strength') <= dpg.get_item_configuration('s_fakelag_str')['max_value']: dpg.set_value('s_fakelag_str',Config.read('misc','lag_strength'))