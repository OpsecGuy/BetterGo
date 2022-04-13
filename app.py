__author__ = 'MaGicSuR / https://github.com/MaGicSuR'
__name__ = 'BetterGo'
__version__ = '1.4.2'

from time import sleep
from memory import *
from entity import *
from local import *
from gui import *
import helper as h

def entity_loop():
    while True:
        try:
            if ent.in_game():
                ent.entity_loop()
                ent.glow_objects_loop()
        except Exception as err:
            pass
        sleep(0.001)

def player_esp():
    while True:
        try:
            if player_esp_switch:
                for entity in ent.glow_objects_list:
                    if entity[2] == 40:
                        if ent.get_dormant(entity[1]) == True:
                                continue
                        if ent.get_team(entity[1]) != ent.get_team(lp.local_player()):
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x8), 0.47)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0xC), 0.24)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x10), 1.0)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x14), 0.6)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x28), True)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x29), False)
        except Exception as err:
            pass
        time.sleep(0.001)

def item_esp():
    while True:
        try:
            if item_esp_switch:
                for entity in ent.glow_objects_list:
                    if h.class_id_c4(entity[2]) or h.class_id_gun(entity[2]):
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x8), 0.95)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0xC), 0.12)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x10), 0.54)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x14), 0.6)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x28), True)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x29), False)
                    elif h.class_id_grenade(entity[2]):
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x8), 1.0)
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0xC), 1.0)
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x10), 1.0)
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x14), 0.6)
                        mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x28), True)
                        mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x29), False)
        except Exception as err:
            pass
        time.sleep(0.001)

def rcs(key: int):
    current_angle = Vector3(0, 0, 0)
    view_angle = Vector3(0, 0, 0)
    old_angle = Vector3(0, 0, 0)
    while (True):
        try:
            if rcs_switch and ent.in_game() and ent.get_health(lp.local_player()) > 0:
                if ctypes.windll.user32.GetAsyncKeyState(key) and ent.get_shots_fired(lp.local_player()) > int(rcs_shots_fired):
                    if h.weapon_rifle(ent.active_weapon()) or h.weapon_smg(ent.active_weapon()) or h.weapon_heavy(ent.active_weapon()):
                        view_angle = ent.get_view_angle()
                        punch_angle = lp.aim_punch_angle()

                        view_angle.x = view_angle.x + old_angle.x
                        view_angle.y = view_angle.y + old_angle.y
                        # Add the old "viewpunch" so we get the "center" of the screen again

                        current_angle.x = view_angle.x - punch_angle.x * rcs_smooth
                        current_angle.y = view_angle.y - punch_angle.y * rcs_smooth
                        # remove the new "viewpunch" from the viewangles

                        h.clamp_angle(current_angle)
                        h.normalize_vector(current_angle)
                        ent.set_view_angle(current_angle.x, current_angle.y, 0.0)

                        old_angle.x = punch_angle.x * rcs_smooth
                        old_angle.y = punch_angle.y * rcs_smooth
                        # save the old "viewpunch"
                    else:
                        old_angle.x = 0
                        old_angle.y = 0
                else:
                    old_angle.x = 0
                    old_angle.y = 0
        except Exception as err:
            pass
        time.sleep(0.001)

def auto_pistol(key: int, delay: float):
    while True:
        try:
            if auto_pistol_switch and ent.in_game():
                if ctypes.windll.user32.GetAsyncKeyState(key) and h.weapon_pistol(ent.active_weapon()):
                    lp.force_attack(6)
                    time.sleep(delay)
        except Exception as err:
            pass
        time.sleep(0.01)

def trigger_bot(key: int):
    while True:
        try:
            if trigger_bot_switch and ent.in_game():
                if ctypes.windll.user32.GetAsyncKeyState(key):

                    crosshair = lp.get_crosshair_id()
                    if crosshair == 0:
                        continue

                    target = lp.get_entity_by_crosshair()
                    if ent.get_team(lp.local_player()) != lp.get_team_by_crosshair(target) and lp.get_health_by_crosshair(target) > 0:
                        if trigger_bot_humanization == True:

                            v2_delay = round(random.uniform(0.001, 0.01), 3)
                            time.sleep(triggerbot_delay + v2_delay)
                        else:
                            time.sleep(triggerbot_delay)

                        ent.force_attack(6)
        except Exception as err:
            pass
        time.sleep(0.001)

def bunny_hop(key: int):
    while True:
        try:
            if bunny_hop_switch and lp.get_current_state() == 5:
                while ctypes.windll.user32.GetAsyncKeyState(key):
                    if ent.get_flag(lp.local_player()) == 257:
                        lp.force_jump(5)
                        time.sleep(0.01)
                    else:
                        lp.force_jump(4)
                        time.sleep(0.01)
        except Exception as err:
            pass
        time.sleep(0.001)

def radar_hack():
    while True:
        try:
            if radar_hack_switch and ent.in_game():
                for entity in ent.entity_list:
                    if entity[2] == 40:
                        ent.set_is_visible(entity[1], True)
        except Exception as err:
            pass
        time.sleep(0.1)

