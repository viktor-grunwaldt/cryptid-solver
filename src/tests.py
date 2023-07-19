import unittest
import board

class Tests(unittest.TestCase):
    def test_self_inverse(self):
        orig = board.TILES[1]
        reversed_str = board.rotate_fen(orig)
        twice_reversed = board.rotate_fen(reversed_str)
        self.assertEqual(twice_reversed, orig)

    def test_flip_once(self):
        orig = board.TILES[1]
        # TODO: change coord system
        expected = "f/fdBdB/ffdds/1fwwss/3wws/5w"
        ans = board.rotate_fen(orig)
        self.assertEqual(ans, expected)

    def test_merge_tile_count(self):
        ans = board.merge_tiles([1, 2, 3, 4, 5, 6], [False] * 6)
        tiles_count = sum(1 for e in board.flatten(ans) if e is not None)
        # a proper board should have all 6 tiles which are 3 by 6
        self.assertEqual(tiles_count, 6 * 3 * 6)