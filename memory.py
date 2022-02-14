from dataclasses import dataclass
from pymem import Pymem, process, exception
import re, os, threading, winsound, ctypes, time

try:
    game_handle = Pymem('csgo.exe')
    client_dll = process.module_from_name(game_handle.process_handle, 'client.dll').lpBaseOfDll
    client_dll_size = process.module_from_name(game_handle.process_handle, 'client.dll').SizeOfImage
    engine_dll = process.module_from_name(game_handle.process_handle, 'engine.dll').lpBaseOfDll
except exception.ProcessNotFound as err:
    print(f'Failed to open a handle!')
    os._exit(0)

@dataclass
class Memory:
    game_handle: Pymem('csgo.exe')
    client_dll: process.module_from_name(game_handle.process_handle, 'client.dll').lpBaseOfDll
    client_dll_size: process.module_from_name(game_handle.process_handle, 'client.dll').SizeOfImage
    engine_dll: process.module_from_name(game_handle.process_handle, 'engine.dll').lpBaseOfDll

def get_sig(modname, pattern, extra = 0, offset = 0, relative = True):
    module = process.module_from_name(game_handle.process_handle, modname)
    bytes = game_handle.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, bytes).start()
    non_relative = game_handle.read_int(module.lpBaseOfDll + match + offset) + extra
    yes_relative = game_handle.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
    return yes_relative if relative else non_relative