def no_flash():
    temp = 0
    while True:
        try:
            if no_flash_switch and ent.in_game():
                if lp.get_flashbang_duration() > 0:
                    lp.set_flashbang_alpha(no_flash_value)
                    temp = no_flash_value
            elif no_flash_switch == False and temp != 255.0:
                lp.set_flashbang_alpha(255.0)
        except Exception as err:
            pass
        time.sleep(0.1)

def no_smoke():
    while True:
        try:
            if no_smoke_switch and ent.in_game():
                for glow_object in ent.glow_objects_list:
                    if glow_object[2] == 157:
                        ent.set_position(glow_object[1], 0.0, 0.0)
        except Exception as err:
            pass
        time.sleep(0.01)

def fov_changer():
    temp = 0
    while True:
        try:
            if ent.in_game():
                if temp != fov_value:
                    lp.set_fov(int(fov_value))
                    temp = fov_value
        except Exception as err:
            pass
        time.sleep(0.1)

def hit_sound(filename: str):
    oldDmg = 0
    while True:
        try:
            if hit_sound_switch and ent.in_game():
                damage = ent.get_total_hits(lp.local_player())
                if damage != oldDmg:
                    if 0 < oldDmg >= 255:
                        continue
                    oldDmg = damage
                    winsound.PlaySound(filename, winsound.SND_ASYNC)
        except Exception as err:
            pass
        time.sleep(0.01)

def spectator_list():
    spectators = []
    while True:
        spectators.clear()
        if ent.in_game():
            try:
                if ent.get_health(lp.local_player()) <= 0:
                    spectators.clear()

                for entity in ent.entity_list:
                    if entity[2] == 40:
                        player_name = ent.get_name(entity[0])
                        if player_name == None or player_name == 'GOTV':
                            continue

                        if ent.get_team(entity[1]) == ent.get_team(lp.local_player()):
                            observed_target_handle = mem.game_handle.read_uint(entity[1] + offsets.m_hObserverTarget) & 0xFFF
                            spectated = mem.game_handle.read_uint(mem.client_dll + offsets.dwEntityList + (observed_target_handle - 1) * 0x10)
                            
                            if spectated == lp.local_player():
                                spectators.append(ent.get_name(entity[0]))
            
                if len(spectators) > 0:
                    format = '\n'.join(spectators)
                    return format
                else:
                    return ''
            except Exception as err:
                pass
        time.sleep(1)

def player_infos(key: int):
    while True:
        try:
            if ctypes.windll.user32.GetAsyncKeyState(key): 
                os.system('cls')
                for entity in ent.entity_list:
                    if entity[2] == 40:
                        if ent.get_name(entity[0]) == None:
                            continue
                        player_info = ''.join(f'Name: {ent.get_name(entity[0])} Wins: {str(ent.get_wins(entity[0]))} Rank: {str(h._RANKS_[ent.get_rank(entity[0])])}')
                        print(player_info)
        except Exception as err:
            pass
        time.sleep(0.2)

def night_mode():
    temp = 0
    while True:
        try:
            if nightmode_switch and ent.in_game():
                if temp != nightmode_strength:
                    for entity in ent.entity_list:
                        if entity[2] == 69:
                            mem.game_handle.write_int(entity[1] + offsets.m_bUseCustomAutoExposureMin, 1)
                            mem.game_handle.write_int(entity[1] + offsets.m_bUseCustomAutoExposureMax, 1)
                            mem.game_handle.write_float(entity[1] + offsets.m_flCustomAutoExposureMin, nightmode_strength)
                            mem.game_handle.write_float(entity[1] + offsets.m_flCustomAutoExposureMax, nightmode_strength)
                            temp = nightmode_strength

        except Exception as err:
            pass
        time.sleep(0.1)

def exit():
    try:
        print('Exiting...')
        mem.game_handle.write_int(ent.engine_ptr() + 0x174, -1)
        lp.set_fov(90)
        lp.set_flashbang_alpha(255.0)
    except exception.MemoryWriteError as err:
        print(err)
    os._exit(0)

