__author__ = 'MaGicSuR / https://github.com/MaGicSuR'
__version__ = '1.4.6'

from memory import *
from entity import *
from local import *
from gui import *
from helper import *
from convar import *


def entity_loop():
    while True:
        try:
            if ent.in_game():
                ent.entity_loop()
                ent.glow_objects_loop()
        except Exception as err:
            pass
        time.sleep(0.001)

def player_esp():
    while True:
        try:
            if dpg.get_value('player_esp'):
                enemy_team_color = dpg.get_value('enemy_glow_color')
                team_color = dpg.get_value('mates_glow_color')
                c1 = [round(enemy_team_color[0], 1), round(enemy_team_color[1], 1), round(enemy_team_color[2], 1), round(enemy_team_color[3], 1)]
                c2 = [round(team_color[0], 1), round(team_color[1], 1), round(team_color[2], 1), round(team_color[3], 1)]
                
                for entity in ent.glow_objects_list:
                    if entity[2] == 40:
                        if ent.get_dormant(entity[1]) == True:
                                continue
                        if ent.get_team(entity[1]) != ent.get_team(lp.local_player()):
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x8), c1[0] / 100)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0xC), c1[1] / 100)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x10), c1[2] / 100)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x14), c1[3] / 100)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x28), True)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x29), False)
                        elif ent.get_team(lp.local_player()) and dpg.get_value('player_esp_temates'):
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x8), c2[0] / 100)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0xC), c2[1] / 100)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x10), c2[2] / 100)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x14), c2[3] / 100)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x28), True)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x29), False)
        except Exception as err:
            pass
        time.sleep(0.001)

def item_esp():
    while True:
        try:
            if dpg.get_value('item_esp'):
                for entity in ent.glow_objects_list:
                    if class_id_c4(entity[2]) or class_id_gun(entity[2]):
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x8), 0.95)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0xC), 0.12)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x10), 0.54)
                            mem.game_handle.write_float(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x14), 0.6)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x28), True)
                            mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (entity[0] - 1)) + 0x29), False)
                    elif class_id_grenade(entity[2]):
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
            if dpg.get_value('rcs_checkbox') and ent.in_game() and ent.get_health(lp.local_player()) > 0:
                if ctypes.windll.user32.GetAsyncKeyState(key) and ent.get_shots_fired(lp.local_player()) > dpg.get_value('rcs_get_bullets'):
                    if weapon_rifle(ent.active_weapon()) or weapon_smg(ent.active_weapon()) or weapon_heavy(ent.active_weapon()):
                        view_angle = ent.get_view_angle()
                        punch_angle = lp.aim_punch_angle()

                        view_angle.x = view_angle.x + old_angle.x
                        view_angle.y = view_angle.y + old_angle.y
                        # Add the old "viewpunch" so we get the "center" of the screen again

                        current_angle.x = view_angle.x - punch_angle.x * dpg.get_value('rcs_strength')
                        current_angle.y = view_angle.y - punch_angle.y * dpg.get_value('rcs_strength')
                        # remove the new "viewpunch" from the viewangles

                        clamp_angle(current_angle)
                        normalize_vector(current_angle)
                        ent.set_view_angle(Vector3(current_angle.x, current_angle.y, current_angle.z))

                        old_angle.x = punch_angle.x * dpg.get_value('rcs_strength')
                        old_angle.y = punch_angle.y * dpg.get_value('rcs_strength')
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

def auto_pistol():
    while True:
        try:
            if dpg.get_value('autopistol_checkbox') and ent.in_game():
                if ctypes.windll.user32.GetAsyncKeyState(key_handler('autopistol_key')) and weapon_pistol(ent.active_weapon()):
                    lp.force_attack(6)
                    time.sleep(0.02)
        except Exception as err:
            pass
        time.sleep(0.01)

def trigger_bot():
    while True:
        try:
            if dpg.get_value('triggerbot_checkbox') and ent.in_game():
                if ctypes.windll.user32.GetAsyncKeyState(key_handler('triggerbot_key')):

                    crosshair = lp.get_crosshair_id()
                    if crosshair == 0:
                        continue

                    target = lp.get_entity_by_crosshair()
                    if ent.get_team(lp.local_player()) != lp.get_team_by_crosshair(target) and lp.get_health_by_crosshair(target) > 0:
                        if dpg.get_value('humanization_checkbox') == True:

                            v2_delay = round(random.uniform(0.001, 0.01), 3)
                            time.sleep(dpg.get_value('triggerbot_delay') + v2_delay)
                        else:
                            time.sleep(dpg.get_value('triggerbot_delay'))

                        lp.force_attack(6)
        except Exception as err:
            pass
        time.sleep(0.001)

def bunny_hop():
    while True:
        try:
            if dpg.get_value('bunnyhop_checkbox') and lp.get_current_state() == 5:
                while ctypes.windll.user32.GetAsyncKeyState(0x20):
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
            if dpg.get_value('radarhack_checkbox') and ent.in_game():
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
            if dpg.get_value('noflash_checkbox') and ent.in_game():
                if lp.get_flashbang_duration() > 0:
                    lp.set_flashbang_alpha(dpg.get_value('noflash_strength'))
                    temp = dpg.get_value('noflash_strength')
            elif dpg.get_value('noflash_checkbox') == False and temp != 255.0:
                lp.set_flashbang_alpha(255.0)
        except Exception as err:
            pass
        time.sleep(0.1)

