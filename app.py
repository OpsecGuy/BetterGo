__author__ = 'OpsecGuy'

from memory import *
from entity import *
from local import *
from gui import *
from convar import *
from overlay import *
import threading
import winsound

DEBUG_MODE = False

def entity_loop():
    while True:
        try:
            if ent.in_game():
                ent.entity_loop()
                ent.glow_objects_loop()
        except Exception as err:
            if DEBUG_MODE == True:
                print(entity_loop.__name__, err)
            pass
        time.sleep(0.001)

def glow_esp():
    while True:
        try:
            if ent.in_game():
                enemy_team_color = dpg.get_value('e_glow_esp_enemy')
                team_color = dpg.get_value('e_glow_esp_team')
                c1 = [enemy_team_color[0], enemy_team_color[1], enemy_team_color[2], enemy_team_color[3]]
                c2 = [team_color[0], team_color[1], team_color[2], team_color[3]]
                local_player_team = ent.get_team(lp.local_player())

                for entity in ent.glow_objects_list:
                    if lp.local_player() == entity[1] or ent.get_dormant(entity[1]) == True:
                        continue
                    
                    if dpg.get_value('c_glow_esp'):
                        if entity[2] == 40:

                            health = ent.get_health(entity[1])
                            if health <= 0:
                                continue

                            if ent.get_team(entity[1]) != local_player_team:
                                # + 0x8 because we skip reading first 2 int(s) which leaded to crashes
                                # 3 last fields in orginal struct we ignore and update only what we need
                                glow_target_address = ent.glow_object() + (0x38 * (entity[0] - 1))
                                glow_struct_bytes = game_handle.read_bytes(glow_target_address + 0x8, 0x23) # 0x23, because we don't fill whole struct
                                var = list(struct.unpack("4f1?3c3f3c", glow_struct_bytes))
                                var[0] = round(c1[0] / 255, 2) if not dpg.get_value('c_glow_esp_health') else 1.0 - (health / 100.0)
                                var[1] = round(c1[1] / 255, 2) if not dpg.get_value('c_glow_esp_health') else health / 100.0
                                var[2] = round(c1[2] / 255, 2) if not dpg.get_value('c_glow_esp_health') else 0.0
                                var[3] = round(c1[3] / 255, 2)
                                var[11] = b'\x01'
                                var[12] = b'\x00'
                                # pack glow object struct with our changes
                                value = struct.pack("4f1?3c3f3c", *var)
                                # Write new glow struct to game memory
                                game_handle.write_bytes(glow_target_address + 0x8, value, 0x23)

                            elif dpg.get_value('c_glow_esp_team'):
                                glow_target_address = ent.glow_object() + (0x38 * (entity[0] - 1))                   
                                glow_struct_bytes = game_handle.read_bytes(glow_target_address + 0x8, 0x23)
                                var = list(struct.unpack("4f1?3c3f3c", glow_struct_bytes))
                                var[0] = round(c2[0] / 255, 2) if not dpg.get_value('c_esp_health') else 1.0 - (health / 100.0)
                                var[1] = round(c2[1] / 255, 2) if not dpg.get_value('c_esp_health') else health / 100.0
                                var[2] = round(c2[2] / 255, 2) if not dpg.get_value('c_esp_health') else 0.0
                                var[3] = round(c2[3] / 255, 2)
                                var[11] = b'\x01'
                                var[12] = b'\x00'
                                value = struct.pack("4f1?3c3f3c", *var)
                                game_handle.write_bytes(glow_target_address + 0x8, value, 0x23)

                    if dpg.get_value('c_glow_esp_items'):
                        if class_id_c4(entity[2]) or class_id_gun(entity[2]):
                            glow_target_address = ent.glow_object() + (0x38 * (entity[0] - 1))                   
                            glow_struct_bytes = game_handle.read_bytes(glow_target_address + 0x8, 0x23)
                            var = list(struct.unpack("4f1?3c3f3c", glow_struct_bytes))
                            var[0] = 0.92
                            var[1] = 0.79
                            var[2] = 0.16
                            var[3] = 0.7
                            var[11] = b'\x01'
                            var[12] = b'\x00'
                            value = struct.pack("4f1?3c3f3c", *var)
                            game_handle.write_bytes(glow_target_address + 0x8, value, 0x23)

                        if class_id_grenade(entity[2]):                            
                            glow_target_address = ent.glow_object() + (0x38 * (entity[0] - 1))                    
                            glow_struct_bytes = game_handle.read_bytes(glow_target_address + 0x8, 0x23)
                            var = list(struct.unpack("4f1?3c3f3c", glow_struct_bytes))
                            var[0] = 1.0
                            var[1] = 0.0
                            var[2] = 0.0
                            var[3] = 0.8
                            var[11] = b'\x01'
                            var[12] = b'\x00'
                            value = struct.pack("4f1?3c3f3c", *var)
                            game_handle.write_bytes(glow_target_address + 0x8, value, 0x23)
                    
        except Exception as err:
            if DEBUG_MODE == True:
                print(glow_esp.__name__, err)
            pass
        time.sleep(0.001)

