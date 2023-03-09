from helper import *
import offsets, struct

class LocalPlayer():
    def __init__(self, mem) -> None:
        self.mem = mem

    def local_player(self) -> int:
        return self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwLocalPlayer)

    def get_current_state(self) -> int:
        return self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwForceJump)

    def get_flashbang_duration(self) -> float:
        return self.mem.game_handle.read_float(self.local_player() + offsets.m_flFlashDuration)

    def set_flashbang_duration(self, value: float) -> None:
        self.mem.game_handle.write_float(self.local_player() + offsets.m_flFlashDuration, value)

    def set_flashbang_alpha(self, value: float) -> None:
        self.mem.game_handle.write_float(self.local_player() + offsets.m_flFlashMaxAlpha, value)

    def get_total_hits(self) -> int:
        return self.mem.game_handle.read_uint(self.local_player() + offsets.m_totalHitsOnServer)

    def get_shots_fired(self) -> int:
        return self.mem.game_handle.read_uint(self.local_player() + offsets.m_iShotsFired)

    def get_crosshair_id(self) -> int:
        return self.mem.game_handle.read_uint(self.local_player() + offsets.m_iCrosshairId)

    def get_entity_by_crosshair(self) -> int:
        return self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwEntityList + ((self.get_crosshair_id() - 1) * 0x10))

    def get_team_by_crosshair(self, entity: int) -> int:
        return self.mem.game_handle.read_int(entity + offsets.m_iTeamNum)

    def get_health_by_crosshair(self, entity: int) -> int:
        return self.mem.game_handle.read_int(entity + offsets.m_iHealth)

    def force_jump(self, value: int) -> None:
        self.mem.game_handle.write_int(self.mem.client_dll + offsets.dwForceJump, value)

    def force_left(self, value: int) -> None:
        self.mem.game_handle.write_int(self.mem.client_dll + offsets.dwForceLeft, value)

    def force_right(self, value: int) -> None:
        self.mem.game_handle.write_int(self.mem.client_dll + offsets.dwForceRight, value)

    def force_attack(self, value: int) -> None:
        self.mem.game_handle.write_uint(self.mem.client_dll + offsets.dwForceAttack, value)

    def force_attack2(self, value: int) -> None:
        self.mem.game_handle.write_uint(self.mem.client_dll + offsets.dwForceAttack2, value)

    def active_weapon(self):
        active_weapon = self.mem.game_handle.read_uint(self.local_player() + offsets.m_hActiveWeapon) & 0xFFF
        weapon_handle = self.mem.game_handle.read_uint(self.mem.client_dll + offsets.dwEntityList + (active_weapon - 1) * 0x10)
        return self.mem.game_handle.read_short(weapon_handle + offsets.m_iItemDefinitionIndex)

    def send_packets(self, value: bool) -> None:
        self.mem.game_handle.write_bool(self.mem.engine_dll + offsets.dwbSendPackets, value)

    def get_fov(self) -> int:
        return self.mem.game_handle.read_int(self.local_player() + offsets.m_iDefaultFOV)

    def set_fov(self, value: int) -> None:
        self.mem.game_handle.write_int(self.local_player() + offsets.m_iDefaultFOV, value)

    def aim_punch_angle(self) -> Vector3:
        punch_angle_bytes = self.mem.game_handle.read_bytes(self.local_player() + offsets.m_aimPunchAngle, 0xC)
        var = struct.unpack("3f", punch_angle_bytes)
        return Vector3(*var)

    def get_move_type(self) -> int:
        return self.mem.game_handle.read_uint(self.local_player() + offsets.m_MoveType)

    def get_view(self) -> Vector3:
        vec_view_bytes = self.mem.game_handle.read_bytes(self.local_player() + offsets.m_vecViewOffset, 0xC)
        var = struct.unpack("3f", vec_view_bytes)
        return Vector3(*var)

    def get_eye_position(self, origin: Vector3) -> Vector3:
        my_view = self.get_view()
        return Vector3(origin.x + my_view.x,
                       origin.y + my_view.y,
                       origin.z + my_view.z)
