
from ctypes.wintypes import DWORD, LPVOID, HANDLE, CHAR
from pymem import Pymem, process, exception, pattern
from dataclasses import dataclass
import os, time, threading, winsound, ctypes, win32process, win32api, win32con, win32event, sys

# TO:DO : cleanup code
try:
    kernel32 = ctypes.WinDLL('kernel32.dll')
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
    vchat_spam_buffer = kernel32.VirtualAllocEx(game_handle.process_handle, 0, sys.getsizeof(command) + 1, 0x00001000 | 0x00002000, win32con.PAGE_READWRITE)
    kernel32.WriteProcessMemory(game_handle.process_handle, vchat_spam_buffer, command, sys.getsizeof(command), 0)
    chat_spam_thread = win32process.CreateRemoteThread(game_handle.process_handle, None, 0, (address), vchat_spam_buffer, 0)
    win32event.WaitForSingleObject(chat_spam_thread[0], 0)
    thread_handle = int(str(chat_spam_thread[0]).removesuffix('>').split(':')[1])
    kernel32.VirtualFreeEx(game_handle.process_handle, vchat_spam_buffer, sys.getsizeof(command) + 1, win32con.MEM_RELEASE)
    kernel32.CloseHandle(thread_handle)