from enum import IntEnum
from ctypes import *
from dataclasses import dataclass

player_info_buffer = []

@dataclass
class ScreenSize:
    x = windll.user32.GetSystemMetrics(0)
    y = windll.user32.GetSystemMetrics(1)

@dataclass
class Vector3:
    x: float
    y: float
    z: float

@dataclass
class Vector2:
    x: float
    y: float

def w2s(pos: Vector3, matrix):
    z = pos.x * matrix[12] + pos.y * matrix[13] + pos.z * matrix[14] + matrix[15]
    if z < 0.1:
        return None

    x = pos.x * matrix[0] + pos.y * matrix[1] + pos.z * matrix[2] + matrix[3]
    y = pos.x * matrix[4] + pos.y * matrix[5] + pos.z * matrix[6] + matrix[7]

    xx = x / z
    yy = y / z

    _x = (1920 / 2 * xx) + (xx + 1920 / 2)
    _y = (1090 / 2 * yy) + (yy + 1080 / 2)

    return [_x, _y]

def clamp_angle(angle: Vector3):
    if (angle.x > 89.0): angle.x = 89.0
    elif (angle.x < -89.0): angle.x = -89.0

    if (angle.y > 180.0): angle.y = 180.0
    elif (angle.y < -180.0): angle.y = -180.0
    angle.z = 0.0

    return angle

def normalize_vector(angle: Vector3):
    if ( angle.x != angle.x or angle.y != angle.y or angle.z != angle.z ):
        return False
    
    if ( angle.x > 180 ): angle.x -= 360.0
    if ( angle.x < -180 ): angle.x += 360.0
    if ( angle.y > 180.0 ): angle.y -= 360.0
    if ( angle.y < -180.0 ): angle.y += 360.0
 
    return angle

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

class Weapon(IntEnum):
    Desert_Eagle = 1
    Dual_Berettas = 2
    Five_SeveN = 3
    Glock_18 = 4
    AK_47 = 7
    AUG = 8
    AWP = 9
    FAMAS = 10
    G3SG1 = 11
    Galil_AR = 13
    M249 = 14
    M4A4 = 16
    MAC_10 = 17
    P90 = 19
    MP5_SD = 23
    UMP_45 = 24
    XM1014 = 25
    Bizon = 26
    MAG_7 = 27
    Negev = 28
    Sawed_Off = 29
    Tec_9 = 30
    Zeus = 31
    P2000 = 32
    MP7 = 33
    MP9 = 34
    Nova = 35
    P250 = 36
    SCAR_20 = 38
    SG_553 = 39
    SSG_08 = 40
    Golden_Knife = 41
    Knife = 42
    Flashbang = 43
    Explosive_Grenade = 44
    Smoke_Grenade = 45
    Molotov = 46
    Decoy_Grenade = 47
    Incendiary_Grenade = 48
    C4 = 49
    Kevlar_Vest = 50
    Kevlar_Helmet = 51
    Defuse_Kit = 55
    Rescue_Kit = 56
    Medi_Shot = 57
    Music_Kit = 58
    T_knife = 59
    M4A1_S = 60
    USP_S = 61
    CZ75_Auto = 63
    R8_Revolver = 64
    Bayonet = 500
    Classic_Knife = 503
    Flip_Knife = 505
    Gut_Knife = 506
    Karambit = 507
    M9_Bayonet = 508
    Huntsman_Knife = 509
    Falchion_Knife = 512
    Bowie_Knife = 514
    Butterfly_Knife = 515
    Shadow_Daggers = 516
    Paracord_Knife = 517
    Survival_Knife = 518
    Ursus_Knife = 519
    Navaja_Knife = 520
    Nomad_Knife = 521
    Stiletto_Knife = 522
    Talon_Knife = 523
    Skeleton_Knife = 525

