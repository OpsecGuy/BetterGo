__author__ = "MaGicSuR / https://github.com/MaGicSuR"

from asyncio.exceptions import CancelledError
from memory import *
from entity import *
from local import *
import helper as h
import winsound
from asyncio import Task, tasks, sleep, gather, run
import ctypes
import time
import os

async def glow_esp():
    while True:
        try:
            for i in range(1, 2222):
                entityList = mem.game_handle.read_uint(ent.glow_object() + 0x38 * (i - 1) + 0x4)
                if entityList <= 0:
                    continue
                if ent.class_id(entityList) == None:
                    continue
                if ent.get_dormant(entityList) == True:
                    continue
                if ent.class_id(entityList) == 40:
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), 1.0)
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), 1.0)
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x10), 1.0)
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x14), 0.55)
                    mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x28), True)
                    mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x29), False)
                elif ent.class_id(entityList) == 34 or ent.class_id(entityList) == 129:
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x8), 1.0)
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0xC), 1.0)
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x10), 1.0)
                    mem.game_handle.write_float(ent.glow_object() + ((0x38 * (i - 1)) + 0x14), 0.55)
                    mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x28), True)
                    mem.game_handle.write_bool(ent.glow_object() + ((0x38 * (i - 1)) + 0x29), False)

        except Exception as err:
            pass
        await sleep(0)

async def auto_pistol(key: int, delay: float):
    while True:
        try:
            if ctypes.windll.user32.GetAsyncKeyState(key) and h.weapon_pistol(ent.active_weapon()):
                lp.force_attack(6)
                await sleep(delay)
        except Exception:
            pass
        await sleep(0)

async def bunny_hop(key: int):
    while True:
        try:
            if lp.get_current_state() == 5:
                while ctypes.windll.user32.GetAsyncKeyState(key):
                    if ent.get_flag(lp.local_player()) == 257:
                        lp.force_jump(5)
                        await sleep(0)
                    else:
                        lp.force_jump(4)
                        await sleep(0)
        except Exception:
            pass
        await sleep(0)

async def radar_hack():
    while True:
        try:
            if ent.in_game():
                for i in ent.entity_list:
                    ent.set_is_visible(i, True)
        except Exception:
            pass
        await sleep(1)

async def fov_changer(key_add: int, key_subtract: int, key_normalize: int):
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
        except Exception:
            pass
        await sleep(0.1)

async def hit_marker(filename: str):
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
        except Exception:
            pass
        await sleep(0.1)

async def money_reveal(key: int):
    # Thanks Daniel for that. Modified script for my needs.
    # https://github.com/danielkrupinski/OneByteMoney

    clientModule = mem.game_handle.read_bytes(mem.client_dll, mem.client_dll_size)
    address = mem.client_dll + re.search(rb'.\x0C\x5B\x5F\xB8\xFB\xFF\xFF\xFF',
                                clientModule).start()
    while True:
        try:
            if ent.in_game():
                if ctypes.windll.user32.GetAsyncKeyState(key):
                    await sleep(0.12)
                    mem.game_handle.write_uchar(address, 0xEB if mem.game_handle.read_uchar(address) == 0x75 else 0x75)
        except Exception:
            pass
        await sleep(0.1)

async def exit(key: int):
    while True:
        if ctypes.windll.user32.GetAsyncKeyState(key):
            print('Exiting...')
            for i in tasks.all_tasks():
                Task.cancel(i)

            lp.set_fov(90)
            mem.game_handle.write_int(ent.engine_ptr() + 0x174, -1)
            os._exit(0)
        await sleep(0.1)

async def start_threads():
    try:
        await gather(
            glow_esp(),
            auto_pistol(0x05, 0.07),
            bunny_hop(0x20),
            radar_hack(),
            fov_changer(0x68, 0x62, 0x65),
            #hit_marker('hitsound.wav'),
            money_reveal(0x67),
            exit(0x2E),
        )
    except (Exception, CancelledError) as err:
        print(f'Threads have been canceled! Exiting...\nReason: {err}\nExiting...')
        os._exit(0)

if __name__ == '__main__':
    try:
        start_timer = time.perf_counter()
        mem = Memory(game_handle, client_dll, client_dll_size, engine_dll)
        ent = Entity(mem)
        lp = LocalPlayer(mem)
        ent.entity_loop()
        ent.glow_objects_loop()
        stop_timer = time.perf_counter()
        print(f'Initialization took {round((stop_timer - start_timer), 5)} seconds.')
    except (Exception, KeyboardInterrupt) as err:
        print(f'Failed to initialize!\nReason: {err}\nExiting...')
        os._exit(0)
    
    run(start_threads())