def aimbot():
    # TO:DO Lock aim on player
    fov = 0
    while True:
        try:
            if ctypes.windll.user32.GetAsyncKeyState(gui.key_handler('k_aimbot')) and dpg.get_value('c_aimbot') and ent.in_game() and ent.get_health(lp.local_player()) > 0:
                best_angle = Vector3(0.0, 0.0, 0.0)
                best_fov = dpg.get_value('s_aimbot_fov')
                local_origin = ent.get_position(lp.local_player())
                view_angle = ent.get_view_angle()
                aim_punch = lp.aim_punch_angle()
                local_eye_pos = lp.get_eye_position(local_origin)
                for entity in ent.entity_list:
                    if entity[2] == 40:
                        if entity[1] == lp.local_player():
                            continue
                        if dpg.get_value('c_aimbot_vis'):
                            if ent.is_spotted_by_mask(entity[1]) == False:
                                continue
                        if not dpg.get_value('c_aimbot_team'):
                            if ent.get_team(entity[1]) == ent.get_team(lp.local_player()):
                                continue
                        if ent.get_dormant(entity[1]) or ent.is_protected(entity[1]) == True:
                            continue
                        if ent.get_health(entity[1]) <= 0:
                            continue

                        bone_matrix = ent.get_bone_position(entity[1], bone_ids.get(dpg.get_value('c_aimbot_bone')))
                        current_view_angle = \
                        Vector3(view_angle.x + aim_punch.x * 2.0,
                                view_angle.y + aim_punch.y * 2.0,
                                view_angle.z + aim_punch.z * 2.0)
                        angle = calculate_angle(local_eye_pos, bone_matrix, current_view_angle)
                        fov = hypot(angle.x, angle.y)

                        fixed_angle = clamp_angle(normalize_angle(angle))
                        if fov < best_fov:
                            best_fov = fov
                            best_angle = fixed_angle

                if best_angle.x < fov and best_angle.y < fov and best_angle.x != 0.0 and best_angle.y != 0.0:
                    ent.set_view_angle(Vector3(view_angle.x + best_angle.x / dpg.get_value('s_aimbot_smooth'),
                                        view_angle.y + best_angle.y / dpg.get_value('s_aimbot_smooth'),
                                        view_angle.z + best_angle.z / dpg.get_value('s_aimbot_smooth')
                                        ))

        except Exception as err:
            if DEBUG_MODE == True:
                print(aimbot.__name__, err)
            pass
        time.sleep(0.001)

def rcs():
    current_angle = Vector3(0, 0, 0)
    old_angle = Vector3(0, 0, 0)
    while (True):
        try:
            if dpg.get_value('c_rcs') and ent.in_game() and ent.get_health(lp.local_player()) > 0:
                if ctypes.windll.user32.GetAsyncKeyState(0x01) and ent.get_shots_fired() > dpg.get_value('s_rcs_min_bullets'):
                    if weapon_rifle(lp.active_weapon()) or weapon_smg(lp.active_weapon()) or weapon_heavy(lp.active_weapon()):
                        view_angle = ent.get_view_angle()
                        punch_angle = lp.aim_punch_angle()

                        current_angle.x = (view_angle.x + old_angle.x) - punch_angle.x * dpg.get_value('s_rcs_str')
                        current_angle.y = (view_angle.y + old_angle.y) - punch_angle.y * dpg.get_value('s_rcs_str')

                        clamped_angle = clamp_angle(current_angle)
                        ent.set_view_angle(current_angle)

                        old_angle.x = punch_angle.x * dpg.get_value('s_rcs_str')
                        old_angle.y = punch_angle.y * dpg.get_value('s_rcs_str')
                    else:
                        old_angle.x = old_angle.y = 0.0
                else:
                    old_angle.x = old_angle.y = 0.0

        except Exception as err:
            if DEBUG_MODE == True:
                print(rcs.__name__, err)
            pass
        time.sleep(0.001)