def no_smoke():
    while True:
        try:
            if dpg.get_value('nosmoke_checkbox') and ent.in_game():
                for glow_object in ent.glow_objects_list:
                    if glow_object[2] == 157:
                        ent.set_position(glow_object[1], Vector3(0.0, 0.0, 0.0))
        except Exception as err:
            pass
        time.sleep(0.001)

def fov_changer():
    temp = 0
    while True:
        try:
            if ent.in_game():
                if temp != dpg.get_value('fov'):
                    lp.set_fov(dpg.get_value('fov'))
                    temp = dpg.get_value('fov')
        except Exception as err:
            pass
        time.sleep(0.1)

def fake_lag():
    while True:
        try:
            if dpg.get_value('fakelag_checkbox') and ent.in_game():
                lp.send_packets(False)
                time.sleep(dpg.get_value('fakelag_strength'))
                lp.send_packets(True)
        except Exception as err:
            pass
        time.sleep(0.001)

def hit_sound(filename: str):
    oldDmg = 0
    while True:
        try:
            if dpg.get_value('hitsound_checkbox') and ent.in_game():
                damage = ent.get_total_hits(lp.local_player())
                if damage != oldDmg:
                    if 0 < oldDmg >= 255:
                        continue
                    winsound.PlaySound(filename, winsound.SND_ASYNC)
                    oldDmg = damage
        except Exception as err:
            pass
        time.sleep(0.01)

def spectator_list():
    spectators = []
    while True:
        try:
            spectators.clear()
            if ent.in_game():
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
                        dpg.set_value('spectator_list', format)
            else:
                dpg.set_value('spectator_list', '')
        except Exception as err:
            pass
        time.sleep(0.2)

def player_infos(key: int):
    while True:
        try:
            if ctypes.windll.user32.GetAsyncKeyState(key): 
                os.system('cls')
                for entity in ent.entity_list:
                    if entity[2] == 40:
                        if ent.get_name(entity[0]) in [None, 'GOTV']:
                            continue
                        player_info = ''.join(f'Name: {ent.get_name(entity[0])} Wins: {str(ent.get_wins(entity[0]))} Rank: {str(ranks_list[ent.get_rank(entity[0])])}')
                        print(player_info)
        except Exception as err:
            pass
        time.sleep(0.2)

def night_mode():
    temp = 0
    while True:
        try:
            if dpg.get_value('nightmode_checkbox') and ent.in_game():
                if temp != dpg.get_value('nightmode_strength'):
                    for entity in ent.entity_list:
                        if entity[2] == 69:
                            mem.game_handle.write_int(entity[1] + offsets.m_bUseCustomAutoExposureMin, 1)
                            mem.game_handle.write_int(entity[1] + offsets.m_bUseCustomAutoExposureMax, 1)
                            mem.game_handle.write_float(entity[1] + offsets.m_flCustomAutoExposureMin, dpg.get_value('nightmode_strength'))
                            mem.game_handle.write_float(entity[1] + offsets.m_flCustomAutoExposureMax, dpg.get_value('nightmode_strength'))
                            temp = dpg.get_value('nightmode_strength')

        except Exception as err:
            pass
        time.sleep(0.1)

def chat_spam():
    global last_cmd, free_chat_vmem, close_chat_handle
    last_cmd = ''
    while True:
        try:
            if dpg.get_value('chat_spam_checkbox') and ent.in_game():
                current_cmd = f'say {dpg.get_value("chat_spam_input")}'.encode('ascii')
                
                if current_cmd != last_cmd:
                    if last_cmd != '':
                        free_chat_vmem = kernel32.VirtualFreeEx(game_handle.process_handle, vchat_spam_buffer, sys.getsizeof(current_cmd) + 1, win32con.MEM_RELEASE)
                        close_chat_handle = kernel32.CloseHandle(thread_handle)
                    vchat_spam_buffer = kernel32.VirtualAllocEx(game_handle.process_handle, 0, sys.getsizeof(current_cmd) + 1, 0x00001000 | 0x00002000, win32con.PAGE_READWRITE)

                kernel32.WriteProcessMemory(game_handle.process_handle, vchat_spam_buffer, current_cmd, sys.getsizeof(current_cmd), 0)
                chat_spam_thread = win32process.CreateRemoteThread(game_handle.process_handle, None, 0, (engine_dll + offsets.Cmd_ExecuteCommand), vchat_spam_buffer, 0)
                win32event.WaitForSingleObject(chat_spam_thread[0], 0)
                thread_handle = int(str(chat_spam_thread[0]).removesuffix('>').split(':')[1])
                last_cmd = current_cmd

        except Exception as err:
            print(err)
        time.sleep(0.1)

