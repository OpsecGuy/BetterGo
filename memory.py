import os, time, ctypes, win32process, win32con, win32event, win32gui, sys, struct
from pymem import Pymem, process, exception, pattern
from dataclasses import dataclass
from helper import get_hash_of

try:
    kernel32 = ctypes.WinDLL('kernel32.dll')
    ntdll = ctypes.WinDLL('ntdll.dll')
except Exception as err:
    ctypes.windll.user32.MessageBoxW(0, 'Failed to hook Kernel32/Ntdll', 'Fatal Error', 0)
    os._exit(0)

try:
    glfw_path = os.getcwd() + '\\glfw3.dll'
    valid_file_md5 = '732d3c46d42abd44fd5555fe9c3ae29f'
    hash = get_hash_of(glfw_path)

    if hash != valid_file_md5:
        ctypes.windll.user32.MessageBoxW(0, f'MD5 hash of glfw3.dll does not match', 'Fatal Error', 0)
        os._exit(0)

except Exception as err:
    ctypes.windll.user32.MessageBoxW(0, f'{err}', 'Fatal Error', 0)
    os._exit(0)

while True:
    try:
        game_handle = Pymem('csgo.exe')
        client_dll = process.module_from_name(game_handle.process_handle, 'client.dll').lpBaseOfDll
        engine_dll = process.module_from_name(game_handle.process_handle, 'engine.dll').lpBaseOfDll
        print(f'{game_handle.base_address=:#0x}\n{client_dll=:#0x}\n{engine_dll=:#0x}')
        break
    except (exception.ProcessNotFound, AttributeError) as err:
        os.system('cls')
        print('Waiting for csgo.exe!')
        time.sleep(1)
        continue

@dataclass
class Memory:
    game_handle: 0
    client_dll: 0
    engine_dll: 0

def get_sig(module_name, _pattern, extra = 0, offset = 0, relative = True, deref = False):
    module = process.module_from_name(game_handle.process_handle, module_name)
    result = pattern.pattern_scan_module(game_handle.process_handle, module, _pattern)

    if relative == False and deref == True:
        result += extra - module.lpBaseOfDll
    elif relative == True and deref == False:
        result = game_handle.read_int(result + offset) + extra - module.lpBaseOfDll
    elif relative == False and deref == False:
        result = game_handle.read_int(result + offset) + extra

    return result

def execute_cmd(command: str, address: int):
    command_buffer = kernel32.VirtualAllocEx(game_handle.process_handle, 0, sys.getsizeof(command) + 1, 0x00001000 | 0x00002000, win32con.PAGE_READWRITE)
    kernel32.WriteProcessMemory(game_handle.process_handle, command_buffer, command, sys.getsizeof(command), 0)
    command_thread = win32process.CreateRemoteThread(game_handle.process_handle, None, 0, (address), command_buffer, 0)
    win32event.WaitForSingleObject(command_thread[0], 0)
    thread_handle = int(str(command_thread[0]).removesuffix('>').split(':')[1])
    kernel32.VirtualFreeEx(game_handle.process_handle, command_buffer, sys.getsizeof(command) + 1, win32con.MEM_RELEASE)
    kernel32.CloseHandle(thread_handle)
