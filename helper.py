import hashlib, random
from math import atan2, hypot, sqrt, pi
from dataclasses import dataclass
from memory import ctypes
from enum import IntEnum

player_info_buffer = []

config_example = {
    'aimbot': {
        'switch': False,
        'key': 'LEFT MOUSE',
        'fov': 2.0,
        'smooth': 10.0,
        'bone': 'HEAD',
        'visible_only': False,
        'attack_team': False,
    },
    "standalone_rcs": {
        "switch": False,
        "strength": 2.0,
        "min_bullets": 1,
    },
    "triggerbot": {
        "switch": True,
        "key": "MOUSE 4",
        "humanization": True,
        "delay": 0.025,
    },
    "visuals": {
        "player_esp": False,
        "glow_team": False,
        "health_mode": False,
        "item_esp": False,
        "night_mode": False,
        "night_mode_strength": 1.0,
        "noflash": False,
        "noflash_strength": 255.0,
        "player_fov": 90,
    },
    "overlay": {
        "box_esp": False,
        "hp_text": False,
        "snap_lines": False,
        "distance": False,
        "head_indicator": False,
        "bomb_indicator": False,
        "grenade_traces": False,
        "sniper_crosshair": True,
        "recoil_crosshair": False,
        "crosshair_style": 'Crosshair',
    },
    "misc":{
        "auto_pistol": True,
        "auto_pistol_key": 'MOUSE 5',
        "radar_hack": False,
        "hit_sound": True,
        "bunny_hop": True,
        "auto_strafe": False,
        "auto_zeus": False,
        "knife_bot": False,
        "no_smoke": False,
        "spec_alert": False,
        "show_fps": False,
        "fake_lag": False,
        "lag_strength": 0.001,
    },
    "other":{
        "safe_mode": True,
    },
}

class GlowObjectDefinition_t(ctypes.Structure):
    _fields_ = [
        ("m_nNextFreeSlot", ctypes.c_int32),
        ("m_pEntity", ctypes.c_uint32),
        ("r", ctypes.c_float), # 0x8
        ("g", ctypes.c_float),
        ("b", ctypes.c_float),
        ("a", ctypes.c_float),
        ("m_bGlowAlphaCappedByRenderAlpha", ctypes.c_bool),
        ("pad_0018[3]", ctypes.c_char * 3),
        ("m_flGlowAlphaFunctionOfMaxVelocity", ctypes.c_float),
        ("m_flGlowAlphaMax", ctypes.c_float),
        ("m_flGlowPulseOverdrive", ctypes.c_float),
        ("m_bRenderWhenOccluded", ctypes.c_bool),
        ("m_bRenderWhenUnoccluded", ctypes.c_bool),
        ("m_bFullBloomRender", ctypes.c_bool),
        ("pad_002B[1]", ctypes.c_char),
        ("m_nFullBloomStencilTestValue", ctypes.c_int32),
        ("m_nRenderStyle", ctypes.c_int32),
        ("m_nSplitScreenSlot", ctypes.c_int32)
    ]

@dataclass
class ScreenSize:
    x = ctypes.windll.user32.GetSystemMetrics(0) - 1
    y = ctypes.windll.user32.GetSystemMetrics(1) - 1

@dataclass
class Vector3:
    x: float
    y: float
    z: float

@dataclass
class Vector2:
    x: float
    y: float

def to_angle(delta: Vector3):
    return Vector3(
        atan2(-delta.z, hypot(delta.x, delta.y)) * (180.0 / pi),
        atan2(delta.y, delta.x) * (180.0 / pi),
        0.0
    )

def calculate_angle(start_pos: Vector3, end_pos: Vector3, view_angle: Vector3):
    distance = Vector3(end_pos.x - start_pos.x, end_pos.y - start_pos.y, end_pos.z - start_pos.z)
    angle = to_angle(distance)
    return Vector3(angle.x - view_angle.x, angle.y - view_angle.y, angle.z - view_angle.z)

def clamp_angle(angle: Vector3):
    if (angle.x > 89.0): angle.x = 89.0
    elif (angle.x < -89.0): angle.x = -89.0

    if (angle.y > 180.0): angle.y = 180.0
    elif (angle.y < -180.0): angle.y = -180.0
    angle.z = 0.0

    return angle

