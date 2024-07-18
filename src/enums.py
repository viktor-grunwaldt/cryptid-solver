from enum import Enum
from typing import Optional


class Biome(Enum):
    DESERT = 0
    WATER = 1
    MOUNTAIN = 2
    FOREST = 3
    SWAMP = 4

    @staticmethod
    def from_char(c: str):
        return CHAR_TO_BIOME.get(c)

    def to_char(self) -> str:
        return BIOME_TO_CHAR[self]

    def get_color(self) -> tuple[int, int, int]:
        return BIOME_COLORS_DICT[self]


class Territory(Enum):
    COUGAR = 0
    BEAR = 1
    BOTH = 2

    @staticmethod
    def from_char(c: str):
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


class Clue(Enum):
    def __init__(self, clue_type: ClueType, data: tuple):
        self.clue_type: ClueType
        self.data: (
            tuple[Biome, Biome] | Biome | Territory | StructureColor | StructureType
        )


class StructureColor(Enum):
    BLACK = 0
    BLUE = 1
    WHITE = 2
    GREEN = 3


class StructureType(Enum):
    STONE = 0
    SHACK = 1


class PlayerColor(Enum):
    RED = 0
    ORANGE = 1
    CYAN = 2
    LIGHT_BLUE = 3
    PURPLE = 4


class Structure:
    def __init__(self, color: StructureColor, stype: StructureType):
        self.color = color
        self.type = stype
        self.name = f"{color}-{stype}"


class Piece:
    def __init__(self, color: PlayerColor, ptype: PieceType):
        self.color = color
        self.type = ptype
        self.name = f"{color}-{ptype}"


class Field:
    def __init__(
        self,
        biome: Biome,
        territory: Optional[Territory],
        structure: Optional[Structure],
        pieces: Optional[list[Piece]],
    ):
        self.biome = biome
        self.territory = territory
        self.structure = structure
        self.pieces = []


BIOME_TO_CHAR = {
    Biome.DESERT: "d",
    Biome.WATER: "w",
    Biome.MOUNTAIN: "m",
    Biome.FOREST: "f",
    Biome.SWAMP: "s",
}

CHAR_TO_BIOME = {v: k for k, v in BIOME_TO_CHAR.items()}
BIOME_COLORS_DICT = {
    Biome.WATER: (97, 150, 202),  # blue for water
    Biome.DESERT: (255, 212, 81),  # sandy brown for desert
    Biome.MOUNTAIN: (185, 185, 185),  # brown for mountain
    Biome.SWAMP: (117, 87, 115),  # dark purple for swamp
    Biome.FOREST: (113, 173, 103),  # dark green for forest
}

ALL_BIOMES = tuple(CHAR_TO_BIOME.keys())

STRUCT_COLORS_DICT = {
    StructureColor.BLUE: (0, 0, 255),  # blue
    StructureColor.WHITE: (255, 255, 255),  # white
    StructureColor.GREEN: (0, 128, 0),  # green
    StructureColor.BLACK: (0, 0, 0),  # black
}

STRUCT_COLORS = tuple(STRUCT_COLORS_DICT.keys())

PLAYER_COLORS = (
    PlayerColor.RED,
    PlayerColor.ORANGE,
    PlayerColor.CYAN,
    PlayerColor.LIGHT_BLUE,
    PlayerColor.PURPLE,
)


colors = BIOME_COLORS_DICT | STRUCT_COLORS_DICT
bundle_colors = [
    (223, 66, 59),  # Red
    (253, 201, 27),  # Orange
    (52, 199, 206),  # Cyan
    (174, 228, 255),  # Light blue
    (126, 85, 207),  # Violet
]
structure_bundle_colors = tuple(STRUCT_COLORS_DICT.values())
