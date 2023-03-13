import dearpygui.dearpygui as dpg
import helper as h
import webbrowser
import time, ctypes
from config import *

class GUI(Config):
    def __init__(self) -> None:
        self.random_string = h.get_random_string()
        self.config = Config()
    
    def _log(self, sender, app_data, user_data):
        print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")

    def init_menu(self) -> None:
        dpg.create_context()
        self.set_custom_theme()
        dpg.create_viewport(title=self.random_string, decorated=True, width=380, height=450)
        
        self.config.create_default_config('default_config.json')
        with dpg.window(tag='w_main'):
            with dpg.tab_bar():
                with dpg.tab(label='News'):
                    dpg.add_text('Version: 1.6.3')
                    dpg.add_text('Functions marked by (?)\nmay lower your trust factor.\nSafe Mode disables them.', color=(255, 0, 0, 255))
                    dpg.add_checkbox(label='Safe Mode', default_value=True, tag='c_safe_mode')
                    dpg.add_button(label='Github', width=160, height=25, callback=lambda: webbrowser.open('https://github.com/OpsecGuy/BetterGo'))
                with dpg.tab(label='Aim'):
                    dpg.add_checkbox(label='Aimbot (?)', tag='c_aimbot')
                    dpg.add_combo(label='Key', items=tuple(h.gui_keys_list.keys()), default_value='MOUSE 5', width=215, tag='k_aimbot')
                    dpg.add_slider_float(label='Aimbot FOV', default_value=5.0, min_value=1.0, max_value=359.9, clamped=True, width=215, format='%.3f', tag='s_aimbot_fov')
                    dpg.add_slider_float(label='Aimbot Smooth', default_value=3.0, min_value=1.0, max_value=30.0, clamped=True, width=215, format='%.3f', tag='s_aimbot_smooth')
                    dpg.add_combo(label='Bone', items=tuple(h.bone_ids.keys()), default_value='HEAD', width=215, tag='c_aimbot_bone')
                    dpg.add_checkbox(label='Visible Only (?)', tag='c_aimbot_vis')
                    dpg.add_checkbox(label='Attack Team', tag='c_aimbot_team')
                    dpg.add_separator()
                    dpg.add_checkbox(label='Standalone RCS', tag='c_rcs')
                    dpg.add_slider_float(label='RCS Strength', default_value=0.0, min_value=0.0, max_value=2.0, clamped=True, width=215, format='%.3f', tag='s_rcs_str')
                    dpg.add_slider_int(label='Shot After x Bullets', default_value=1, min_value=0, max_value=30, clamped=True, width=215, tag='s_rcs_min_bullets')
                    dpg.add_separator()
                    dpg.add_checkbox(label='TriggerBot', tag='c_tbot')
                    dpg.add_combo(label='Key', items=tuple(h.gui_keys_list.keys()), default_value='MOUSE 4', width=215, tag='k_tbot')
                    dpg.add_checkbox(label='Humanization', tag='c_tbot_legit')
                    dpg.add_slider_float(label='TriggerBot Delay', default_value=0.025, min_value=0.01, max_value=0.2, clamped=True, width=215, format='%.3f', tag='s_tbot_delay')
                with dpg.tab(label='Visuals'):
                    dpg.add_checkbox(label='Player ESP (?)', tag='c_glow_esp')
                    dpg.add_checkbox(label='Team Check', tag='c_glow_esp_team')
                    dpg.add_color_edit(label='Enemy Team Color', default_value=[124, 12, 51, 160], tag='e_glow_esp_enemy')
                    dpg.add_color_edit(label='Team color', default_value=[42, 196, 15, 160], tag='e_glow_esp_team')
                    dpg.add_checkbox(label='Health Based', tag='c_glow_esp_health')
                    dpg.add_checkbox(label='Item ESP (?)', tag='c_glow_esp_items')
                    dpg.add_separator()
                    dpg.add_checkbox(label='Night Mode', tag='c_night')
                    dpg.add_slider_float(label='Night Mode Strength', default_value=1.0, min_value=0.01, max_value=3.0, clamped=True, width=215, format='%.3f', tag='s_night_str')
                    dpg.add_checkbox(label='No Flash (?)', tag='c_noflash')
                    dpg.add_slider_float(label='No Flash Strength', default_value=255.0, min_value=0.0, max_value=255.0, clamped=True, width=215, format='%.3f', tag='s_noflash_str')
                    dpg.add_slider_int(label='FOV', default_value=90, min_value=60, max_value=160, clamped=True, width=215, tag='s_fov')
                    dpg.add_combo(label='Sky', items=list(h.sky_list), default_value='', width=215, tag='d_sky')
                with dpg.tab(label='Overlay'):
                    dpg.add_checkbox(label='Box ESP + HP Text', tag='c_box_esp')
                    dpg.add_checkbox(label='Snaplines', tag='c_snaplines')
                    dpg.add_checkbox(label='Distance', tag='c_distance')
                    dpg.add_checkbox(label='Head Indicator', tag='c_head_indicator')
                    dpg.add_checkbox(label='Bomb Indicator', tag='c_bomb_indicator')
                    dpg.add_checkbox(label='Grenade Trajectory', tag='c_gre_line')
                    dpg.add_checkbox(label='Sniper Crosshair', tag='c_sniper_crosshair')
                    dpg.add_checkbox(label='Recoil Crosshair', tag='c_recoil_crosshair')
                    dpg.add_combo(label='Crosshair Style', items=['Crosshair', 'Circle'], default_value='Crosshair', width=215, tag='c_recoil_crosshair_mode')
                with dpg.tab(label='Misc'):
                    dpg.add_checkbox(label='Auto Pistol', tag='c_autopistol', default_value=True)
                    dpg.add_combo(label='Key', items=tuple(h.gui_keys_list.keys()), default_value='LEFT MOUSE', width=215, tag='k_autopistol')
                    dpg.add_checkbox(label='Radar Hack (?)', tag='c_radar')
                    dpg.add_checkbox(label='Hit Sound', tag='c_hitsound')
                    dpg.add_checkbox(label='BunnyHop', tag='c_bh')
                    dpg.add_checkbox(label='Auto Strafer', tag='c_strafer')
                    dpg.add_checkbox(label='Auto Zeus', tag='c_zeus')
                    dpg.add_checkbox(label='Knife Bot', tag='c_knifebot')
                    dpg.add_checkbox(label='Spectator Alert', tag='c_spec_alert')
                    dpg.add_checkbox(label='No Smoke', tag='c_nosmoke')
                    dpg.add_checkbox(label='Show FPS', tag='c_fps')
                    dpg.add_checkbox(label='Chat Spam (?)', tag='c_chat')
                    dpg.add_input_text(label='Command', width=215, tag='i_chat')
                    dpg.add_checkbox(label='Fake Lag', tag='c_fakelag')
                    dpg.add_slider_float(label='Fake Lag Strength', default_value=0.001, min_value=0.001, max_value=0.016, clamped=True, width=215, tag='s_fakelag_str')
                    dpg.add_button(label='Players Info', width=160, height=25, tag='b_pinfo', callback=lambda: dpg.show_item('w_players_dump'))
                with dpg.tab(label='Config'):
                    dpg.add_input_text(label='Config name', default_value='default_config', width=140, tag='i_config_name')
                    dpg.add_button(label='Create', width=160, height=25, callback=lambda: self.create_config(), tag='b_create_config')
                    dpg.add_combo(label='Select Config', items=tuple(self.config.get_config_list()), width=215, tag='c_config_list')
                    with dpg.group(horizontal=True):
                        dpg.add_button(label='Save', width=160, height=25, callback=lambda: self.save_config(), tag='b_save_config')
                        dpg.add_button(label='Load', width=160, height=25, callback=lambda: self.load_config(), tag='b_load_config')
                    dpg.add_button(label='Unload Cheat', width=160, height=25, tag='b_unload')

        with dpg.window(label='Player info', tag='w_players_dump', show=False, autosize=True):
            with dpg.group(horizontal=True):
                dpg.add_text('', tag='buffer_name')
                dpg.add_text('', tag='buffer_wins')
                dpg.add_text('', tag='buffer_rank')

        with dpg.tooltip(parent='c_safe_mode'):
            dpg.add_text('Disables features that can cause red trust factor.')

        dpg.bind_theme('base_theme')
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("w_main", True)

    def make_interactive(self) -> None:
        while True:
            try:
                dpg.hide_item('k_aimbot') if dpg.get_value('c_aimbot') == False else dpg.show_item('k_aimbot')
                dpg.hide_item('s_aimbot_fov') if dpg.get_value('c_aimbot') == False else dpg.show_item('s_aimbot_fov')
                dpg.hide_item('s_aimbot_smooth') if dpg.get_value('c_aimbot') == False else dpg.show_item('s_aimbot_smooth')
                dpg.hide_item('c_aimbot_bone') if dpg.get_value('c_aimbot') == False else dpg.show_item('c_aimbot_bone')
                dpg.hide_item('c_aimbot_vis') if dpg.get_value('c_aimbot') == False else dpg.show_item('c_aimbot_vis')
                dpg.hide_item('c_aimbot_team') if dpg.get_value('c_aimbot') == False else dpg.show_item('c_aimbot_team')
                dpg.hide_item('s_rcs_str') if dpg.get_value('c_rcs') == False else dpg.show_item('s_rcs_str')
                dpg.hide_item('s_rcs_min_bullets') if dpg.get_value('c_rcs') == False else dpg.show_item('s_rcs_min_bullets')
                dpg.hide_item('c_tbot_legit') if dpg.get_value('c_tbot') == False else dpg.show_item('c_tbot_legit')
                dpg.hide_item('k_tbot') if dpg.get_value('c_tbot') == False else dpg.show_item('k_tbot')
                dpg.hide_item('s_tbot_delay') if dpg.get_value('c_tbot') == False else dpg.show_item('s_tbot_delay')
                dpg.hide_item('c_glow_esp_team') if dpg.get_value('c_glow_esp') == False else dpg.show_item('c_glow_esp_team')
                dpg.hide_item('e_glow_esp_enemy') if dpg.get_value('c_glow_esp') == False else dpg.show_item('e_glow_esp_enemy')
                dpg.hide_item('e_glow_esp_team') if dpg.get_value('c_glow_esp') == False else dpg.show_item('e_glow_esp_team')
                dpg.hide_item('c_recoil_crosshair_mode') if dpg.get_value('c_recoil_crosshair') == False else dpg.show_item('c_recoil_crosshair_mode')
                dpg.hide_item('c_glow_esp_health') if dpg.get_value('c_glow_esp') == False else dpg.show_item('c_glow_esp_health')
                dpg.hide_item('s_noflash_str') if dpg.get_value('c_noflash') == False else dpg.show_item('s_noflash_str')
                dpg.hide_item('k_autopistol') if dpg.get_value('c_autopistol') == False else dpg.show_item('k_autopistol')
                dpg.hide_item('c_strafer') if dpg.get_value('c_bh') == False else dpg.show_item('c_strafer')
                dpg.hide_item('i_chat') if dpg.get_value('c_chat') == False else dpg.show_item('i_chat')
                dpg.hide_item('s_fakelag_str') if dpg.get_value('c_fakelag') == False else dpg.show_item('s_fakelag_str')
                dpg.hide_item('s_night_str') if dpg.get_value('c_night') == False else dpg.show_item('s_night_str')
                
                if dpg.get_value('c_safe_mode'):
                    dpg.disable_item('c_aimbot')
                    dpg.set_value('c_aimbot', False)
                    dpg.disable_item('c_aimbot_vis')
                    dpg.set_value('c_aimbot_vis', False)
                    dpg.disable_item('c_glow_esp')
                    dpg.set_value('c_glow_esp', False)
                    dpg.disable_item('c_glow_esp_items')
                    dpg.set_value('c_glow_esp_items', False)
                    dpg.disable_item('c_radar')
                    dpg.set_value('c_radar', False)
                    dpg.disable_item('c_chat')
                    dpg.set_value('c_chat', False)
                else:
                    dpg.enable_item('c_aimbot')
                    dpg.enable_item('c_aimbot_vis')
                    dpg.enable_item('c_glow_esp')
                    dpg.enable_item('c_glow_esp_items')
                    dpg.enable_item('c_radar')
                    dpg.enable_item('c_chat')
                
                dpg.configure_item('c_config_list', items=tuple(self.config.get_config_list()))
            except Exception as err:
                pass
            time.sleep(0.1)

    def set_custom_theme(self) -> None:
        dpg.add_theme(tag='base_theme')
        with dpg.theme_component(parent='base_theme'):
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 9)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 9)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 9)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 9)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 7)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 13)
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,(0, 170, 50, 130))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive,(0, 170, 50, 130))
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (0, 255, 0))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,(0, 170, 50, 130))

    def create_config(self) -> None:
        if dpg.get_value('i_config_name') != '':
            config_file = f"{dpg.get_value('i_config_name')}"
            path_to_config = f'{self.config.get_cfg_dir}\\'+ f'{config_file}'
            try:
                if os.path.exists(f'{path_to_config}.json'):
                    ctypes.windll.user32.MessageBoxW(0, 'Config file with the same name already exist!', 'Config Error', 0)
                else:
                    with open(f'{path_to_config}.json', 'w+') as file:
                        file.write(json.dumps(config_example))
            except Exception as err:
                pass

    def save_config(self) -> None:
        if dpg.get_value('c_config_list') != '':
            config_file = f"{dpg.get_value('c_config_list')}.json"
            path_to_config = (f'{self.config.get_cfg_dir}\\'+ f'{config_file}')
            with open(f'{path_to_config}', 'r+') as f:
                content = json.load(f)
                # save new values
                content['aimbot']['switch'] = dpg.get_value('c_aimbot')
                content['aimbot']['key'] = dpg.get_value('k_aimbot')
                content['aimbot']['fov'] = dpg.get_value('s_aimbot_fov')
                content['aimbot']['smooth'] = dpg.get_value('s_aimbot_smooth')
                content['aimbot']['bone'] = dpg.get_value('c_aimbot_bone')
                content['aimbot']['visible_only'] = dpg.get_value('c_aimbot_vis')
                content['aimbot']['attack_team'] = dpg.get_value('c_aimbot_team')

                content['standalone_rcs']['switch'] = dpg.get_value('c_rcs')
                content['standalone_rcs']['strength'] = dpg.get_value('s_rcs_str')
                content['standalone_rcs']['min_bullets'] = dpg.get_value('s_rcs_min_bullets')

                content['triggerbot']['switch'] = dpg.get_value('c_tbot')
                content['triggerbot']['key'] = dpg.get_value('k_tbot')
                content['triggerbot']['humanization'] = dpg.get_value('c_tbot_legit')
                content['triggerbot']['delay'] = dpg.get_value('s_tbot_delay')

                content['visuals']['player_esp'] = dpg.get_value('c_glow_esp')
                content['visuals']['glow_team'] = dpg.get_value('c_glow_esp_team')
                content['visuals']['health_mode'] = dpg.get_value('c_glow_esp_health')
                content['visuals']['item_esp'] = dpg.get_value('c_glow_esp_items')
                content['visuals']['night_mode'] = dpg.get_value('c_night')
                content['visuals']['night_mode_strength'] = dpg.get_value('s_night_str')
                content['visuals']['noflash'] = dpg.get_value('c_noflash')
                content['visuals']['noflash_strength'] = dpg.get_value('s_noflash_str')
                content['visuals']['player_fov'] = dpg.get_value('s_fov')

                content['overlay']['box_esp'] = dpg.get_value('c_box_esp')
                content['overlay']['snap_lines'] = dpg.get_value('c_snaplines')
                content['overlay']['distance'] = dpg.get_value('c_distance')
                content['overlay']['head_indicator'] = dpg.get_value('c_head_indicator')
                content['overlay']['bomb_indicator'] = dpg.get_value('c_bomb_indicator')
                content['overlay']['grenade_traces'] = dpg.get_value('c_gre_line')
                content['overlay']['sniper_crosshair'] = dpg.get_value('c_sniper_crosshair')
                content['overlay']['recoil_crosshair'] = dpg.get_value('c_recoil_crosshair')
                content['overlay']['crosshair_style'] = dpg.get_value('c_recoil_crosshair_mode')

                content['misc']['auto_pistol'] = dpg.get_value('c_autopistol')
                content['misc']['auto_pistol_key'] = dpg.get_value('k_autopistol')
                content['misc']['radar_hack'] = dpg.get_value('c_radar')
                content['misc']['hit_sound'] = dpg.get_value('c_hitsound')
                content['misc']['bunny_hop'] = dpg.get_value('c_bh')
                content['misc']['auto_strafe'] = dpg.get_value('c_strafer')
                content['misc']['auto_zeus'] = dpg.get_value('c_zeus')
                content['misc']['knife_bot'] = dpg.get_value('c_knifebot')
                content['misc']['no_smoke'] = dpg.get_value('c_nosmoke')
                content['misc']['spec_alert'] = dpg.get_value('c_spec_alert')
                content['misc']['show_fps'] = dpg.get_value('c_fps')
                content['misc']['fake_lag'] = dpg.get_value('c_fakelag')
                content['misc']['lag_strength'] = dpg.get_value('s_fakelag_str')
                
                content['other']['safe_mode'] = dpg.get_value('c_safe_mode')
                
                with open(f'{path_to_config}', 'w') as f:
                    json.dump(content, f)

    # TO:DO Clean up
    def load_config(self) -> None:
        config = f"{dpg.get_value('c_config_list')}.json"
        path_to_config = (f'{self.config.get_cfg_dir}\\'+ f'{config}')
        config_name = dpg.get_value('c_config_list')
        # print(path_to_config)
        if dpg.get_value('c_config_list') == '.json':
            ctypes.windll.user32.MessageBoxW(0, 'Could not load given config!', 'Config Error', 0)
        else:
            dpg.set_value('c_aimbot', self.config.read_value(config_name, 'aimbot','switch'))
            dpg.set_value('k_aimbot', self.config.read_value(config_name, 'aimbot','key'))
            dpg.set_value('s_aimbot_fov', self.config.read_value(config_name, 'aimbot','fov'))
            dpg.set_value('s_aimbot_smooth', self.config.read_value(config_name, 'aimbot','smooth'))
            dpg.set_value('c_aimbot_bone', self.config.read_value(config_name, 'aimbot','bone'))
            dpg.set_value('c_aimbot_vis', self.config.read_value(config_name, 'aimbot','visible_only'))
            dpg.set_value('c_aimbot_team', self.config.read_value(config_name, 'aimbot','attack_team'))

            dpg.set_value('c_rcs', self.config.read_value(config_name, 'standalone_rcs','switch'))
            if self.config.read_value(config_name, 'standalone_rcs','strength') <= dpg.get_item_configuration('s_rcs_str')['max_value']: dpg.set_value('s_rcs_str', self.config.read_value(config_name, 'standalone_rcs','strength'))
            if self.config.read_value(config_name, 'standalone_rcs','min_bullets') <= dpg.get_item_configuration('s_rcs_min_bullets')['max_value']: dpg.set_value('s_rcs_min_bullets', self.config.read_value(config_name, 'standalone_rcs','min_bullets'))

            dpg.set_value('c_tbot', self.config.read_value(config_name, 'triggerbot','switch'))
            dpg.set_value('k_tbot', self.config.read_value(config_name, 'triggerbot','key'))
            dpg.set_value('c_tbot_legit', self.config.read_value(config_name, 'triggerbot','humanization'))
            dpg.set_value('s_tbot_delay', self.config.read_value(config_name, 'triggerbot','delay')) if self.config.read_value(config_name, 'triggerbot','delay') <= dpg.get_item_configuration('s_tbot_delay')['max_value'] else None

            dpg.set_value('c_glow_esp', self.config.read_value(config_name, 'visuals','player_esp'))
            dpg.set_value('c_glow_esp_team', self.config.read_value(config_name, 'visuals','glow_team'))
            dpg.set_value('c_glow_esp_health', self.config.read_value(config_name, 'visuals','health_mode'))
            dpg.set_value('c_glow_esp_items', self.config.read_value(config_name, 'visuals','item_esp'))
            dpg.set_value('c_night', self.config.read_value(config_name, 'visuals','night_mode'))
            if self.config.read_value(config_name, 'visuals','night_mode_strength') <= dpg.get_item_configuration('s_night_str')['max_value']: dpg.set_value('s_night_str', self.config.read_value(config_name, 'visuals','night_mode_strength'))
            dpg.set_value('c_noflash', self.config.read_value(config_name, 'visuals','noflash'))
            if self.config.read_value(config_name, 'visuals','noflash_strength') <= dpg.get_item_configuration('s_noflash_str')['max_value']: dpg.set_value('s_noflash_str', self.config.read_value(config_name, 'visuals','noflash_strength'))
            dpg.set_value('s_fov', self.config.read_value(config_name, 'visuals','player_fov')) if self.config.read_value(config_name, 'visuals','player_fov') <= dpg.get_item_configuration('s_fov')['max_value'] else None
            if self.config.read_value(config_name, 'visuals','player_fov') <= dpg.get_item_configuration('s_fov')['max_value']: dpg.set_value('s_fov', self.config.read_value(config_name, 'visuals','player_fov'))

            dpg.set_value('c_box_esp', self.config.read_value(config_name, 'overlay','box_esp'))
            dpg.set_value('c_snaplines', self.config.read_value(config_name, 'overlay','snap_lines'))
            dpg.set_value('c_distance', self.config.read_value(config_name, 'overlay', 'distance'))
            dpg.set_value('c_head_indicator', self.config.read_value(config_name, 'overlay','head_indicator'))
            dpg.set_value('c_bomb_indicator', self.config.read_value(config_name, 'overlay','bomb_indicator'))
            dpg.set_value('c_gre_line', self.config.read_value(config_name, 'overlay','grenade_traces'))
            dpg.set_value('c_sniper_crosshair', self.config.read_value(config_name, 'overlay','sniper_crosshair'))
            dpg.set_value('c_recoil_crosshair', self.config.read_value(config_name, 'overlay','recoil_crosshair'))
            dpg.set_value('c_recoil_crosshair_mode', self.config.read_value(config_name, 'overlay','crosshair_style'))

            dpg.set_value('c_autopistol', self.config.read_value(config_name, 'misc','auto_pistol'))
            dpg.set_value('k_autopistol', self.config.read_value(config_name, 'misc','auto_pistol_key'))
            dpg.set_value('c_radar', self.config.read_value(config_name, 'misc','radar_hack'))
            dpg.set_value('c_hitsound', self.config.read_value(config_name, 'misc','hit_sound'))
            dpg.set_value('c_bh', self.config.read_value(config_name, 'misc','bunny_hop'))
            dpg.set_value('c_strafer', self.config.read_value(config_name, 'misc','auto_strafe'))
            dpg.set_value('c_zeus', self.config.read_value(config_name, 'misc','auto_zeus'))
            dpg.set_value('c_knifebot', self.config.read_value(config_name, 'misc','knife_bot'))
            dpg.set_value('c_spec_alert', self.config.read_value(config_name, 'misc', 'spec_alert'))
            dpg.set_value('c_nosmoke', self.config.read_value(config_name, 'misc','no_smoke'))
            dpg.set_value('c_fps', self.config.read_value(config_name, 'misc','show_fps'))
            dpg.set_value('c_fakelag', self.config.read_value(config_name, 'misc','fake_lag'))
            if self.config.read_value(config_name, 'misc','lag_strength') <= dpg.get_item_configuration('s_fakelag_str')['max_value']: dpg.set_value('s_fakelag_str',self.config.read_value(config_name, 'misc','lag_strength'))
            
            dpg.set_value('c_safe_mode', self.config.read_value(config_name, 'other','safe_mode'))

    def key_handler(self, key: str) -> int:
        return h.gui_keys_list.get(dpg.get_value(key))