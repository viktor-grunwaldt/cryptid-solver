from enum import Enum
from typing import Optional, List, Annotated
from attrs import define
from itertools import pairwise, combinations
from more_itertools import flatten
import unittest


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


ALL_BIOMES = (
    Biome.DESERT,
    Biome.FOREST,
    Biome.MOUNTAIN,
    Biome.SWAMP,
    Biome.WATER,
)


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


STRUCT_COLORS = (
    StructureColor.BLACK,
    StructureColor.BLUE,
    StructureColor.WHITE,
    StructureColor.GREEN,
)


class StructureType(Enum):
    STONE = 0
    SHACK = 1


@define
class Structure:
    color: StructureColor
    type: StructureType


class Clue:
    clue_type: ClueType
    data: tuple[Biome, Biome] | Biome | Territory | StructureColor | StructureType


def generate_all_clues() -> list[Clue]:
    within_two = (StructureType.SHACK, StructureType.STONE, Territory.BEAR, Territory.COUGAR)
    clues = [Clue(ClueType.TWO_TERRAINS, pair) for pair in combinations(ALL_BIOMES, 2)]
    clues += [Clue(ClueType.WITHIN_ONE, e) for e in (ALL_BIOMES + Territory.BOTH)]
    clues += [Clue(ClueType.WITHIN_TWO, e) for e in within_two]
    clues += [Clue(ClueType.WITHIN_THREE, e) for e in STRUCT_COLORS]
    return clues


@define
class Piece:
    color: Color
    type: PieceType


@define
class Field:
    biome: Biome
    territory: Optional[Territory]
    structure: Optional[Structure]
    piece: Optional[list[Piece]]


Grid = Annotated[List[List[Optional["Field"]]], "TypeAlias for a grid of optional 'Field' objects"]
Point = tuple[int, int]
# Grid = TypeAlias(List[List[Optional["Field"]]])

# there are 6 tiles numbered 1 to 6 which are arranged into a 3x2 tileset
# the tiles can also be rotated by 180 degreees
TILES = [
    "",
    "w/sww/sswwf/1sddff/3dBdBf/5f",
    "sC/sfCfC/ssfff/1mmddf/3mmd/5d",
    "w/wwm/wwmmm/1fffsCmC/3fssC/5s",
    "d/ddm/ddmmm/1ddwwm/3ffwC/5fC",
    "wB/mBwBw/mmwwd/1mmddd/3sss/5s",
    "f/fww/ffsww/1sssmm/3sdmB/5dB",
]
#
# on a 2d matrix a tile looks like this:
# x
# xxx
# xxxxx
# _xxxxx
# ___xxx
# _____x


def to_grid(fen: str) -> Grid:
    res = []
    for line in fen.split("/"):
        index = 0
        row = [None for _ in range(6)]
        for letter, l_next in pairwise(line + "/"):
            match l_next:
                case "B":
                    territory_opt = Territory.BEAR
                case "C":
                    territory_opt = Territory.COUGAR
                case _:
                    territory_opt = None

            match letter:
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

            if cur is None:
                if letter.isdigit():
                    index += int(letter)
            else:
                row[index] = Field(cur, territory_opt, None)
                index += 1

        res.append(row)
    return res


# def rotate_tile(g:Grid)-> Grid:
#     rotated = []
#     for line in reversed(g):
#         end = 0
#         while True:
#             if line[end]


def rotate_fen(f: str) -> str:
    spaces = ["", "", "", "1", "3", "5"]
    res = []
    for line, num in zip(reversed(f.split("/")), spaces):
        newline = []
        for c, opt in pairwise(line + "/"):
            if c in "dwmfs":
                newline.append(c + (opt if opt.isupper() else ""))
        res.append(num + "".join(reversed(newline)))

    return "/".join(res)


# vertical append:
# x
# xxx
# xxxxx
# yxxxxx
# yyyxxx
# yyyyyx
# _yyyyy
# ___yyy
# _____y

# horizontal append:
# x
# xxx
# xxxxx
# _xxxxxy
# ___xxxyyy
# _____xyyyyy
# _______yyyyy
# _________yyy
# ___________y