def bomb_events():
    # works just fine, but currently unused.
    # TO:DO : cleanup code
    while True:
        try:
            cur_time = mem.game_handle.read_float(mem.engine_dll + offsets.dwGlobalVars + 0x10)
            has_defuser = mem.game_handle.read_bool(lp.local_player() + 0x117DC)
            # print(t)
            for entity in ent.glow_objects_list:
                bomb_defused = mem.game_handle.read_bool(entity[1] + 0x29c0)
                
                if entity[2] == 129:
                    bomb = mem.game_handle.read_float(entity[1] + 0x29a0)
                    time_to_explode = bomb - cur_time

                    time_to_defuse = bomb - cur_time - (5 if has_defuser == True else 10)
                    # print(time_to_explode, time_to_defuse)
                    if (time_to_explode) <= 0:
                        print('Bomb exploaded!')
                        time.sleep(10)
                    elif (bomb_defused == True):
                        print('Bomb defused!')
                        time.sleep(10)
        except Exception as err:
            pass
        time.sleep(0.001)

def exit():
    try:
        print('Exiting...')
        lp.send_packets(True)
        if last_cmd != '':
            free_chat_vmem
            close_chat_handle
        showfps.set_int(0)
        grenade_preview.set_int(0)
        sky_name.set_string('embassy')
        lp.set_fov(90)
        lp.set_flashbang_alpha(255.0)
        ent.force_update()
        dpg.destroy_context()
        process.close_handle(game_handle.process_handle)
    except exception.MemoryWriteError as err:
        pass
    os._exit(0)

def convar_handler():
    global showfps, grenade_preview, sky_name
    showfps = ConVar('cl_showfps')
    grenade_preview = ConVar('cl_grenadepreview')
    sky_name = ConVar('sv_skyname')
    _temp1, _temp2, _temp3 = 0, 0, ''

    while True:
        try:
            fps_state = int(dpg.get_value('fps_checkbox'))
            gre_state = int(dpg.get_value('grenade_checkbox'))
            sky_state = dpg.get_value('sky_name')

            if fps_state != _temp1:
                if (dpg.get_value('fps_checkbox')):
                        showfps.set_int(fps_state)
                        _temp1 = fps_state
                else:
                    showfps.set_int(fps_state)
                    _temp1 = fps_state

            elif gre_state != _temp2:
                if (dpg.get_value('grenade_checkbox')):
                        grenade_preview.set_int(gre_state)
                        _temp2 = gre_state
                else:
                    grenade_preview.set_int(gre_state)
                    _temp2 = gre_state
            
            elif sky_state != _temp3:
                if (dpg.get_value('sky_name')):
                        sky_name.set_string(sky_state)
                        _temp3 = sky_state
                else:
                    sky_name.set_string(sky_state)
                    _temp3 = sky_state

        except Exception as err:
            pass
        time.sleep(0.01)

def key_handler(key: str):
        v0 = dpg.get_value(key)
        return gui_keys_list.get(v0)

def start_threads():
    try:
        gui.menu()
        dpg.set_item_callback('unload_button', exit)
        threading.Thread(target=entity_loop, name='entity_loop').start()
        threading.Thread(target=player_esp, name='player_esp').start()
        threading.Thread(target=item_esp, name='item_esp').start()
        threading.Thread(target=rcs, args=[0x01], name='rcs').start()
        threading.Thread(target=auto_pistol, name='auto_pistol').start()
        threading.Thread(target=trigger_bot, name='trigger_bot').start()
        threading.Thread(target=bunny_hop, name='bunny_hop').start()
        threading.Thread(target=radar_hack, name='radar_hack').start()
        threading.Thread(target=no_flash, name='no_flash').start()
        threading.Thread(target=no_smoke, name='no_smoke').start()
        threading.Thread(target=fov_changer, name='fov_changer').start()
        threading.Thread(target=fake_lag, name='fake_lag').start()
        threading.Thread(target=hit_sound, args=['hitsound.wav'], name='hit_sound').start()
        # threading.Thread(target=spectator_list, name='spectator_list').start()
        threading.Thread(target=player_infos, args=[0x77], name='player_infos').start()
        threading.Thread(target=night_mode, name='night_mode').start()
        threading.Thread(target=chat_spam, name='cmd').start()
        # threading.Thread(target=bomb_events, name='bomb_events').start()
        threading.Thread(target=convar_handler, name='convar_controller').start()
        threading.Thread(target=gui.make_interactive, name='interactive_gui').start()
    except Exception as err:
        print(f'Threads have been canceled! Exiting...\nReason: {err}\nExiting...')
        os._exit(0)

if __name__ == '__main__':
    try:
        print(f'By: {__author__}\nVersion: {__version__}')
        print('[F8] Players info')
        mem = Memory(game_handle, client_dll, client_dll_size, engine_dll)
        lp = LocalPlayer(mem)
        ent = Entity(mem)
        gui = GUI()
        start_threads()
        dpg.start_dearpygui()
    except (Exception, KeyboardInterrupt) as err:
        ctypes.windll.user32.MessageBoxW(0, f'Failed to initialize!\nExiting...\nReason: {err}', 'Fatal Error', 0)
        os._exit(0)