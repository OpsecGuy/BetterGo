import offsets, struct
from helper import *

class Entity():
    def __init__(self, mem) -> None:
        self.mem = mem
        self.entity_list = []
        self.glow_objects_list = []

    def entity_loop(self) -> list:
        try:
            self.entity_list.clear()
            # 0 - world entity
            # 1 - 64 - reserved for players
            for i in range(0, 512):
                entity = self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwEntityList + i * 0x10)

                if entity != 0:
                    class_id = self.class_id(entity)
                    if class_id == None:
                        continue
                    if [entity, class_id] not in self.entity_list:
                        self.entity_list.append([i, entity, class_id])
        except Exception as err:
            pass

    def glow_objects_loop(self) -> list:
        try:
            self.glow_objects_list.clear()

            for i in range(1, self.glow_object_size()):
                glow_object = self.mem.game_handle.read_uint(self.glow_object() + 0x38 * (i - 1) + 0x4)

                if glow_object != 0:
                    class_id = self.class_id(glow_object)
                    if class_id == None:
                        continue
                    if [glow_object, class_id] not in self.glow_objects_list:
                        self.glow_objects_list.append([i, glow_object, class_id])
        except Exception as err:
            pass

    def get_entity(self, entity: int) -> int:
        return self.mem.game_handle.read_uint((self.mem.client_dll + offsets.dwEntityList) + entity * 0x10)

    def get_life_state(self, entity: int) -> int:
        return self.mem.game_handle.read_int(entity + offsets.m_lifeState)

    def get_health(self, entity: int) -> int:
        return self.mem.game_handle.read_int(entity + offsets.m_iHealth)

    def get_team(self, entity: int) -> int:
        return self.mem.game_handle.read_int(entity + offsets.m_iTeamNum)

    def get_dormant(self, entity: int) -> bool:
        return self.mem.game_handle.read_bool(entity + offsets.m_bDormant)

    def set_dormant(self, entity: int, value: bool) -> None:
        return self.mem.game_handle.write_bool(entity + offsets.m_bDormant, value)

    def is_spotted(self, entity: int) -> bool:
        return self.mem.game_handle.read_bool(entity + offsets.m_bSpotted)

    def set_spotted(self, entity: int, value: bool) -> None:
        return self.mem.game_handle.write_bool(entity + offsets.m_bSpotted, value)

    def is_spotted_by_mask(self, entity: int) -> bool:
        return self.mem.game_handle.read_bool(entity + offsets.m_bSpottedByMask)

    def set_spotted_by_mask(self, entity: int, value: bool) -> None:
        return self.mem.game_handle.write_bool(entity + offsets.m_bSpottedByMask, value)

    def is_defusing(self, entity: int) -> bool:
        return self.mem.game_handle.read_bool(entity + offsets.m_bIsDefusing)

    def is_scoping(self, entity: int) -> bool:
        return self.mem.game_handle.read_bool(entity + offsets.m_bIsScoped)

    def is_protected(self, entity: int) -> bool:
        return self.mem.game_handle.read_bool(entity + offsets.m_bGunGameImmunity)

    def get_flag(self, entity: int) -> int:
        return self.mem.game_handle.read_uint(entity + offsets.m_fFlags)

    def is_bomb_planted(self) -> bool:
        return self.mem.game_handle.read_bool(
            self.mem.game_handle.read_int(
            self.mem.client_dll + offsets.dwGameRulesProxy) + offsets.m_bBombPlanted)

    def glow_object(self) -> int:
        return self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwGlowObjectManager)

    def glow_object_size(self) -> int:
        return self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwGlowObjectManager + 0xC)

    def glow_index(self, entity: int) -> int:
        return self.mem.game_handle.read_uint(entity + offsets.m_iGlowIndex)

    def is_bomb_planted(self) -> bool:
        return self.mem.game_handle.read_bool((self.mem.client_dll + offsets.dwGameRulesProxy) + offsets.m_bBombPlanted)

    def engine_ptr(self) -> int:
        return self.mem.game_handle.read_uint(self.mem.engine_dll + offsets.dwClientState)

    def force_update(self) -> None:
        self.mem.game_handle.write_int(self.engine_ptr() + 0x174, -1)

    def in_game(self) -> int:
        return self.mem.game_handle.read_uint(self.engine_ptr() + offsets.dwClientState_State) == 6

    def get_map_name(self) -> str:
        return self.mem.game_handle.read_string(self.engine_ptr() +  offsets.dwClientState_Map)

    def get_map_dir(self) -> str:
        return self.mem.game_handle.read_string(self.engine_ptr() +  offsets.dwClientState_MapDirectory)

    def class_id(self, entity: int) -> int:
        client_networkable = self.mem.game_handle.read_uint(entity + 0x8)
        dwGetClientClassFn = self.mem.game_handle.read_uint(client_networkable + 0x8)
        entity_client_class = self.mem.game_handle.read_uint(dwGetClientClassFn + 0x1)
        class_id = self.mem.game_handle.read_uint(entity_client_class + 0x14)
        return class_id

    def get_position(self, entity: int) -> Vector3:
        position_bytes = self.mem.game_handle.read_bytes(entity + offsets.m_vecOrigin, 0xC)
        var = struct.unpack("3f", position_bytes)
        return Vector3(*var)

    def set_position(self, entity, position: Vector3) -> None:
        Vector3(self.mem.game_handle.write_float(entity + offsets.m_vecOrigin, position.x),
                self.mem.game_handle.write_float(entity + offsets.m_vecOrigin + 0x4, position.y),
                self.mem.game_handle.write_float(entity + offsets.m_vecOrigin + 0x4, position.z)
        )

    def get_view_angle(self) -> Vector3:
        view_angle_bytes = self.mem.game_handle.read_bytes(self.engine_ptr() + offsets.dwClientState_ViewAngles, 0xC)
        var = struct.unpack("3f", view_angle_bytes)
        return Vector3(*var)

    def set_view_angle(self, angle: Vector3) -> None:
        Vector3(self.mem.game_handle.write_float(self.engine_ptr() + offsets.dwClientState_ViewAngles, angle.x),
                self.mem.game_handle.write_float(self.engine_ptr() + offsets.dwClientState_ViewAngles + 0x4, angle.y),
                self.mem.game_handle.write_float(self.engine_ptr() + offsets.dwClientState_ViewAngles + 0x8, angle.z),
        )

    def get_bone_position(self, entity, bone_id: int) -> Vector3:
        bone_matrix = self.mem.game_handle.read_uint(entity + offsets.m_dwBoneMatrix)
        return Vector3(self.mem.game_handle.read_float(bone_matrix + 0x30 * bone_id + 0x0c),
                       self.mem.game_handle.read_float(bone_matrix + 0x30 * bone_id + 0x1c),
                       self.mem.game_handle.read_float(bone_matrix + 0x30 * bone_id + 0x2c)
        )

    def get_name(self, entity: int) -> bytes:
        player_info = self.mem.game_handle.read_uint(self.engine_ptr()
        + offsets.dwClientState_PlayerInfo)

        player_info_items = self.mem.game_handle.read_uint(
            self.mem.game_handle.read_uint(player_info + 0x40) + 0xC
        )
        info = self.mem.game_handle.read_uint(player_info_items + 0x28 + (entity * 0x34))

        if info > 0:
            return self.mem.game_handle.read_bytes(info + 0x10, 32)
            # return self.mem.game_handle.read_string(info + 0x10)

    def get_rank(self, entity: int) -> int:
        return self.mem.game_handle.read_uint((self.mem.client_dll + offsets.dwPlayerResource) 
                                              + offsets.m_iCompetitiveRanking + (entity  + 1) * 0x4)

    def get_wins(self, entity: int) -> int:
        return self.mem.game_handle.read_uint((self.mem.client_dll + offsets.dwPlayerResource) 
                                              + offsets.m_iCompetitiveWins + (entity + 1) * 0x4)

    def view_matrix(self) -> Vector3:
        view_matrix = self.mem.game_handle.read_bytes(self.mem.client_dll + offsets.dwViewMatrix, 64)
        return struct.unpack("16f", view_matrix)