def normalize_angle(angle: Vector3):
    if ( angle.x != angle.x or angle.y != angle.y or angle.z != angle.z ):
        return False
    
    if ( angle.x > 180.0 ): angle.x -= 360.0
    if ( angle.x < -180.0 ): angle.x += 360.0
    if ( angle.y > 180.0 ): angle.y -= 360.0
    if ( angle.y < -180.0 ): angle.y += 360.0
 
    return angle

def distance(start_point: Vector3, end_point: Vector3):
	distance = sqrt(
        (int(start_point.x) - int(end_point.x)) * (int(start_point.x) - int(end_point.x)) +
		(int(start_point.y) - int(end_point.y)) * (int(start_point.y) - int(end_point.y)) +
		(int(start_point.z) - int(end_point.z)) * (int(start_point.z) - int(end_point.z)))

	return int(abs(round(distance)))

def get_hash_of(file_name: str):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_random_string() -> None:
    chars = ['A',
    'B', 'C', 'D', 'E', 'F','G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'U', 'P', 'R', 'S', 'T', 'W', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f','g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'u', 'p', 'r', 's', 't', 'w', 'y', 'z',
    '1','2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#', '$', '%', '^', '&', '&', '(', ')', '-', '_', '=', '+']
    return ''.join(random.choice(chars) for _ in range(0, 15))

sky_list =[
    'cs_tibet',
    'embassy',
    'italy',
    'jungle',
    'nukeblank',
    'office',
    'sky_cs15_daylight01_hdr',
    'sky_cs15_daylight02_hdr',
    'sky_cs15_daylight03_hdr',
    'sky_cs15_daylight04_hdr',
    'sky_csgo_cloudy01',
    'sky_csgo_night02',
    'sky_csgo_night02b',
    'sky_day02_05',
    'sky_dust',
    'sky_lunacy',
    'sky_venice',
    'vertigo',
    'vertigoblue_hdr',
    'vietnam',
]

ranks_list =[
    'Unranked',
    "Silver I",
    "Silver II",
    "Silver III",
    "Silver IV",
    "Silver Elite",
    "Silver Elite Master",
    "Gold Nova I",
    "Gold Nova II",
    "Gold Nova III",
    "Gold Nova Master",
    "Master Guardian I",
    "Master Guardian II",
    "Master Guardian Elite",
    "Distinguished Master Guardian",
    "Legendary Eagle",
    "Legendary Eagle Master",
    "Supreme Master First Class",
    "The Global Elite",
]

gui_keys_list = {
    'LEFT MOUSE': 0x01,
    'RIGHT MOUSE': 0x02,
    'SCROLL': 0x04,
    'MOUSE 4': 0x05,
    'MOUSE 5': 0x06,
    'SHIFT': 0x10,
    'CTRL': 0x11,
    'LEFT SHIFT': 0xA0,
    'RIGHT SHIFT': 0xA1,
    'LEFT CONTROL': 0xA2,
    'RIGHT CONTROL': 0xA3,
    'NUMPAD0': 0x60,
    'NUMPAD1': 0x61,
    'NUMPAD2': 0x62,
    'NUMPAD3': 0x63,
    'NUMPAD4': 0x64,
    'NUMPAD5': 0x65,
    'NUMPAD6': 0x66,
    'NUMPAD7': 0x67,
    'NUMPAD8': 0x68,
    'NUMPAD9': 0x69,
    'A': 0x41, 
    'B': 0x42, 
    'C': 0x43, 
    'D': 0x44, 
    'E': 0x45, 
    'F': 0x46, 
    'G': 0x47, 
    'H': 0x48, 
    'I': 0x49, 
    'J': 0x4A, 
    'K': 0x4B, 
    'L': 0x4C, 
    'M': 0x4D, 
    'N': 0x4E, 
    'O': 0x4F, 
    'P': 0x50, 
    'Q': 0x51, 
    'R': 0x52, 
    'S': 0x53, 
    'T': 0x54, 
    'U': 0x55, 
    'V': 0x56, 
    'W': 0x57, 
    'X': 0x58, 
    'Y': 0x59, 
    'Z': 0x5A, 
}

bone_ids = {
    'HEAD': 8,
    'NECK': 7,
    'UPPER BODY': 6,
    'CENTER BODY': 5,
    'LOWER BODY': 0,
}

