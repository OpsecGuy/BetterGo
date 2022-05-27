from local import LocalPlayer
from helper import *
import offsets

class Entity(LocalPlayer):
    def __init__(self, mem) -> None:
        self.mem = mem
        self.entity_list = []
        self.glow_objects_list = []

    def entity_loop(self):
        try:
            self.entity_list.clear()
            for i in range(0, 1024):
                entity = self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwEntityList + i * 0x10)
                
                if entity != 0:
                    if self.class_id(entity) == None:
                        continue
                    if [entity, self.class_id(entity)] not in self.entity_list:
                        self.entity_list.append([i, entity, self.class_id(entity)])
        except Exception as err:
            pass

    def glow_objects_loop(self):
        try:
            self.glow_objects_list.clear()
            for i in range(1, 1024):
                glow_object = self.mem.game_handle.read_uint(self.glow_object() + 0x38 * (i - 1) + 0x4)

                if glow_object != 0:
                    if self.class_id(glow_object) == None:
                        continue
                    if [glow_object, self.class_id(glow_object)] not in self.glow_objects_list:
                        self.glow_objects_list.append([i, glow_object, self.class_id(glow_object)])
        except Exception as err:
            pass

    def get_entity(self, entity):
        return self.mem.game_handle.read_uint((self.mem.client_dll + offsets.dwEntityList) + entity * 0x10)

    def get_life_state(self, entity):
        return self.mem.game_handle.read_int(entity + offsets.m_lifeState)

    def get_health(self, entity):
        return self.mem.game_handle.read_int(entity + offsets.m_iHealth)

    def get_team(self, entity):
        return self.mem.game_handle.read_int(entity + offsets.m_iTeamNum)

    def get_dormant(self, entity):
        return self.mem.game_handle.read_bool(entity + offsets.m_bDormant)

    def set_dormant(self, entity, val: bool):
        return self.mem.game_handle.write_bool(entity + offsets.m_bDormant, val)

    def is_visible(self, entity):
        return self.mem.game_handle.read_bool(entity + offsets.m_bSpotted)

    def set_is_visible(self, entity, val: bool):
        return self.mem.game_handle.write_bool(entity + offsets.m_bSpotted, val)

    def is_defusing(self, entity):
        return self.mem.game_handle.read_bool(entity + offsets.m_bIsDefusing)

    def get_flag(self, entity):
        return self.mem.game_handle.read_int(entity + offsets.m_fFlags)

    def get_shots_fired(self, entity):
        return self.mem.game_handle.read_uint(entity + offsets.m_iShotsFired)

    def get_total_hits(self, entity):
        return self.mem.game_handle.read_uint(entity + 0x103f8) # m_totalHitsOnServer

    def is_bomb_planted(self):
        return self.mem.game_handle.read_bool(
            self.mem.game_handle.read_int(
            self.mem.client_dll + offsets.dwGameRulesProxy) + offsets.m_bBombPlanted)

    def glow_object(self):
        return self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwGlowObjectManager)

    def glow_object_size(self):
        return self.mem.game_handle.read_uint(self.glow_object() + 0xC)

    def glow_index(self, entity):
        return self.mem.game_handle.read_uint(entity + offsets.m_iGlowIndex)

    def is_bomb_planted(self):
        return self.mem.game_handle.read_bool((self.mem.client_dll + offsets.dwGameRulesProxy) + offsets.m_bBombPlanted)

    def engine_ptr(self):
        return self.mem.game_handle.read_uint(self.mem.engine_dll + offsets.dwClientState)

    def force_update(self):
        self.mem.game_handle.write_int(self.engine_ptr() + 0x174, -1)

    def in_game(self):
        return self.mem.game_handle.read_uint(self.engine_ptr() + offsets.dwClientState_State) == 6

    def get_map_name(self):
        return self.mem.game_handle.read_string(self.engine_ptr() +  offsets.dwClientState_Map)

    def class_id(self, entity):
        dwClientNetworkable = self.mem.game_handle.read_uint(entity + 0x8)
        dwGetClientClassFn = self.mem.game_handle.read_uint(dwClientNetworkable + 0x8)
        dwEntityClientClass = self.mem.game_handle.read_uint(dwGetClientClassFn + 0x1)
        classID = self.mem.game_handle.read_uint(dwEntityClientClass + 0x14)
        return classID

    def get_position(self, entity):
        x = self.mem.game_handle.read_float(entity + offsets.m_vecOrigin)
        y = self.mem.game_handle.read_float(entity + offsets.m_vecOrigin + 0x4)
        z = self.mem.game_handle.read_float(entity + offsets.m_vecOrigin + 0x8)
        return Vector3(x, y, z)

    def set_position(self, entity, vec3: Vector3):
        x = self.mem.game_handle.write_float(entity + offsets.m_vecOrigin, vec3.x)
        y = self.mem.game_handle.write_float(entity + offsets.m_vecOrigin + 0x4, vec3.y)
        y = self.mem.game_handle.write_float(entity + offsets.m_vecOrigin + 0x4, vec3.z)

    def get_view_angle(self):
        x = self.mem.game_handle.read_float(self.engine_ptr() + offsets.dwClientState_ViewAngles)
        y = self.mem.game_handle.read_float(self.engine_ptr() + offsets.dwClientState_ViewAngles + 0x4)
        z = self.mem.game_handle.read_float(self.engine_ptr() + offsets.dwClientState_ViewAngles + 0x8)
        return Vector3(x, y, z)

    def set_view_angle(self, angle: Vector3):
        x = self.mem.game_handle.write_float(self.engine_ptr() + offsets.dwClientState_ViewAngles, angle.x)
        y = self.mem.game_handle.write_float(self.engine_ptr() + offsets.dwClientState_ViewAngles + 0x4, angle.y)
        z = self.mem.game_handle.write_float(self.engine_ptr() + offsets.dwClientState_ViewAngles + 0x8, angle.z)

    def get_bone_position(self, entity, bone_id: int):
        base = self.mem.game_handle.read_uint(entity + offsets.m_dwBoneMatrix)
        x = self.mem.game_handle.read_float(base + 0x30 * bone_id + 0x0c)
        y = self.mem.game_handle.read_float(base + 0x30 * bone_id + 0x1c)
        z = self.mem.game_handle.read_float(base + 0x30 * bone_id + 0x2c)
        return Vector3(x, y, z)

    def active_weapon(self):
        actWeapon = self.mem.game_handle.read_uint(self.local_player() + offsets.m_hActiveWeapon) & 0xFFF
        actWeapon = self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwEntityList + (actWeapon - 1) * 0x10)
        return self.mem.game_handle.read_short(actWeapon + offsets.m_iItemDefinitionIndex)

    def get_name(self, entity):
        player_info = self.mem.game_handle.read_uint(self.engine_ptr()
        + offsets.dwClientState_PlayerInfo)
                
        player_info_items = self.mem.game_handle.read_uint(
            self.mem.game_handle.read_uint(player_info + 0x40) + 0xC
        )
        info = self.mem.game_handle.read_uint(player_info_items + 0x28 + (entity * 0x34))

        if info > 0:
            return self.mem.game_handle.read_string(info + 0x10)

    def get_rank(self, entity):
        player_resources = self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwPlayerResource)
        return self.mem.game_handle.read_uint(player_resources + offsets.m_iCompetitiveRanking + (entity  + 1) * 0x4)

    def get_wins(self, entity):
        player_resources = self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwPlayerResource)
        return self.mem.game_handle.read_uint(player_resources + offsets.m_iCompetitiveWins + (entity + 1) * 0x4)