def auto_pistol():
    while True:
        try:
            if dpg.get_value('c_autopistol') and ent.in_game() and ov.window_focused() and ent.get_health(lp.local_player()) > 0:
                if ctypes.windll.user32.GetAsyncKeyState(gui.key_handler('k_autopistol')) and weapon_pistol(lp.active_weapon()):    
                    lp.force_attack(6)
                    time.sleep(0.02)
        except Exception as err:
            if DEBUG_MODE == True:
                print(auto_pistol.__name__, err)
            pass
        time.sleep(0.01)

def trigger_bot():
    while True:
        try:
            if ov.window_focused() and ent.in_game() and ent.get_health(lp.local_player()) > 0:
                crosshair = lp.get_crosshair_id()
                entity = lp.get_entity_by_crosshair()
                if crosshair == 0 or entity == 0:
                    continue
                    
                local_position = ent.get_position(lp.local_player())
                distance = helper.distance(local_position, ent.get_position(entity))
                entity_hp_crosshair = lp.get_health_by_crosshair(entity)
                entity_team_crosshair = lp.get_team_by_crosshair(entity)
                local_team = ent.get_team(lp.local_player())
                if ctypes.windll.user32.GetAsyncKeyState(gui.key_handler('k_tbot')) and dpg.get_value('c_tbot'):
                    if entity_team_crosshair != local_team and entity_hp_crosshair > 0:
                        if dpg.get_value('c_tbot_legit') == True:
                            v2_delay = round(random.uniform(0.001, 0.01), 3)
                            time.sleep(dpg.get_value('s_tbot_delay') + v2_delay)
                        else:
                            time.sleep(dpg.get_value('s_tbot_delay'))
                        lp.force_attack(6)
                
                if dpg.get_value('c_zeus'):
                    if lp.active_weapon() == 31 and entity_team_crosshair != local_team:
                        if entity_hp_crosshair > 0:
                            if distance <= 150:
                                lp.force_attack(6)

                if dpg.get_value('c_knifebot'):
                    if weapon_knife(lp.active_weapon()) and entity_team_crosshair != local_team:
                        if distance <= 82:
                            if entity_hp_crosshair <= 55 and distance <= 70:
                                lp.force_attack2(6)
                            else:
                                lp.force_attack(6)

        except Exception as err:
            if DEBUG_MODE == True:
                print(trigger_bot.__name__, err)
            pass
        time.sleep(0.01)

def bunny_hop():
    while True:
        try:
            if dpg.get_value('c_bh') and lp.get_current_state() == 5:
                while ctypes.windll.user32.GetAsyncKeyState(0x20):
                    if ent.get_flag(lp.local_player()) & (1 << 0) and lp.get_move_type() != 9:
                        lp.force_jump(5)
                    else:
                        lp.force_jump(4)
        except Exception as err:
            if DEBUG_MODE == True:
                print(bunny_hop.__name__, err)
            pass
        time.sleep(0.001)

def auto_strafer():
    old_view_angle = Vector3(0.0, 0.0, 0.0)
    while True:
        try:
            if dpg.get_value('c_bh') and dpg.get_value('c_strafer'):
                if ctypes.windll.user32.GetAsyncKeyState(0x20) and ent.get_flag(lp.local_player()) != 257 and lp.get_move_type() != 9: # 9 - player on ladder
                    current_angle = ent.get_view_angle()
                    if current_angle.y > old_view_angle.y:
                        lp.force_left(6)
                    elif current_angle.y < old_view_angle.y:
                        lp.force_right(6)
                    old_view_angle = current_angle
        except Exception as err:
            if DEBUG_MODE == True:
                print(auto_strafer.__name__, err)
            pass
        time.sleep(0.001)