class Weapon(IntEnum):
    Desert_Eagle    = 1
    Dual_Berettas   = 2
    Five_SeveN      = 3
    Glock_18        = 4
    AK_47           = 7
    AUG             = 8
    AWP             = 9
    FAMAS           = 10
    G3SG1           = 11
    Galil_AR        = 13
    M249            = 14
    M4A4            = 16
    MAC_10          = 17
    P90             = 19
    MP5_SD          = 23
    UMP_45          = 24
    XM1014          = 25
    Bizon           = 26
    MAG_7           = 27
    Negev           = 28
    Sawed_Off       = 29
    Tec_9           = 30
    Zeus            = 31
    P2000           = 32
    MP7             = 33
    MP9             = 34
    Nova            = 35
    P250            = 36
    SCAR_20         = 38
    SG_553          = 39
    SSG_08          = 40
    Golden_Knife    = 41
    Knife           = 42
    Flashbang       = 43
    Explosive_Grenade= 44
    Smoke_Grenade   = 45
    Molotov         = 46
    Decoy_Grenade   = 47
    Incendiary_Grenade = 48
    C4              = 49
    Kevlar_Vest     = 50
    Kevlar_Helmet   = 51
    Defuse_Kit      = 55
    Rescue_Kit      = 56
    Medi_Shot       = 57
    Music_Kit       = 58
    T_knife         = 59
    M4A1_S          = 60
    USP_S           = 61
    CZ75_Auto       = 63
    R8_Revolver     = 64
    Bayonet         = 500
    Classic_Knife   = 503
    Flip_Knife      = 505
    Gut_Knife       = 506
    Karambit        = 507
    M9_Bayonet      = 508
    Huntsman_Knife  = 509
    Falchion_Knife  = 512
    Bowie_Knife     = 514
    Butterfly_Knife = 515
    Shadow_Daggers  = 516
    Paracord_Knife  = 517
    Survival_Knife  = 518
    Ursus_Knife     = 519
    Navaja_Knife    = 520
    Nomad_Knife     = 521
    Stiletto_Knife  = 522
    Talon_Knife     = 523
    Skeleton_Knife  = 525

