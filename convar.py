from memory import *
import offsets

class ConVar():
    def __init__(self, name):
        try:
            self.address = 0
            vstdlib = process.module_from_name(game_handle.process_handle, 'vstdlib.dll').lpBaseOfDll
            v1 = game_handle.read_uint(vstdlib + offsets.interface_engine_cvar)
            v2 = game_handle.read_uint(game_handle.read_uint(game_handle.read_uint(v1 + 0x34)) + 0x4)
            while v2 != 0:
                if name == game_handle.read_string(game_handle.read_uint(v2 + 0x0C)):
                    self.address = v2
                    return
                # print(game_handle.read_string(game_handle.read_uint(a0 + 0x0C)))
                v2 = game_handle.read_uint(v2 + 0x4)
        except Exception as err:
            print(err)
    
    def get_name(self):
        return game_handle.read_string(game_handle.read_uint(self.address + 0xC))
    
    def get_description(self):
        return game_handle.read_string(game_handle.read_uint(self.address + 0x10))

    def get_default_value(self):
        return game_handle.read_string(game_handle.read_uint(self.address + 0x20))
    
    def get_size(self):
        return game_handle.read_uint(self.address + 0x28)

    def get_flags(self):
        return game_handle.read_uint(self.address + 0x14)

    def get_int(self):
        return game_handle.read_uint(self.address + 0x30) ^ self.address
    
    def get_string(self):
        return game_handle.read_string(game_handle.read_uint(self.address + 0x24))

    def set_int(self, value: int):
        game_handle.write_int(self.address + 0x30, value ^ self.address)

    def set_string(self, value: str):
        game_handle.write_bytes(game_handle.read_uint(self.address + 0x24), value.encode('utf-8'), 128)