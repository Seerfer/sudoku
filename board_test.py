import unittest
from unittest import mock
import board


def choice(x):
    return x[0]


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

    def test_board_knows_unfilled_cells(self):
        self.assertSetEqual(self.board.unfilled, set(self.board.cells))

    def test_board_knows_cells_with_least_options(self):
        self.board.cells[1].value = 1
        self.board.cells[4].value = 2
        self.board.cells[5].value = 3
        self.assertIs(self.board.least_free, self.board.cells[0])

    def test_board_can_fill_one_cell(self):
        # count unfilled cells and see if their number decreases
        before = len(self.board.unfilled)
        self.board.fill_one()
        after = len(self.board.unfilled)
        self.assertEqual(before - 1, after)

    def test_board_fills_with_values(self):
        self.board.fill()
        self.assertSetEqual(self.board.unfilled, set())

    def test_board_can_undo_fill(self):
        mock_cell = mock.Mock()
        self.board._least_free = lambda: mock_cell
        self.board.fill_one()
        self.board.undo_one()
        mock_cell.undo.assert_called()