class ClassId(IntEnum):
    CAI_BaseNPC = 0,
    CAK47 = 1,
    CBaseAnimating = 2,
    CBaseAnimatingOverlay = 3,
    CBaseAttributableItem = 4,
    CBaseButton = 5,
    CBaseCombatCharacter = 6,
    CBaseCombatWeapon = 7,
    CBaseCSGrenade = 8,
    CBaseCSGrenadeProjectile = 9,
    CBaseDoor = 10,
    CBaseEntity = 11,
    CBaseFlex = 12,
    CBaseGrenade = 13,
    CBaseParticleEntity = 14,
    CBasePlayer = 15,
    CBasePropDoor = 16,
    CBaseTeamObjectiveResource = 17,
    CBaseTempEntity = 18,
    CBaseToggle = 19,
    CBaseTrigger = 20,
    CBaseViewModel = 21,
    CBaseVPhysicsTrigger = 22,
    CBaseWeaponWorldModel = 23,
    CBeam = 24,
    CBeamSpotlight = 25,
    CBoneFollower = 26,
    CBRC4Target = 27,
    CBreachCharge = 28,
    CBreachChargeProjectile = 29,
    CBreakableProp = 30,
    CBreakableSurface = 31,
    CBumpMine = 32,
    CBumpMineProjectile = 33,
    CC4 = 34,
    CCascadeLight = 35,
    CChicken = 36,
    CColorCorrection = 37,
    CColorCorrectionVolume = 38,
    CCSGameRulesProxy = 39,
    CCSPlayer = 40,
    CCSPlayerResource = 41,
    CCSRagdoll = 42,
    CCSTeam = 43,
    CDangerZone = 44,
    CDangerZoneController = 45,
    CDEagle = 46,
    CDecoyGrenade = 47,
    CDecoyProjectile = 48,
    CDrone = 49,
    CDronegun = 50,
    CDynamicLight = 51,
    CDynamicProp = 52,
    CEconEntity = 53,
    CEconWearable = 54,
    CEmbers = 55,
    CEntityDissolve = 56,
    CEntityFlame = 57,
    CEntityFreezing = 58,
    CEntityParticleTrail = 59,
    CEnvAmbientLight = 60,
    CEnvDetailController = 61,
    CEnvDOFController = 62,
    CEnvGasCanister = 63,
    CEnvParticleScript = 64,
    CEnvProjectedTexture = 65,
    CEnvQuadraticBeam = 66,
    CEnvScreenEffect = 67,
    CEnvScreenOverlay = 68,
    CEnvTonemapController = 69,
    CEnvWind = 70,
    CFEPlayerDecal = 71,
    CFireCrackerBlast = 72,
    CFireSmoke = 73,
    CFireTrail = 74,
    CFish = 75,
    CFists = 76,
    CFlashbang = 77,
    CFogController = 78,
    CFootstepControl = 79,
    CFunc_Dust = 80,
    CFunc_LOD = 81,
    CFuncAreaPortalWindow = 82,
    CFuncBrush = 83,
    CFuncConveyor = 84,
    CFuncLadder = 85,
    CFuncMonitor = 86,
    CFuncMoveLinear = 87,
    CFuncOccluder = 88,
    CFuncReflectiveGlass = 89,
    CFuncRotating = 90,
    CFuncSmokeVolume = 91,
    CFuncTrackTrain = 92,
    CGameRulesProxy = 93,
    CGrassBurn = 94,
    CHandleTest = 95,
    CHEGrenade = 96,
    CHostage = 97,
    CHostageCarriableProp = 98,
    CIncendiaryGrenade = 99,
    CInferno = 100,
    CInfoLadderDismount = 101,
    CInfoMapRegion = 102,
    CInfoOverlayAccessor = 103,
    CItem_Healthshot = 104,
    CItemCash = 105,
    CItemDogtags = 106,
    CKnife = 107,
    CKnifeGG = 108,
    CLightGlow = 109,
    CMapVetoPickController = 110,
    CMaterialModifyControl = 111,
    CMelee = 112,
    CMolotovGrenade = 113,
    CMolotovProjectile = 114,
    CMovieDisplay = 115,
    CParadropChopper = 116,
    CParticleFire = 117,
    CParticlePerformanceMonitor = 118,
    CParticleSystem = 119,
    CPhysBox = 120,
    CPhysBoxMultiplayer = 121,
    CPhysicsProp = 122,
    CPhysicsPropMultiplayer = 123,
    CPhysMagnet = 124,
    CPhysPropAmmoBox = 125,
    CPhysPropLootCrate = 126,
    CPhysPropRadarJammer = 127,
    CPhysPropWeaponUpgrade = 128,
    CPlantedC4 = 129,
    CPlasma = 130,
    CPlayerPing = 131,
    CPlayerResource = 132,
    CPointCamera = 133,
    CPointCommentaryNode = 134,
    CPointWorldText = 135,
    CPoseController = 136,
    CPostProcessController = 137,
    CPrecipitation = 138,
    CPrecipitationBlocker = 139,
    CPredictedViewModel = 140,
    CProp_Hallucination = 141,
    CPropCounter = 142,
    CPropDoorRotating = 143,
    CPropJeep = 144,
    CPropVehicleDriveable = 145,
    CRagdollManager = 146,
    CRagdollProp = 147,
    CRagdollPropAttached = 148,
    CRopeKeyframe = 149,
    CSCAR17 = 150,
    CSceneEntity = 151,
    CSensorGrenade = 152,
    CSensorGrenadeProjectile = 153,
    CShadowControl = 154,
    CSlideshowDisplay = 155,
    CSmokeGrenade = 156,
    CSmokeGrenadeProjectile = 157,
    CSmokeStack = 158,
    CSnowball = 159,
    CSnowballPile = 160,
    CSnowballProjectile = 161,
    CSpatialEntity = 162,
    CSpotlightEnd = 163,
    CSprite = 164,
    CSpriteOriented = 165,
    CSpriteTrail = 166,
    CStatueProp = 167,
    CSteamJet = 168,
    CSun = 169,
    CSunlightShadowControl = 170,
    CSurvivalSpawnChopper = 171,
    CTablet = 172,
    CTeam = 173,
    CTeamplayRoundBasedRulesProxy = 174,
    CTEArmorRicochet = 175,
    CTEBaseBeam = 176,
    CTEBeamEntPoint = 177,
    CTEBeamEnts = 178,
    CTEBeamFollow = 179,
    CTEBeamLaser = 180,
    CTEBeamPoints = 181,
    CTEBeamRing = 182,
    CTEBeamRingPoint = 183,
    CTEBeamSpline = 184,
    CTEBloodSprite = 185,
    CTEBloodStream = 186,
    CTEBreakModel = 187,
    CTEBSPDecal = 188,
    CTEBubbles = 189,
    CTEBubbleTrail = 190,
    CTEClientProjectile = 191,
    CTEDecal = 192,
    CTEDust = 193,
    CTEDynamicLight = 194,
    CTEEffectDispatch = 195,
    CTEEnergySplash = 196,
    CTEExplosion = 197,
    CTEFireBullets = 198,
    CTEFizz = 199,
    CTEFootprintDecal = 200,
    CTEFoundryHelpers = 201,
    CTEGaussExplosion = 202,
    CTEGlowSprite = 203,
    CTEImpact = 204,
    CTEKillPlayerAttachments = 205,
    CTELargeFunnel = 206,
    CTEMetalSparks = 207,
    CTEMuzzleFlash = 208,
    CTEParticleSystem = 209,
    CTEPhysicsProp = 210,
    CTEPlantBomb = 211,
    CTEPlayerAnimEvent = 212,
    CTEPlayerDecal = 213,
    CTEProjectedDecal = 214,
    CTERadioIcon = 215,
    CTEShatterSurface = 216,
    CTEShowLine = 217,
    CTesla = 218,
    CTESmoke = 219,
    CTESparks = 220,
    CTESprite = 221,
    CTESpriteSpray = 222,
    CTest_ProxyToggle_Networkable = 223,
    CTestTraceline = 224,
    CTEWorldDecal = 225,
    CTriggerPlayerMovement = 226,
    CTriggerSoundOperator = 227,
    CVGuiScreen = 228,
    CVoteController = 229,
    CWaterBullet = 230,
    CWaterLODControl = 231,
    CWeaponAug = 232,
    CWeaponAWP = 233,
    CWeaponBaseItem = 234,
    CWeaponBizon = 235,
    CWeaponCSBase = 236,
    CWeaponCSBaseGun = 237,
    CWeaponCycler = 238,
    CWeaponElite = 239,
    CWeaponFamas = 240,
    CWeaponFiveSeven = 241,
    CWeaponG3SG1 = 242,
    CWeaponGalil = 243,
    CWeaponGalilAR = 244,
    CWeaponGlock = 245,
    CWeaponHKP2000 = 246,
    CWeaponM249 = 247,
    CWeaponM3 = 248,
    CWeaponM4A1 = 249,
    CWeaponMAC10 = 250,
    CWeaponMag7 = 251,
    CWeaponMP5Navy = 252,
    CWeaponMP7 = 253,
    CWeaponMP9 = 254,
    CWeaponNegev = 255,
    CWeaponNOVA = 256,
    CWeaponP228 = 257,
    CWeaponP250 = 258,
    CWeaponP90 = 259,
    CWeaponSawedoff = 260,
    CWeaponSCAR20 = 261,
    CWeaponScout = 262,
    CWeaponSG550 = 263,
    CWeaponSG552 = 264,
    CWeaponSG556 = 265,
    CWeaponShield = 266,
    CWeaponSSG08 = 267,
    CWeaponTaser = 268,
    CWeaponTec9 = 269,
    CWeaponTMP = 270,
    CWeaponUMP45 = 271,
    CWeaponUSP = 272,
    CWeaponXM1014 = 273,
    CWeaponZoneRepulsor = 274,
    CWorld = 275,
    CWorldVguiText = 276,
    DustTrail = 277,
    MovieExplosion = 278,
    ParticleSmokeGrenade = 279,
    RocketTrail = 280,
    SmokeTrail = 281,
    SporeExplosion = 282,
    SporeTrail = 283,