def merge_tiles(tiles: tuple[int], flips: tuple[bool]) -> Grid:
    assert sorted(tiles) == list(range(1, 7))
    assert len(flips) == 6
    vertical_offset = 3
    horizontal_offset = 6
    #    1st tile + 2 added rows + 1 horizontal row
    height = Board.height
    width = Board.width
    grid = [[None] * width for _ in range(height)]
    # so basically if we append lower, then we insert our tile with offset 3 down
    # and for horizontal it's 3 down and 6 right
    for tile_idx, tile_num, flip in zip(range(6), tiles, flips):
        tile_fen = TILES[tile_num]
        if flip:
            tile_fen = rotate_fen(tile_fen)
        x, y = divmod(tile_idx, 2)
        tile_grid = to_grid(tile_fen)

        for i, row in enumerate(tile_grid):
            for j, elem in enumerate(row):
                dx = x * vertical_offset + y * vertical_offset + i
                dy = y * horizontal_offset + j
                # prevent overwriting of empty tiles (especially when appending vertically)
                if grid[dx][dy] is None:
                    grid[dx][dy] = elem

    return grid


neigh = [(-1, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (0, -1)]


def is_on_grid(p: Point) -> bool:
    return 0 <= p[0] < Board.height and 0 <= p[1] < Board.width


def distance(g: Grid, p1: Point, p2: Point) -> Optional[int]:
    """calculates the distance between two points, if possible"""
    if not is_on_grid(p1) or not is_on_grid(p2):
        return None
    # dx = x2 - x1
    # dy = y2 - y2
    # well, I have no idea how to do the math now
    # I think that if dy or dx == 0 then dist == the other one
    # also if  dx == dy then it's dx
    # but in other cases I'm confused
    # At least I know the neighbors: udlr and ul and dr
    # should I just slap a bfs?
    #
    # wait a minute, wouldn't distance be just a sum of the values
    # of the vector projected on base vectors?
    # so, for example,  (8,6) = 2*(1,0) + 6*(1,1) so dist = 8
    # but also          (8,6) = 8*(1,0) + 6*(0,1) => 14
    # what if           (-8, 6) = ??? is it 14?
    # https://stackoverflow.com/questions/14491444/calculating-distance-on-a-hexagon-grid
    # https://www.redblobgames.com/grids/hexagons/
    return NotImplemented


class Board:
    """cryptid uses hexgrid composed of 6 tiles which compose the playfield"""

    width: int = 12
    height: int = 15
    grid: Grid

    def __init__(
        self,
        tiles: list[int] = [1, 2, 3, 4, 5, 6],
        flips: list[bool] = [False] * 6,
    ):
        self.grid = merge_tiles(tiles, flips)

    def __repr__(self) -> str:
        """basic printing, pieces not implemented"""
        res = []

        def fd(e: Optional[Field]) -> str:
            if e is None:
                return " "
            match e.biome:
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
                    return Exception("Not reachable!")

        for line in self.grid:
            res.append("\t".join(fd(e) for e in line))

        return "\n".join(res)


class Tests(unittest.TestCase):
    def test_self_inverse(self):
        orig = TILES[1]
        reversed_str = rotate_fen(orig)
        twice_reversed = rotate_fen(reversed_str)
        self.assertEqual(twice_reversed, orig)

    def test_flip_once(self):
        orig = TILES[1]
        expected = "f/fdBdB/ffdds/1fwwss/3wws/5w"
        ans = rotate_fen(orig)
        self.assertEqual(ans, expected)

    def test_merge_tile_count(self):
        ans = merge_tiles([1, 2, 3, 4, 5, 6], [False] * 6)
        tiles_count = sum(1 for e in flatten(ans) if e is not None)
        # a proper board should have all 6 tiles which are 3 by 6
        self.assertEqual(tiles_count, 6 * 3 * 6)


if __name__ == "__main__":
    # seems to be legit
    # b = Board([3, 2, 1, 6, 5, 4], [True] + [False] * 5)
    # print(b)
    # b = Board([3, 2, 1, 6, 5, 4])
    # print(b)
    unittest.main()
