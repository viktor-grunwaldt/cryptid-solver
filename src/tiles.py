from enums import Biome

"""
w = water
d = desert
m = mountain
s = swamp
f = forest
"""


class Tiles:
    tile1 = ["wwwwff", "sswdff", "ssdddf"]
    tile2 = ["sfffff", "ssfddd", "smmmmd"]
    tile3 = ["ssfffw", "ssfmww", "mmmmww"]
    tile4 = ["ddmmmm", "ddmwww", "dddfff"]
    tile5 = ["sssmmm", "sddwmm", "ddwwww"]
    tile6 = ["ddsssf", "mmssff", "mwwwwf"]

    habitat1 = ["xxxxxx", "xxxxxx", "xxxBBB"]
    habitat2 = ["CCCxxx", "xxxxxx", "xxxxxx"]
    habitat3 = ["xxxxxx", "CCxxxx", "Cxxxxx"]
    habitat4 = ["xxxxxx", "xxxxxC", "xxxxxC"]
    habitat5 = ["xxxxxx", "xxxxxB", "xxxxBB"]
    habitat6 = ["Bxxxxx", "Bxxxxx", "xxxxxx"]

    def rotate(tile: list[str]) -> list[str]:
        return [s[::-1] for s in reversed(tile)]

    def from_int(num:int) -> tuple[list[str], list[str]]:
        assert num in range(1,7)
        return [
            (Tiles.tile1, Tiles.habitat1),
            (Tiles.tile2, Tiles.habitat2),
            (Tiles.tile3, Tiles.habitat3),
            (Tiles.tile4, Tiles.habitat4),
            (Tiles.tile5, Tiles.habitat5),
            (Tiles.tile6, Tiles.habitat6),
        ][num-1]
