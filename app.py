__author__ = "MaGicSuR / https://github.com/MaGicSuR"

from memory import *
from entity import *
from local import *
from gui import *
import helper as h

def glow_esp():
    while True:
        try:
            for i in range(1, 1024):
                entity_list = mem.game_handle.read_uint(ent.glow_object() + 0x38 * (i - 1) + 0x4)
                
                if entity_list <= 0:
                    continue
                if ent.class_id(entity_list) == None:
                    continue
                if ent.get_dormant(entity_list) == True:
                    continue

                if ent.class_id(entity_list) == 40:
                    if ent.get_team(entity_list) != ent.get_team(lp.local_player()):
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), 0.47)
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), 0.24)
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x10), 1.0)
                        mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x14), 0.6)
                        mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x28), True)
                        mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x29), False)

                elif h.class_id_c4(ent.class_id(entity_list)) or h.class_id_gun(ent.class_id(entity_list)):
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), 0.95)
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), 0.12)
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x10), 0.54)
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x14), 0.6)
                    mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x28), True)
                    mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x29), False)

                elif h.class_id_grenade(ent.class_id(entity_list)):
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), 1.0)
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), 1.0)
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x10), 1.0)
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x14), 0.6)
                    mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x28), True)
                    mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x29), False)

        except Exception as err:
            pass
        time.sleep(0.001)

def auto_pistol(key: int, delay: float):
    while True:
        try:
            if ctypes.windll.user32.GetAsyncKeyState(key) and h.weapon_pistol(ent.active_weapon()):
                lp.force_attack(6)
                time.sleep(delay)
        except Exception as err:
            pass
        time.sleep(0.01)

def bunny_hop(key: int):
    while True:
        try:
            if lp.get_current_state() == 5:
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
            if ent.in_game():
                for i in ent.entity_list:
                    ent.set_is_visible(i, True)
        except Exception as err:
            pass
        time.sleep(1)

def fov_changer(key_add: int, key_subtract: int, key_normalize: int):
    while True:
        try:
            v1 = lp.get_fov()
            v2 = 0
            if ent.in_game():
                if ctypes.windll.user32.GetAsyncKeyState(key_add):
                    v2 = v1 + 1
                    lp.set_fov(v2)
                elif ctypes.windll.user32.GetAsyncKeyState(key_subtract):
                    v2 = v1 - 1
                    lp.set_fov(v2)
                elif ctypes.windll.user32.GetAsyncKeyState(key_normalize):
                    lp.set_fov(90)
        except Exception as err:
            pass
        time.sleep(0.1)

def hit_sound(filename: str):
    oldDmg = 0
    while True:
        try:
            damage = ent.get_total_hits(lp.local_player())
            if ent.get_health(ent.player) <= 0:
                continue

            if damage != oldDmg:
                oldDmg = damage
                if 0 < oldDmg >= 255:
                    continue
                winsound.PlaySound(filename, winsound.SND_ASYNC)
        except Exception as err:
            pass
        time.sleep(0.1)

def spectator_list():
    spectators = []
    while True:
        spectators.clear()
        try:
            if ent.get_health(lp.local_player()) <= 0:
                return ''

            for i in range(0, 64):
                if ent.get_entity(i) <= 0:
                    continue

                player_name = ent.get_name(i)
                if player_name == None or player_name == 'GOTV':
                    continue

                if ent.get_team(ent.get_entity(i)) == ent.get_team(lp.local_player()):
                    observed_target_handle = mem.game_handle.read_uint(ent.get_entity(i) + offsets.m_hObserverTarget) & 0xFFF
                    spectected = mem.game_handle.read_uint(mem.client_dll + offsets.dwEntityList + (observed_target_handle - 1) * 0x10)
                    
                    if spectected == lp.local_player():
                        spectators.append(ent.get_name(i))
    
            if len(spectators) > 0:
                format = '\n'.join(spectators)
                return format
            else:
                return ''

        except Exception as err:
            pass
        time.sleep(1)

def exit(key: int):
    while True:
        if ctypes.windll.user32.GetAsyncKeyState(key):
            try:
                print('Exiting...')
                mem.game_handle.write_int(ent.engine_ptr() + 0x174, -1)
                lp.set_fov(90)
            except exception.MemoryWriteError as err:
                print(err)
            
            os._exit(0)
        time.sleep(0.2)

def create_window():
    h = window.create_window()
    while True:
        event, values = h.read(timeout=100)
        if ent.in_game():
            h['spec_list'].update(spectator_list())

def start_threads():
    try:
        threading.Thread(target=glow_esp, name='glow_esp').start()
        threading.Thread(target=auto_pistol, args=[0x05, 0.02], name='auto_pistol').start()
        threading.Thread(target=bunny_hop, args=[0x20], name='bunny_hop').start()
        threading.Thread(target=radar_hack, name='radar_hack').start()
        threading.Thread(target=fov_changer, args=[0x68, 0x62, 0x65], name='fov_changer').start()
        threading.Thread(target=hit_sound, args=['hitsound.wav'], name='hit_sound').start()
        threading.Thread(target=spectator_list, name='spectator_list').start()
        threading.Thread(target=exit, args=[0x2E], name='exit').start()
        threading.Thread(target=create_window, name='create_window').start()

    except Exception as err:
        print(f'Threads have been canceled! Exiting...\nReason: {err}\nExiting...')
        os._exit(0)

if __name__ == '__main__':
    try:
        start_timer = time.perf_counter()
        mem = Memory(game_handle, client_dll, client_dll_size, engine_dll)
        lp = LocalPlayer(mem)
        ent = Entity(mem)
        window = GUI()
        ent.entity_loop()
        start_threads()
        stop_timer = time.perf_counter()
        print(f'Initialization took {round((stop_timer - start_timer), 5)} seconds.')
        print('[NUMPAD 8/5/2] FOV Changer\n[MOUSE4] Auto Pistol\n[SPACE] BunnyHop\n[DEL] Exit safely from app!')
    except (Exception, KeyboardInterrupt) as err:
        print(f'Failed to initialize!\nReason: {err}\nExiting...')
        os._exit(0)