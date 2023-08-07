import unittest
import board


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.board = board.Board(4)

    def test_board_knows_own_size(self):
        self.assertEqual(4, self.board.size)

    def test_board_has_all_its_cells(self):
        self.assertEqual(4**2, len(self.board.cells))

    def test_board_has_all_its_containers(self):
        self.assertEqual(4, len(self.board.rows))
        self.assertEqual(4, len(self.board.columns))
        self.assertEqual(4, len(self.board.squares))

    def test_board_can_pick_a_cell(self):
        cell = self.board.pick_cell()
        self.assertIs(self.board.cells[0], cell)