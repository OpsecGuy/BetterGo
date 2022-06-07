
from ctypes.wintypes import DWORD, LPVOID, HANDLE, CHAR
from pymem import Pymem, process, exception, pattern
from dataclasses import dataclass
import os, time, threading, winsound, ctypes, win32process, win32api, win32con, win32event, sys

LPTHREAD_START_ROUTINE = ctypes.WINFUNCTYPE(LPVOID)
kernel32 = ctypes.WinDLL('kernel32.dll')

# TO:DO : cleanup code
try:
    game_handle = Pymem('csgo.exe')
    client_dll = process.module_from_name(game_handle.process_handle, 'client.dll').lpBaseOfDll
    client_dll_size = process.module_from_name(game_handle.process_handle, 'client.dll').SizeOfImage
    engine_dll = process.module_from_name(game_handle.process_handle, 'engine.dll').lpBaseOfDll
except exception.ProcessNotFound as err:
    ctypes.windll.user32.MessageBoxW(0, 'Could not find CS:GO process!\nMake sure the game is running first!', 'Fatal Error', 0)
    os._exit(0)

@dataclass
class Memory:
    game_handle: Pymem('csgo.exe')
    client_dll: process.module_from_name(game_handle.process_handle, 'client.dll').lpBaseOfDll
    client_dll_size: process.module_from_name(game_handle.process_handle, 'client.dll').SizeOfImage
    engine_dll: process.module_from_name(game_handle.process_handle, 'engine.dll').lpBaseOfDll


def get_sig(modname, _pattern, extra = 0, offset = 0, relative = True, deref = False):
    module = process.module_from_name(game_handle.process_handle, modname)
    result = pattern.pattern_scan_module(game_handle.process_handle, module, _pattern)

    if relative == False and deref == True:
        result += extra - module.lpBaseOfDll
    elif relative == True and deref == False:
        result = game_handle.read_int(result + offset) + extra - module.lpBaseOfDll
    elif relative == False and deref == False:
        result = game_handle.read_int(result + offset) + extra

    return result