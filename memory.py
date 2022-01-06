from dataclasses import dataclass
import pymem
import re

game_handle = pymem.Pymem('csgo.exe')
client_dll = pymem.pymem.process.module_from_name(game_handle.process_handle, 'client.dll').lpBaseOfDll
client_dll_size = pymem.pymem.process.module_from_name(game_handle.process_handle, 'client.dll').SizeOfImage
engine_dll = pymem.pymem.process.module_from_name(game_handle.process_handle, 'engine.dll').lpBaseOfDll

def get_sig(modname, pattern, extra = 0, offset = 0, relative = True):
    module = pymem.pymem.process.module_from_name(game_handle.process_handle, modname)
    bytes = game_handle.read_bytes(module.lpBaseOfDll, module.SizeOfImage)
    match = re.search(pattern, bytes).start()
    non_relative = game_handle.read_int(module.lpBaseOfDll + match + offset) + extra
    yes_relative = game_handle.read_int(module.lpBaseOfDll + match + offset) + extra - module.lpBaseOfDll
    return yes_relative if relative else non_relative

@dataclass
class Memory:
    game_handle: pymem.Pymem('csgo.exe')
    client_dll: pymem.pymem.process.module_from_name(game_handle.process_handle, 'client.dll').lpBaseOfDll
    client_dll_size: pymem.pymem.process.module_from_name(game_handle.process_handle, 'client.dll').SizeOfImage
    engine_dll: pymem.pymem.process.module_from_name(game_handle.process_handle, 'engine.dll').lpBaseOfDll