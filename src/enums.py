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
                cur = Biome.DESERT
            case "w":
                cur = Biome.WATER
            case "m":
                cur = Biome.MOUNTAIN
            case "f":
                cur = Biome.FOREST
            case "s":
                cur = Biome.SWAMP
            case _:
                cur = None
        return cur

class Territory(Enum):
    COUGAR = 0
    BEAR = 1
    BOTH = 2


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
