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
    PlayerColor,
    ALL_BIOMES,
    STRUCT_COLORS,
    PLAYER_COLORS,
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
    color: PlayerColor
    type: PieceType


@define
class Field:
    biome: Biome
    territory: Optional[Territory]
    structure: Optional[Structure]
    pieces: Optional[list[Piece]]


Grid = Annotated[
    List[List["Field"]],
    "TypeAlias for a grid of optional 'Field' objects",
]
Point = tuple[int, int]


def is_on_grid(p: Point) -> bool:
    return 0 <= p[0] < Board.height and 0 <= p[1] < Board.width


def oddq_to_axial(row: int, col: int):
    r = row - (col - (col & 1)) // 2
    return col, r


def axial_to_oddq(q, r):
    row = r + (q - q & 1) // 2
    return q, row


def distance(g: Grid, p1: Point, p2: Point) -> Optional[int]:
    """calculates the distance between two points, if possible"""
    if not is_on_grid(p1) or not is_on_grid(p2):
        return None

    return NotImplemented


# TODO: this might break stuff if the order row and col in point is wrong
def neigh_dist(pos: Point, radius: int) -> list[Point]:
    q, r = oddq_to_axial(pos[0], pos[1])
    neigh = []
    for q in range(-radius, radius + 1):
        r_min = max(-radius, -radius - q)
        r_max = min(radius, radius - q)
        for r in range(r_min, r_max + 1):
            neigh.append(axial_to_oddq(q, r))

    return neigh


class Board:
    """cryptid uses hexgrid composed of 6 tiles which compose the playfield"""

    width: int = 12
    height: int = 9
    grid: Grid

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
                le + r for le, r in zip(left_biomes_tile, right_biomes_tile)
            ]
            new_territory_rows = [
                le + r for le, r in zip(left_territory_tile, right_territory_tile)
            ]

            for biome_row, territory_row in zip(new_biome_rows, new_territory_rows):
                row = []
                for biome_char, territiory in zip(biome_row, territory_row):
                    t = Territory.from_char(territiory)
                    b = Biome.from_char(biome_char)
                    if b is None:
                        raise ValueError(
                            f"invalid character when parsing biome {biome_char}"
                        )
                    row.append(Field(b, t, None, None))
                grid.append(row)

        return grid

    def add_structure(
        self, position: Point, color: StructureColor, stype: StructureType
    ):
        assert is_on_grid(position)
        y, x = position
        if self.grid[y][x] is not None:
            self.grid[y][x].structure = Structure(color, stype)
        else:
            raise AttributeError()

    def add_piece(self, position: Point, color: PlayerColor, ptype: PieceType):
        assert is_on_grid(position)
        y, x = position
        if self.grid[y][x] is not None:
            if self.grid[y][x].pieces is None:
                self.grid[y][x].pieces = []
            self.grid[y][x].pieces.append(Piece(color, ptype))

        else:
            raise AttributeError()

    def reduce_hints(self, clues: list[Clue], position: Point) -> list[Clue]:
        y, x = position
        assert self.grid[y][x] is not None
        # 1st type of hints: 2 biomes
        cur_biome = self.grid[y][x].biome
        # 2nd type: within 1-3
        visited = [{} for _ in range(4)]
        for radius in range(1, 4):
            for dy, dx in neigh_dist(position, radius):
                x_cur = x + dx
                y_cur = y + dy
                if is_on_grid((y_cur, x_cur)):
                    if self.grid[y][x] is not None:
                        visited[radius].add(self.grid[y][x].biome)
                    if self.grid[y][x].structure is not None:
                        visited[radius].add(self.grid[y][x].structure.color)
                        visited[radius].add(self.grid[y][x].structure.type)
                    if self.grid[y][x].territory is not None:
                        visited[radius].add(self.grid[y][x].territory)
                        visited[radius].add(Territory.BOTH)

        two_terrains = []
        within_one = []
        within_two = []
        within_three = []
        for clue in clues:
            match clue.clue_type:
                case ClueType.TWO_TERRAINS:
                    if cur_biome not in clue.data:
                        two_terrains.append(clue)
                case ClueType.WITHIN_ONE:
                    if clue.data not in visited[1]:
                        within_one.append(clue)
                case ClueType.WITHIN_TWO:
                    if clue.data not in visited[2]:
                        within_three.append(clue)
                case ClueType.WITHIN_THREE:
                    # WARNING: BLACK STRUCTURE IS USED ONLY IN ADVANCED MODE
                    if clue.data not in visited[3]:
                        within_one.append(clue)

        return two_terrains + within_one + within_two + within_three

    def calculate_all_hints(self) -> dict[PlayerColor, list[Clue]]:
        players_hints = {p: generate_all_clues() for p in PLAYER_COLORS}
        for y, row in enumerate(self.grid):
            for x, elem in enumerate(row):
                if elem is not None and elem.pieces is not None:
                    for piece in elem.pieces:
                        if piece.type == PieceType.CUBE:
                            # now we can reduce hints
                            new_hints = self.reduce_hints(
                                players_hints[piece.color], (y, x)
                            )
                            players_hints[piece.color] = new_hints

        return players_hints


if __name__ == "__main__":
    # seems to be legit
    # b = Board([3, 2, 1, 6, 5, 4], [True] + [False] * 5)
    # print(b)
    b = Board()
    print(b)
    pass
