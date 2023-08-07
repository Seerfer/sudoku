import unittest
import board


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board = board.Board(4)

    def test_board_knows_own_size(self):
        self.assertEqual(4, self.board.size)

    def test_board_has_sll_its_cells(self):
        self.assertEqual(4**2, len(self.board.cells))