def radar_hack():
    while True:
        try:
            if dpg.get_value('c_radar') and ent.in_game():
                for entity in ent.entity_list:
                    if entity[2] == 40:
                        ent.set_spotted(entity[1], True)
        except Exception as err:
            if DEBUG_MODE == True:
                print(radar_hack.__name__, err)
            pass
        time.sleep(0.1)

def no_flash():
    temp = 255.0
    while True:
        try:
            if dpg.get_value('c_noflash') and ent.in_game():
                if lp.get_flashbang_duration() > 0:
                    lp.set_flashbang_alpha(dpg.get_value('s_noflash_str'))
                    temp = dpg.get_value('s_noflash_str')
            elif dpg.get_value('c_noflash') == False and temp != 255.0:
                lp.set_flashbang_alpha(255.0)
        except Exception as err:
            if DEBUG_MODE == True:
                print(no_flash.__name__, err)
            pass
        time.sleep(0.1)

def no_smoke():
    while True:
        try:
            if dpg.get_value('c_nosmoke') and ent.in_game():
                for glow_object in ent.glow_objects_list:
                    if glow_object[2] == 157:
                        ent.set_position(glow_object[1], Vector3(0.0, 0.0, 0.0))
        except Exception as err:
            if DEBUG_MODE == True:
                print(no_smoke.__name__, err)
            pass
        time.sleep(0.001)

def fov_changer():
    temp = 0
    while True:
        try:
            if ent.in_game():
                if temp != dpg.get_value('s_fov'):
                    lp.set_fov(dpg.get_value('s_fov'))
                    temp = dpg.get_value('s_fov')
        except Exception as err:
            if DEBUG_MODE == True:
                print(fov_changer.__name__, err)
            pass
        time.sleep(0.1)

def fake_lag():
    while True:
        try:
            if dpg.get_value('c_fakelag') and ent.in_game():
                lp.send_packets(False)
                time.sleep(dpg.get_value('s_fakelag_str'))
                lp.send_packets(True)
        except Exception as err:
            if DEBUG_MODE == True:
                print(fake_lag.__name__, err)
            pass
        time.sleep(0.001)

def hit_sound(file_name: str):
    shots_count = 0
    while True:
        try:
            if dpg.get_value('c_hitsound') and ent.in_game():
                shots_fired = lp.get_total_hits()
                if shots_fired != shots_count:
                    if shots_count <= 255: # 255 - limit of shots_fired per round
                        winsound.PlaySound(file_name, winsound.SND_ASYNC)
                    shots_count = shots_fired
        except Exception as err:
            if DEBUG_MODE == True:
                print(hit_sound.__name__, err)
            pass
        time.sleep(0.01)

def spectator_list():
    spectators = []
    try:
        spectators.clear()
        if ent.in_game():
            local_player = lp.local_player()
            if ent.get_health(local_player) <= 0:
                spectators.clear()

            for entity in ent.entity_list:
                if entity[2] == 40:
                    player_name = str(ent.get_name(entity[0])).removeprefix("b'").split('\\')[0].strip()[:10]

                    if player_name == None or player_name == 'GOTV':
                        continue

                    if ent.get_team(entity[1]) == ent.get_team(local_player):
                        observed_target_handle = game_handle.read_uint(entity[1] + offsets.m_hObserverTarget) & 0xFFF
                        spectated = game_handle.read_uint(mem.client_dll + offsets.dwEntityList + (observed_target_handle - 1) * 0x10)
                        
                        if spectated == local_player:
                            spectators.append(player_name)
            
            if len(spectators) > 0:
                return 'You are spectated'
            else:
                return ''

    except Exception as err:
        if DEBUG_MODE == True:
            print(spectator_list.__name__, err)
        pass