def class_id_gun(classID):
    if (classID == ClassId.CAK47 or classID == ClassId.CSCAR17 or classID == ClassId.CWeaponAug
    or classID == ClassId.CWeaponBizon or classID == ClassId.CWeaponElite or classID == ClassId.CWeaponFamas
    or classID == ClassId.CWeaponFiveSeven or classID == ClassId.CDEagle or classID == ClassId.CWeaponM249
    or classID == ClassId.CWeaponG3SG1 or classID == ClassId.CWeaponGalil or classID == ClassId.CWeaponGalilAR
    or classID == ClassId.CWeaponGlock or classID == ClassId.CWeaponHKP2000  or classID == ClassId.CWeaponM3
    or classID == ClassId.CWeaponM4A1 or classID == ClassId.CWeaponMAC10 or classID == ClassId.CWeaponMag7
    or classID == ClassId.CWeaponMP5Navy or classID == ClassId.CWeaponMP7 or classID == ClassId.CWeaponMP9
    or classID == ClassId.CWeaponNegev or classID == ClassId.CWeaponNOVA or classID == ClassId.CWeaponP228
    or classID == ClassId.CWeaponP250 or classID == ClassId.CWeaponP90 or classID == ClassId.CWeaponSawedoff
    or classID == ClassId.CWeaponSCAR20 or classID == ClassId.CWeaponScout or classID == ClassId.CWeaponSG550
    or classID == ClassId.CWeaponSG552 or classID == ClassId.CWeaponSG556 or classID == ClassId.CWeaponShield
    or classID == ClassId.CWeaponSSG08 or classID == ClassId.CWeaponTaser or classID == ClassId.CWeaponUSP
    or classID == ClassId.CWeaponTec9 or classID == ClassId.CWeaponTMP or classID == ClassId.CWeaponUMP45
    or classID == ClassId.CWeaponXM1014 or classID == ClassId.CWeaponAWP):
        return True
    else:
        return False

