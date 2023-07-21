from enum import Enum


class Color(Enum):
    PURPLE = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    ORANGE = 4


class Biome(Enum):
    DESERT = 0
    WATER = 1
    MOUNTAIN = 2
    FOREST = 3
    SWAMP = 4

    def from_char(c:str):
        match c:
            case "d":
                return Biome.DESERT
            case "w":
                return Biome.WATER
            case "m":
                return Biome.MOUNTAIN
            case "f":
                return Biome.FOREST
            case "s":
                return Biome.SWAMP
            case _:
                return None


class Territory(Enum):
    COUGAR = 0
    BEAR = 1
    BOTH = 2

    def from_char(c:str):
        match c:
            case "B":
                return Territory.BEAR
            case "C":
                return Territory.COUGAR
            case _:
                return None


class PieceType(Enum):
    CUBE = 0
    DISK = 1


class ClueType(Enum):
    TWO_TERRAINS = 0
    WITHIN_ONE = 1
    WITHIN_TWO = 2
    WITHIN_THREE = 3


class StructureColor(Enum):
    BLACK = 0
    BLUE = 1
    WHITE = 2
    GREEN = 3


class StructureType(Enum):
    STONE = 0
    SHACK = 1


ALL_BIOMES = (
    Biome.DESERT,
    Biome.FOREST,
    Biome.MOUNTAIN,
    Biome.SWAMP,
    Biome.WATER,
)

STRUCT_COLORS = (
    StructureColor.BLACK,
    StructureColor.BLUE,
    StructureColor.WHITE,
    StructureColor.GREEN,
)