def player_infos():
    while True:
        try:
            if dpg.is_item_clicked('b_pinfo') and ent.in_game():
                for entity in ent.entity_list:
                    if entity[2] == 40:
                        if ent.get_name(entity[0]) not in [None, 'GOTV']:
                            name = str(ent.get_name(entity[0])).removeprefix("b'").split('\\')[0].strip()[:10]

                            if name not in helper.player_info_buffer:
                                player_info_buffer.append([name, str(ent.get_wins(entity[0])), str(ranks_list[ent.get_rank(entity[0])])])

                # TO:DO Recode needed
                dpg.set_value('buffer_name','\n'.join([i[0] for i in helper.player_info_buffer]))
                dpg.set_value('buffer_wins','\n'.join([i[1] for i in helper.player_info_buffer]))
                dpg.set_value('buffer_rank','\n'.join([i[2] for i in helper.player_info_buffer]))
                helper.player_info_buffer.clear()
        except Exception as err:
            if DEBUG_MODE == True:
                print(player_infos.__name__, err)
            pass
        time.sleep(0.001)

def night_mode():
    temp = 0
    while True:
        try:
            if dpg.get_value('c_night') and ent.in_game():
                if temp != dpg.get_value('s_night_str'):
                    for entity in ent.entity_list:
                        if entity[2] == 69:
                            game_handle.write_int(entity[1] + offsets.m_bUseCustomAutoExposureMin, 1)
                            game_handle.write_int(entity[1] + offsets.m_bUseCustomAutoExposureMax, 1)
                            game_handle.write_float(entity[1] + offsets.m_flCustomAutoExposureMin, dpg.get_value('s_night_str'))
                            game_handle.write_float(entity[1] + offsets.m_flCustomAutoExposureMax, dpg.get_value('s_night_str'))
                            temp = dpg.get_value('s_night_str')

        except Exception as err:
            if DEBUG_MODE == True:
                print(night_mode.__name__, err)
            pass
        time.sleep(0.01)

def chat_spam():
    global last_cmd_chat, free_chat_vmem, close_chat_handle
    last_cmd_chat = ''
    mem_free = False
    while True:
        try:
            if dpg.get_value('c_chat') and ent.in_game():
                current_cmd = f'say {dpg.get_value("i_chat")}'.encode('ascii')
                if ent.get_team(lp.local_player()) not in [2, 3]:
                    continue

                if last_cmd_chat == 'say '.encode('ascii') and mem_free == False:
                    free_chat_vmem = kernel32.VirtualFreeEx(game_handle.process_handle, vchat_spam_buffer, sys.getsizeof(current_cmd) + 1, win32con.MEM_RELEASE)
                    close_chat_handle = kernel32.CloseHandle(thread_handle)
                    mem_free = True
                else:
                    mem_free = False
                    if current_cmd != last_cmd_chat and dpg.get_value('c_chat') != '':
                        vchat_spam_buffer = kernel32.VirtualAllocEx(game_handle.process_handle, 0, sys.getsizeof(current_cmd) + 1, 0x00001000 | 0x00002000, win32con.PAGE_READWRITE)
                    if mem_free == False:
                        kernel32.WriteProcessMemory(game_handle.process_handle, vchat_spam_buffer, current_cmd, sys.getsizeof(current_cmd), 0)
                        chat_spam_thread = win32process.CreateRemoteThread(game_handle.process_handle, None, 0, (engine_dll + offsets.Cmd_ExecuteCommand), vchat_spam_buffer, 0)
                        win32event.WaitForSingleObject(chat_spam_thread[0], 0)
                        thread_handle = int(str(chat_spam_thread[0]).removesuffix('>').split(':')[1])

                last_cmd_chat = current_cmd

        except Exception as err:
            if DEBUG_MODE == True:
                print(chat_spam.__name__, err)
            pass
        time.sleep(1)

def exit():
    try:
        print('Exiting...')
        lp.send_packets(True)
        if last_cmd_chat != '':
            free_chat_vmem
            close_chat_handle
        showfps.set_int(0)
        grenade_preview.set_int(0)
        sky_name.set_string('embassy')
        lp.set_fov(90)
        lp.set_flashbang_alpha(255.0)
        ent.force_update()
        ov.close()
        os._exit(0)
    except exception.MemoryWriteError as err:
        if DEBUG_MODE == True:
            print(exit.__name__, err)
        pass
    os._exit(0)