def draw_gui():
    # Static
    global player_esp_switch, item_esp_switch, rcs_switch, auto_pistol_switch, trigger_bot_switch, trigger_bot_humanization, bunny_hop_switch, radar_hack_switch
    global no_flash_switch, no_smoke_switch, hit_sound_switch, nightmode_switch
    # Dynamic
    global fov_value, triggerbot_delay, rcs_shots_fired, rcs_smooth, nightmode_strength, no_flash_value

    player_esp_switch, item_esp_switch, rcs_switch, auto_pistol_switch, trigger_bot_switch, trigger_bot_humanization, bunny_hop_switch, radar_hack_switch = False, False, False, False, False, False, False, False
    no_flash_switch, no_smoke_switch, hit_sound_switch, nightmode_switch = False, False, False, False
    fov_value, triggerbot_delay, rcs_shots_fired, rcs_smooth, nightmode_strength, no_flash_value = 90, 25.0, 2, 1.6, 1.0, 80.0
    # GUI
    spec_list = window.create_spectator_list()
    main_gui = window.create_main_gui()
    # pinfo = window.create_playerinfo_table()
    
    while True:
        spec_list_event, spec_list_values = spec_list.read(timeout=100)
        main_gui_event, main_gui_values = main_gui.read(timeout=100)
        # pinfo_event, pinfo_values = pinfo.read(timeout=100)
        
        if main_gui_event in (gui.WIN_CLOSED, 'Exit') or ctypes.windll.user32.GetAsyncKeyState(0x2E): # check for exit at first place to avoid issues
            exit()

        ### Player info table ###
        # pinfo['playerinfo'].update(test())
        ### Spectator list ###
        spec_list['spec_list'].update(spectator_list())
        ### Cheat gui ###
        if main_gui_values["player_esp_checkbox"] == True:
            player_esp_switch = True
        else:
            player_esp_switch = False
        if main_gui_values["item_esp_checkbox"] == True:
            item_esp_switch = True
        else:
            item_esp_switch = False
        if main_gui_values["rcs_checkbox"] == True:
            rcs_switch = True
        else:
            rcs_switch = False
        if main_gui_values["auto_pistol_checkbox"] == True:
            auto_pistol_switch = True
        else:
            auto_pistol_switch = False
        if main_gui_values["trigger_bot_checkbox"] == True:
            trigger_bot_switch = True
        else:
            trigger_bot_switch = False
        if main_gui_values["trigger_bot_humanization_checkbox"] == True:
            trigger_bot_humanization = True
        else:
            trigger_bot_humanization = False
        if main_gui_values["bunny_hop_checkbox"] == True:
            bunny_hop_switch = True
        else:
            bunny_hop_switch = False
        if main_gui_values["radar_hack_checkbox"] == True:
            radar_hack_switch = True
        else:
            radar_hack_switch = False
        if main_gui_values["no_smoke_checkbox"] == True:
            no_smoke_switch = True
        else:
            no_smoke_switch = False
        if main_gui_values["no_flash_checkbox"] == True:
            no_flash_switch = True
        else:
            no_flash_switch = False
        if main_gui_values["hit_sound_checkbox"] == True:
            hit_sound_switch = True
        else:
            hit_sound_switch = False
        if main_gui_values["nightmode_checkbox"] == True:
            nightmode_switch = True
        else:
            nightmode_switch = False

        rcs_shots_fired = main_gui_values['rcs_shots_fired']
        
        fov_value = main_gui_values['fov_value']
        main_gui['print_fov_value'].update(fov_value)

        triggerbot_delay = main_gui_values['triggerbot_delay_value']
        main_gui['print_triggerbot_delay'].update(triggerbot_delay)

        rcs_smooth = main_gui_values['rcs_smooth_value']
        main_gui['print_smooth_value'].update(rcs_smooth)

        nightmode_strength = main_gui_values['nightmode_strength']
        main_gui['print_nightmode_value'].update(nightmode_strength)

        no_flash_value = main_gui_values['no_flash_strength']
        main_gui['print_no_flash_value'].update(no_flash_value)

def start_threads():
    try:
        threading.Thread(target=entity_loop, name='entity_loop').start()
        threading.Thread(target=player_esp, name='player_esp').start()
        threading.Thread(target=item_esp, name='item_esp').start()
        threading.Thread(target=rcs, args=[0x01], name='rcs').start()
        threading.Thread(target=auto_pistol, args=[0x05, 0.02], name='auto_pistol').start()
        threading.Thread(target=trigger_bot, args=[0x06], name='trigger_bot').start(),
        threading.Thread(target=bunny_hop, args=[0x20], name='bunny_hop').start()
        threading.Thread(target=radar_hack, name='radar_hack').start()
        threading.Thread(target=no_flash, name='no_flash').start()
        threading.Thread(target=no_smoke, name='no_smoke').start()
        threading.Thread(target=fov_changer, name='fov_changer').start()
        threading.Thread(target=hit_sound, args=['hitsound.wav'], name='hit_sound').start()
        threading.Thread(target=player_infos, args=[0x77], name='player_infos').start()
        threading.Thread(target=night_mode, name='night_mode').start()
        threading.Thread(target=draw_gui, name='gui').start()
    except Exception as err:
        print(f'Threads have been canceled! Exiting...\nReason: {err}\nExiting...')
        os._exit(0)

if __name__ == 'BetterGo':
    try:
        start_timer = time.perf_counter()
        mem = Memory(game_handle, client_dll, client_dll_size, engine_dll)
        lp = LocalPlayer(mem)
        ent = Entity(mem)
        window = GUI()
        start_threads()
        stop_timer = time.perf_counter()
        print(f'Name: {__name__}\nBy: {__author__}\nVersion: {__version__}\n')
        print(f'Initialization took {round((stop_timer - start_timer), 5)} seconds.')
        print('[MOUSE4] Auto Pistol\n[MOUSE5] TriggerBot\n[SPACE] BunnyHop\n[F8] Players info')
    except (Exception, KeyboardInterrupt) as err:
        print(f'Failed to initialize!\nReason: {err}\nExiting...')
        os._exit(0)