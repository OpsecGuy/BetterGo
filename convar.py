from memory import *
from ctypes import *

class ConVar():
    def __init__(self, name):
        try:
            vstdlib = process.module_from_name(game_handle.process_handle, 'vstdlib.dll').lpBaseOfDll
            v1 = game_handle.read_uint(vstdlib + 0x3E9EC)
            self.address = 0
            v2 = game_handle.read_uint(game_handle.read_uint(game_handle.read_uint(v1 + 0x34)) + 0x4)
            while v2 != 0:
                if name == game_handle.read_string(game_handle.read_uint(v2 + 0x0C)):
                    self.address = v2
                    return
                # print(game_handle.read_string(game_handle.read_uint(a0 + 0x0C)))
                v2 = game_handle.read_uint(v2 + 0x4)
        except Exception as err:
            pass

    def get_int(self):
        a0 = c_int32()
        a1 = game_handle.read_uint(self.address + 0x30) ^ self.address
        windll.ntdll.memcpy(pointer(a0), pointer(c_int32(a1)), 4)
        return a0.value

    def set_int(self, value: int):
        game_handle.write_int(self.address + 0x30, value ^ self.address)

    def get_float(self):
        a0 = c_float()
        a1 = game_handle.read_uint(self.address + 0x2C) ^ self.address
        windll.ntdll.memcpy(pointer(a0), pointer(c_int32(a1)), 4)
        return a0.value