def convar_handler():
    global showfps, grenade_preview, sky_name
    showfps = ConVar('cl_showfps')
    grenade_preview = ConVar('cl_grenadepreview')
    sky_name = ConVar('sv_skyname')
    temp_showfps, temp_grenade_preview, temp_sky_name = 0, 0, ''

    while True:
        try:
            fps_state = int(dpg.get_value('c_fps'))
            gre_state = int(dpg.get_value('c_gre_line'))
            sky_state = dpg.get_value('d_sky')
            if fps_state != temp_showfps:
                if (dpg.get_value('c_fps')):
                        showfps.set_int(fps_state)
                        temp_showfps = fps_state
                else:
                    showfps.set_int(fps_state)
                    temp_showfps = fps_state

            if gre_state != temp_grenade_preview:
                if (dpg.get_value('c_gre_line')):
                        grenade_preview.set_int(gre_state)
                        temp_grenade_preview = gre_state
                else:
                    grenade_preview.set_int(gre_state)
                    temp_grenade_preview = gre_state
            
            if sky_state != temp_sky_name:
                if (dpg.get_value('d_sky')):
                        sky_name.set_string(sky_state)
                        temp_sky_name = sky_state
                else:
                    sky_name.set_string(sky_state)
                    temp_sky_name = sky_state
        except Exception as err:
            if DEBUG_MODE == True:
                print(convar_handler.__name__, err)
            pass
        time.sleep(0.01)

def opengl_overlay():
    global ov
    ov = Overlay()
    ov_rect = GetWindowRect(ov.handle)
    center_x = (ov_rect[2] + 1) / 2
    center_y = (ov_rect[3] + 1) / 2

    while True:
        try:
            ov.draw_text(f'github.com/OpsecGuy', 420, 20)
            if ent.in_game():
                if dpg.get_value('c_spec_alert'):
                    ov.draw_text(f'{spectator_list()}', center_x - 75, center_y + 200)

                local_player = lp.local_player()
                view_matrix = ent.view_matrix()
                
                for entity in ent.entity_list:
                    if entity[2] == 40:
                        if entity[1] == local_player or ent.get_team(local_player) == ent.get_team(entity[1]):
                            continue
                        if ent.get_dormant(entity[1]) == True or ent.get_health(entity[1]) <= 0:
                            continue

                        entity_position = ent.get_position(entity[1])
                        w2s_position = ov.w2s(entity_position, view_matrix)
                        bone_head = ov.w2s(ent.get_bone_position(entity[1], 8), view_matrix)

                        if w2s_position is None or bone_head is None:
                            continue

                        if dpg.get_value('c_snaplines'):
                            ov.draw_line(center_x, 0, w2s_position[0], w2s_position[1], 1, (0.0, 1.0, 0.0))

                        if dpg.get_value('c_box_esp'):
                            head = bone_head[1] - w2s_position[1]
                            width = head / 2
                            center = width / -2
                            ov.draw_full_box(w2s_position[0] + center, w2s_position[1], width, head + 5, 2, (0.0, 1.0, 0.0))
                            
                        if dpg.get_value('c_hp_text'):
                            ov.draw_text(f'{ent.get_health(entity[1])}', w2s_position[0], w2s_position[1] - 15)

                        if dpg.get_value('c_distance'):
                            dist = distance(ent.get_position(local_player), entity_position)
                            ov.draw_text(f'{str(dist / 32):.4}m', w2s_position[0], w2s_position[1] - 30)

                        if dpg.get_value('c_head_indicator'):
                            ov.draw_empty_circle(bone_head[0], bone_head[1], 4.0, 10, (0.0, 1.0, 0.0))

                    # bomb indicator
                    if class_id_c4(entity[2]) and dpg.get_value('c_bomb_indicator'):
                        c4_pos = ent.get_position(entity[1])
                        w2s_c4_pos = ov.w2s(c4_pos, view_matrix)
                        if w2s_c4_pos is None or c4_pos.x == 0.0:
                            continue
                        ov.draw_empty_circle(w2s_c4_pos[0], w2s_c4_pos[1], 10.0, 10, (1.0, 1.0, 0.0))

                if dpg.get_value('c_sniper_crosshair'):
                    if weapon_sniper(lp.active_weapon()) and not ent.is_scoping(local_player):
                        ov.draw_crosshair(center_x, center_y, 1, (1.0, 0.0, 0.0))

                if dpg.get_value('c_recoil_crosshair'):
                    punch_angle = lp.aim_punch_angle()
                    if punch_angle.x != 0.0 and lp.get_shots_fired() > 1:
                        fov = lp.get_fov()
                        dx = (ov_rect[2] + 1) / fov
                        dy = (ov_rect[3] + 1) / fov
                        crosshair_x = center_x - dx * punch_angle.y
                        crosshair_y = center_y - dy * punch_angle.x

                        if dpg.get_value('c_recoil_crosshair_mode') == 'Crosshair':
                            ov.draw_crosshair(crosshair_x, crosshair_y, 1, (1.0, 0.0, 0.0))
                        elif dpg.get_value('c_recoil_crosshair_mode') == 'Circle':
                            ov.draw_empty_circle(crosshair_x, crosshair_y, 5.0, 10, (1.0, 1.0, 0.0))

        except Exception as err:
            if DEBUG_MODE == True:
                print(opengl_overlay.__name__, err)
            pass
        ov.refresh()
        time.sleep(0.001)