class ClassId(IntEnum):
    CAI_BaseNPC     = 0
    CAK47           = 1
    CBaseAnimating  = 2
    CBaseAnimatingOverlay = 3
    CBaseAttributableItem = 4
    CBaseButton     = 5
    CBaseCombatCharacter = 6
    CBaseCombatWeapon = 7
    CBaseCSGrenade  = 8
    CBaseCSGrenadeProjectile = 9
    CBaseDoor       = 10
    CBaseEntity     = 11
    CBaseFlex       = 12
    CBaseGrenade    = 13
    CBaseParticleEntity = 14
    CBasePlayer     = 15
    CBasePropDoor   = 16
    CBaseTeamObjectiveResource = 17
    CBaseTempEntity = 18
    CBaseToggle     = 19
    CBaseTrigger    = 20
    CBaseViewModel  = 21
    CBaseVPhysicsTrigger = 22
    CBaseWeaponWorldModel = 23
    CBeam           = 24
    CBeamSpotlight  = 25
    CBoneFollower   = 26
    CBRC4Target     = 27
    CBreachCharge   = 28
    CBreachChargeProjectile = 29
    CBreakableProp  = 30
    CBreakableSurface = 31
    CBumpMine       = 32
    CBumpMineProjectile = 33
    CC4             = 34
    CCascadeLight   = 35
    CChicken        = 36
    CColorCorrection = 37
    CColorCorrectionVolume = 38
    CCSGameRulesProxy = 39
    CCSPlayer       = 40
    CCSPlayerResource = 41
    CCSRagdoll      = 42
    CCSTeam         = 43
    CDangerZone     = 44
    CDangerZoneController = 45
    CDEagle         = 46
    CDecoyGrenade   = 47
    CDecoyProjectile= 48
    CDrone          = 49
    CDronegun       = 50
    CDynamicLight   = 51
    CDynamicProp    = 52
    CEconEntity     = 53
    CEconWearable   = 54
    CEmbers         = 55
    CEntityDissolve = 56
    CEntityFlame    = 57
    CEntityFreezing = 58
    CEntityParticleTrail = 59
    CEnvAmbientLight     = 60
    CEnvDetailController = 61
    CEnvDOFController    = 62
    CEnvGasCanister      = 63
    CEnvParticleScript   = 64
    CEnvProjectedTexture = 65
    CEnvQuadraticBeam    = 66
    CEnvScreenEffect     = 67
    CEnvScreenOverlay    = 68
    CEnvTonemapController = 69
    CEnvWind            = 70
    CFEPlayerDecal      = 71
    CFireCrackerBlast   = 72
    CFireSmoke          = 73
    CFireTrail          = 74
    CFish               = 75
    CFists              = 76
    CFlashbang          = 77
    CFogController      = 78
    CFootstepControl    = 79
    CFunc_Dust          = 80
    CFunc_LOD           = 81
    CFuncAreaPortalWindow = 82
    CFuncBrush          = 83
    CFuncConveyor       = 84
    CFuncLadder         = 85
    CFuncMonitor        = 86
    CFuncMoveLinear     = 87
    CFuncOccluder       = 88
    CFuncReflectiveGlass = 89
    CFuncRotating       = 90
    CFuncSmokeVolume    = 91
    CFuncTrackTrain     = 92
    CGameRulesProxy     = 93
    CGrassBurn          = 94
    CHandleTest         = 95
    CHEGrenade          = 96
    CHostage            = 97
    CHostageCarriableProp = 98
    CIncendiaryGrenade    = 99
    CInferno            = 100
    CInfoLadderDismount = 101
    CInfoMapRegion      = 102
    CInfoOverlayAccessor= 103
    CItem_Healthshot    = 104
    CItemCash           = 105
    CItemDogtags        = 106
    CKnife              = 107
    CKnifeGG            = 108
    CLightGlow          = 109
    CMapVetoPickController = 110
    CMaterialModifyControl = 111
    CMelee              = 112
    CMolotovGrenade     = 113
    CMolotovProjectile  = 114
    CMovieDisplay       = 115
    CParadropChopper    = 116
    CParticleFire       = 117
    CParticlePerformanceMonitor = 118
    CParticleSystem     = 119
    CPhysBox            = 120
    CPhysBoxMultiplayer = 121
    CPhysicsProp        = 122
    CPhysicsPropMultiplayer = 123
    CPhysMagnet         = 124
    CPhysPropAmmoBox    = 125
    CPhysPropLootCrate  = 126
    CPhysPropRadarJammer= 127
    CPhysPropWeaponUpgrade= 128
    CPlantedC4          = 129
    CPlasma             = 130
    CPlayerPing         = 131
    CPlayerResource     = 132
    CPointCamera        = 133
    CPointCommentaryNode = 134
    CPointWorldText     = 135
    CPoseController     = 136
    CPostProcessController  = 137
    CPrecipitation      = 138
    CPrecipitationBlocker   = 139
    CPredictedViewModel = 140
    CProp_Hallucination = 141
    CPropCounter        = 142
    CPropDoorRotating   = 143
    CPropJeep           = 144
    CPropVehicleDriveable = 145
    CRagdollManager     = 146
    CRagdollProp        = 147
    CRagdollPropAttached= 148
    CRopeKeyframe       = 149
    CSCAR17             = 150
    CSceneEntity        = 151
    CSensorGrenade      = 152
    CSensorGrenadeProjectile= 153
    CShadowControl      = 154
    CSlideshowDisplay   = 155
    CSmokeGrenade       = 156
    CSmokeGrenadeProjectile = 157
    CSmokeStack         = 158
    CSnowball           = 159
    CSnowballPile       = 160
    CSnowballProjectile = 161
    CSpatialEntity      = 162
    CSpotlightEnd       = 163
    CSprite             = 164
    CSpriteOriented     = 165
    CSpriteTrail        = 166
    CStatueProp         = 167
    CSteamJet           = 168
    CSun                = 169
    CSunlightShadowControl = 170
    CSurvivalSpawnChopper = 171
    CTablet             = 172
    CTeam               = 173
    CTeamplayRoundBasedRulesProxy = 174
    CTEArmorRicochet    = 175
    CTEBaseBeam         = 176
    CTEBeamEntPoint     = 177
    CTEBeamEnts         = 178
    CTEBeamFollow       = 179
    CTEBeamLaser        = 180
    CTEBeamPoints       = 181
    CTEBeamRing         = 182
    CTEBeamRingPoint    = 183
    CTEBeamSpline       = 184
    CTEBloodSprite      = 185
    CTEBloodStream      = 186
    CTEBreakModel       = 187
    CTEBSPDecal         = 188
    CTEBubbles          = 189
    CTEBubbleTrail      = 190
    CTEClientProjectile = 191
    CTEDecal            = 192
    CTEDust             = 193
    CTEDynamicLight     = 194
    CTEEffectDispatch   = 195
    CTEEnergySplash     = 196
    CTEExplosion        = 197
    CTEFireBullets      = 198
    CTEFizz             = 199
    CTEFootprintDecal   = 200
    CTEFoundryHelpers   = 201
    CTEGaussExplosion   = 202
    CTEGlowSprite       = 203
    CTEImpact           = 204
    CTEKillPlayerAttachments = 205
    CTELargeFunnel      = 206
    CTEMetalSparks      = 207
    CTEMuzzleFlash      = 208
    CTEParticleSystem   = 209
    CTEPhysicsProp      = 210
    CTEPlantBomb        = 211
    CTEPlayerAnimEvent  = 212
    CTEPlayerDecal      = 213
    CTEProjectedDecal   = 214
    CTERadioIcon        = 215
    CTEShatterSurface   = 216
    CTEShowLine         = 217
    CTesla              = 218
    CTESmoke            = 219
    CTESparks           = 220
    CTESprite           = 221
    CTESpriteSpray      = 222
    CTest_ProxyToggle_Networkable = 223
    CTestTraceline      = 224
    CTEWorldDecal       = 225
    CTriggerPlayerMovement = 226
    CTriggerSoundOperator = 227
    CVGuiScreen         = 228
    CVoteController     = 229
    CWaterBullet        = 230
    CWaterLODControl    = 231
    CWeaponAug          = 232
    CWeaponAWP          = 233
    CWeaponBaseItem     = 234
    CWeaponBizon        = 235
    CWeaponCSBase       = 236
    CWeaponCSBaseGun    = 237
    CWeaponCycler       = 238
    CWeaponElite        = 239
    CWeaponFamas        = 240
    CWeaponFiveSeven    = 241
    CWeaponG3SG1        = 242
    CWeaponGalil        = 243
    CWeaponGalilAR      = 244
    CWeaponGlock        = 245
    CWeaponHKP2000      = 246
    CWeaponM249         = 247
    CWeaponM3           = 248
    CWeaponM4A1         = 249
    CWeaponMAC10        = 250
    CWeaponMag7         = 251
    CWeaponMP5Navy      = 252
    CWeaponMP7          = 253
    CWeaponMP9          = 254
    CWeaponNegev        = 255
    CWeaponNOVA         = 256
    CWeaponP228         = 257
    CWeaponP250         = 258
    CWeaponP90          = 259
    CWeaponSawedoff     = 260
    CWeaponSCAR20       = 261
    CWeaponScout        = 262
    CWeaponSG550        = 263
    CWeaponSG552        = 264
    CWeaponSG556        = 265
    CWeaponShield       = 266
    CWeaponSSG08        = 267
    CWeaponTaser        = 268
    CWeaponTec9         = 269
    CWeaponTMP          = 270
    CWeaponUMP45        = 271
    CWeaponUSP          = 272
    CWeaponXM1014       = 273
    CWeaponZoneRepulsor = 274
    CWorld              = 275
    CWorldVguiText      = 276
    DustTrail           = 277
    MovieExplosion      = 278
    ParticleSmokeGrenade= 279
    RocketTrail         = 280
    SmokeTrail          = 281
    SporeExplosion      = 282
    SporeTrail          = 283