def class_id_grenade(classID):
    if (classID == ClassId.CDecoyGrenade or classID == ClassId.CDecoyProjectile
    or classID == ClassId.CMolotovProjectile or classID == ClassId.CMolotovGrenade
    or classID == ClassId.CHEGrenade or classID == ClassId.CIncendiaryGrenade 
    or classID == ClassId.CSmokeGrenade or classID == ClassId.ParticleSmokeGrenade
    or classID == ClassId.CSmokeGrenadeProjectile or classID == ClassId.CFlashbang):
        return True
    else:
        return False

def class_id_c4(classID):
    if (classID == ClassId.CC4 or classID == ClassId.CPlantedC4):
        return True
    else:
        return False

def weapon_knife(weapon):
    if (weapon == Weapon.Knife or weapon == Weapon.Bayonet or weapon == Weapon.Classic_Knife 
    or weapon == Weapon.Flip_Knife or weapon == Weapon.Gut_Knife or weapon == Weapon.Paracord_Knife
    or weapon == Weapon.Karambit or weapon == Weapon.M9_Bayonet or weapon == Weapon.Huntsman_Knife
    or weapon == Weapon.Falchion_Knife or weapon == Weapon.Bowie_Knife or weapon == Weapon.Stiletto_Knife
    or weapon == Weapon.Butterfly_Knife or weapon == Weapon.Shadow_Daggers
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