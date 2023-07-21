from typing import Optional, List, Annotated
from attrs import define
from itertools import combinations
from more_itertools import chunked
from tiles import Tiles

from enums import (
    Biome,
    Territory,
    StructureColor,
    StructureType,
    PieceType,
    ClueType,
    Color,
    ALL_BIOMES,
    STRUCT_COLORS,
)


@define
class Structure:
    color: StructureColor
    type: StructureType


@define
class Clue:
    clue_type: ClueType
    data: tuple[Biome, Biome] | Biome | Territory | StructureColor | StructureType


def generate_all_clues() -> list[Clue]:
    within_two = (
        StructureType.SHACK,
        StructureType.STONE,
        Territory.BEAR,
        Territory.COUGAR,
    )
    clues = [Clue(ClueType.TWO_TERRAINS, pair) for pair in combinations(ALL_BIOMES, 2)]
    clues += [Clue(ClueType.WITHIN_ONE, e) for e in (ALL_BIOMES + (Territory.BOTH,))]
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
    pieces: Optional[list[Piece]]


Grid = Annotated[
    List[List[Optional["Field"]]], "TypeAlias for a grid of optional 'Field' objects"
]
Point = tuple[int, int]


def is_on_grid(p: Point) -> bool:
    return 0 <= p[0] < Board.height and 0 <= p[1] < Board.width


def distance(g: Grid, p1: Point, p2: Point) -> Optional[int]:
    """calculates the distance between two points, if possible"""
    if not is_on_grid(p1) or not is_on_grid(p2):
        return None

    # https://stackoverflow.com/questions/14491444/calculating-distance-on-a-hexagon-grid
    # https://www.redblobgames.com/grids/hexagons/
    return NotImplemented


class Board:
    """cryptid uses hexgrid composed of 6 tiles which compose the playfield"""

    width: int = 12
    height: int = 9
    grid: Grid

    def create_grid(self, tiles: list[int], flips: list[bool]) -> Grid:
        grid = []
        tiles_fen = [Tiles.from_int(i) for i in tiles]
        # load and rotate the tiles
        for i in range(len(tiles_fen)):
            if flips[i]:
                tiles_fen[i] = (
                    Tiles.rotate(tiles_fen[i][0]),
                    Tiles.rotate(tiles_fen[i][1]),
                )
        # parse and merge tiles
        for left, right in chunked(tiles_fen, 2):
            left_biomes_tile, left_territory_tile = left
            right_biomes_tile, right_territory_tile = right
            new_biome_rows = [
                l + r for l, r in zip(left_biomes_tile, right_biomes_tile)
            ]
            new_territory_rows = [
                l + r for l, r in zip(left_territory_tile, right_territory_tile)
            ]

            for biome_row, territory_row in zip(new_biome_rows, new_territory_rows):
                row = []
                for biome_char, territiory in zip(biome_row, territory_row):
                    t = Territory.from_char(territiory)
                    b = Biome.from_char(biome_char)
                    if b is None:
                        raise ValueError(f"invalid character when parsing biome {biome_char}")
                    row.append(Field(b, t, None, None))
                grid.append(row)

        return grid

    def __init__(
        self,
        tiles: list[int] = [1, 2, 3, 4, 5, 6],
        flips: list[bool] = [False] * 6,
    ):
        self.grid = self.create_grid(tiles, flips)

    def __repr__(self) -> str:
        """basic printing, pieces not implemented"""
        res = []

        def fd(e: Optional[Field]) -> str:
            if e is None:
                return " "
            return e.biome.to_char()

        for line in self.grid:
            res.append(" ".join(fd(e) for e in line))

        return "\n".join(res)


if __name__ == "__main__":
    # seems to be legit
    # b = Board([3, 2, 1, 6, 5, 4], [True] + [False] * 5)
    # print(b)
    b = Board()
    print(b)
    pass