def class_id_gun(class_id):
    if (class_id == ClassId.CAK47 or class_id == ClassId.CSCAR17 or class_id == ClassId.CWeaponAug
        or class_id == ClassId.CWeaponBizon or class_id == ClassId.CWeaponElite or class_id == ClassId.CWeaponFamas
        or class_id == ClassId.CWeaponFiveSeven or class_id == ClassId.CDEagle or class_id == ClassId.CWeaponM249
        or class_id == ClassId.CWeaponG3SG1 or class_id == ClassId.CWeaponGalil or class_id == ClassId.CWeaponGalilAR
        or class_id == ClassId.CWeaponGlock or class_id == ClassId.CWeaponHKP2000  or class_id == ClassId.CWeaponM3
        or class_id == ClassId.CWeaponM4A1 or class_id == ClassId.CWeaponMAC10 or class_id == ClassId.CWeaponMag7
        or class_id == ClassId.CWeaponMP5Navy or class_id == ClassId.CWeaponMP7 or class_id == ClassId.CWeaponMP9
        or class_id == ClassId.CWeaponNegev or class_id == ClassId.CWeaponNOVA or class_id == ClassId.CWeaponP228
        or class_id == ClassId.CWeaponP250 or class_id == ClassId.CWeaponP90 or class_id == ClassId.CWeaponSawedoff
        or class_id == ClassId.CWeaponSCAR20 or class_id == ClassId.CWeaponScout or class_id == ClassId.CWeaponSG550
        or class_id == ClassId.CWeaponSG552 or class_id == ClassId.CWeaponSG556 or class_id == ClassId.CWeaponShield
        or class_id == ClassId.CWeaponSSG08 or class_id == ClassId.CWeaponTaser or class_id == ClassId.CWeaponUSP
        or class_id == ClassId.CWeaponTec9 or class_id == ClassId.CWeaponTMP or class_id == ClassId.CWeaponUMP45
        or class_id == ClassId.CWeaponXM1014 or class_id == ClassId.CWeaponAWP):
        return True
    else:
        return False