def main():
    try:
        gui.init_menu()
        dpg.set_item_callback('b_unload', exit)
        threading.Thread(target=opengl_overlay, name='opengl_overlay', daemon=True).start()
        time.sleep(0.5) # Increase in case of issues with overlay to 1.0
        # if ov.overlay_state == True:
        threading.Thread(target=entity_loop, name='entity_loop', daemon=True).start()
        threading.Thread(target=aimbot, name='aimbot', daemon=True).start()
        threading.Thread(target=glow_esp, name='glow_esp', daemon=True).start()
        threading.Thread(target=rcs, name='rcs', daemon=True).start()
        threading.Thread(target=auto_pistol, name='auto_pistol', daemon=True).start()
        threading.Thread(target=trigger_bot, name='trigger_bot', daemon=True).start()
        threading.Thread(target=bunny_hop, name='bunny_hop', daemon=True).start()
        threading.Thread(target=auto_strafer, name='auto_strafer', daemon=True).start()
        threading.Thread(target=radar_hack, name='radar_hack', daemon=True).start()
        threading.Thread(target=no_flash, name='no_flash', daemon=True).start()
        threading.Thread(target=no_smoke, name='no_smoke', daemon=True).start()
        threading.Thread(target=fov_changer, name='fov_changer', daemon=True).start()
        threading.Thread(target=fake_lag, name='fake_lag', daemon=True).start()
        threading.Thread(target=hit_sound, args=['hitsound.wav'], name='hit_sound', daemon=True).start()
        threading.Thread(target=player_infos, name='player_infos', daemon=True).start()
        threading.Thread(target=night_mode, name='night_mode', daemon=True).start()
        threading.Thread(target=chat_spam, name='chat_spam', daemon=True).start()
        threading.Thread(target=convar_handler, name='convar_controller', daemon=True).start()
        threading.Thread(target=gui.make_interactive, name='interactive_gui', daemon=True).start()
        
        if DEBUG_MODE == False:
            console_handle = kernel32.GetConsoleWindow(0) # 0 to hide console window only
            win32gui.ShowWindow(console_handle, win32con.SW_HIDE)
        
        # Call as last
        dpg.start_dearpygui()
    except Exception as err:
        print(f'Threads have been canceled! Exiting...\nReason: {err}\nExiting...')
        os._exit(0)

if __name__ == '__main__':
    try:
        print(f'{DEBUG_MODE=}')
        mem = Memory(game_handle, client_dll, engine_dll)
        lp = LocalPlayer(mem)
        ent = Entity(mem)
        gui = GUI()
        main()
    except (Exception, KeyboardInterrupt) as err:
        ctypes.windll.user32.MessageBoxW(0, f'Failed to initialize!\nExiting...\nReason: {err}', 'Fatal Error', 0)
        os._exit(0)