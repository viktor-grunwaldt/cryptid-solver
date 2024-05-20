from enum import Enum
from typing import Optional


class Biome(Enum):
    DESERT = 0
    WATER = 1
    MOUNTAIN = 2
    FOREST = 3
    SWAMP = 4

    def from_char(c: str):
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

    def to_char(self) -> str:
        match self:
            case Biome.DESERT:
                return "d"
            case Biome.FOREST:
                return "f"
            case Biome.MOUNTAIN:
                return "m"
            case Biome.SWAMP:
                return "s"
            case Biome.WATER:
                return "w"
            case _:
                raise Exception("Not reachable!")


class Territory(Enum):
    COUGAR = 0
    BEAR = 1
    BOTH = 2

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
    color: PlayerColor
    type: PieceType


class Field:
    def __init__(
        self,
        biome: Biome,
        territory: Territory,
        structure: Optional[Structure],
        pieces: Optional[list[Piece]],
    ):
        self.biome = biome
        self.territory = territory
        self.structure = structure
        self.pieces = []


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

PLAYER_COLORS = (
    PlayerColor.RED,
    PlayerColor.ORANGE,
    PlayerColor.CYAN,
    PlayerColor.LIGHT_BLUE,
    PlayerColor.PURPLE,
)
colors = {
    Biome.WATER: (97, 150, 202),  # blue for water
    Biome.DESERT: (255, 212, 81),  # sandy brown for desert
    Biome.MOUNTAIN: (185, 185, 185),  # brown for mountain
    Biome.SWAMP: (117, 87, 115),  # dark purple for swamp
    Biome.FOREST: (113, 173, 103),  # dark green for forest
    StructureColor.BLACK: (0, 0, 0),  # black
    StructureColor.BLUE: (0, 0, 255),  # blue
    StructureColor.WHITE: (255, 255, 255),  # white
    StructureColor.GREEN: (0, 128, 0),  # green
}
bundle_colors = [
    (223, 66, 59),  # Red
    (253, 201, 27),  # Orange
    (52, 199, 206),  # Cyan
    (174, 228, 255),  # Light blue
    (126, 85, 207),  # Violet
]
structure_bundle_colors = [
    (0, 0, 255),  # Blue
    (255, 255, 255),  # White
    (0, 128, 0),  # Green
    (0, 0, 0),  # Black
]