def class_id_grenade(class_id):
    if (class_id == ClassId.CDecoyGrenade or class_id == ClassId.CDecoyProjectile
        or class_id == ClassId.CMolotovProjectile or class_id == ClassId.CMolotovGrenade
        or class_id == ClassId.CHEGrenade or class_id == ClassId.CIncendiaryGrenade 
        or class_id == ClassId.CSmokeGrenade or class_id == ClassId.ParticleSmokeGrenade
        or class_id == ClassId.CSmokeGrenadeProjectile or class_id == ClassId.CFlashbang
        or class_id == ClassId.CBaseCSGrenadeProjectile):
        return True
    else:
        return False

def class_id_c4(class_id):
    if (class_id == ClassId.CC4 or class_id == ClassId.CPlantedC4):
        return True
    else:
        return False

def weapon_knife(weapon):
    if (weapon == Weapon.Knife or weapon == Weapon.T_knife or weapon == Weapon.Bayonet
        or weapon == Weapon.Flip_Knife or weapon == Weapon.Gut_Knife or weapon == Weapon.Paracord_Knife
        or weapon == Weapon.Karambit or weapon == Weapon.M9_Bayonet or weapon == Weapon.Huntsman_Knife
        or weapon == Weapon.Falchion_Knife or weapon == Weapon.Bowie_Knife or weapon == Weapon.Stiletto_Knife
        or weapon == Weapon.Butterfly_Knife or weapon == Weapon.Shadow_Daggers or weapon == Weapon.Classic_Knife 
        or weapon == Weapon.Survival_Knife or weapon == Weapon.Ursus_Knife
        or weapon == Weapon.Navaja_Knife or weapon == Weapon.Nomad_Knife
        or weapon == Weapon.Talon_Knife or weapon == Weapon.Skeleton_Knife):
        return True
    else:
        return False

def weapon_rifle(weapon):
    if (weapon == Weapon.AK_47 or weapon == Weapon.AUG or weapon == Weapon.FAMAS 
        or weapon == Weapon.Galil_AR or weapon == Weapon.SG_553
        or weapon == Weapon.M4A1_S or weapon == Weapon.M4A4):
        return True
    else:
        return False

def weapon_pistol(weapon):
    if (weapon == Weapon.Desert_Eagle or weapon == Weapon.Dual_Berettas or weapon == Weapon.Five_SeveN
        or weapon == Weapon.Glock_18 or weapon == Weapon.Tec_9 or weapon == Weapon.P2000
        or weapon == Weapon.P250 or weapon == Weapon.USP_S or weapon == Weapon.R8_Revolver
        or weapon == Weapon.CZ75_Auto):
        return True
    else:
        return False

def weapon_grenade(weapon):
    if (weapon == Weapon.Flashbang or weapon == Weapon.Explosive_Grenade or weapon == Weapon.Smoke_Grenade
        or weapon == Weapon.Molotov or weapon == Weapon.Decoy_Grenade or weapon == Weapon.C4):
        return True
    else:
        return False

def weapon_sniper(weapon):
    if (weapon == Weapon.AWP or weapon == Weapon.G3SG1 or weapon == Weapon.SCAR_20 or weapon == Weapon.SSG_08):
        return True
    else:
        return False

def weapon_smg(weapon):
    if (weapon == Weapon.MAC_10 or weapon == Weapon.MP7 or weapon == Weapon.UMP_45 or weapon == Weapon.P90
        or weapon == Weapon.Bizon or weapon == Weapon.MP5_SD or weapon == Weapon.MP9):
        return True
    else:
        return False

def weapon_heavy(weapon):
    if (weapon == Weapon.Nova or weapon == Weapon.XM1014 or weapon == Weapon.Sawed_Off or weapon == Weapon.M249
        or weapon == Weapon.Negev or weapon == Weapon.MAG_7):
        return True
    else:
        return False
