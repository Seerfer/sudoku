import unittest
from unittest import mock

import structures
from structures import Cell, CellGroup, Row


class TestCell(unittest.TestCase):
    def setUp(self):
        self.possible_ones = {1, 2, 3, 4}
        self.cell = Cell(self.possible_ones)

    def test_cell_is_initialized(self):
        self.assertIsInstance(self.cell, Cell)

    def test_cell_knows_row_column_square(self):
        self.assertTrue(hasattr(self.cell, "row"))
        self.assertTrue(hasattr(self.cell, "column"))
        self.assertTrue(hasattr(self.cell, "square"))

    def test_cell_knows_actual_value(self):
        self.assertTrue(hasattr(self.cell, "value"))
        self.cell.row = mock.MagicMock()
        self.cell.column = mock.MagicMock()
        self.cell.square = mock.MagicMock()
        self.cell.value = 0
        self.assertEqual(0, self.cell.value)

    def test_cell_knows_possible_values(self):
        self.assertEqual(self.possible_ones, self.cell.options)

    def test_setting_cell_value_clears_possible_ones(self):
        self.cell.row = mock.MagicMock()
        self.cell.column = mock.MagicMock()
        self.cell.square = mock.MagicMock()
        self.cell.value = 3
        self.assertSetEqual(set(), self.cell.options)

    def test_reducing_option_removes_from_options(self):
        self.assertIn(3, self.cell.options)
        self.cell.reduce(3)
        self.assertNotIn(3, self.cell.options)


class TestCellInContext(unittest.TestCase):
    def setUp(self):
        self.possible_ones = {1, 2, 3, 4}
        self.cell = Cell(self.possible_ones)
        self.row = mock.Mock()
        self.cell.row = self.row
        self.cell.column = mock.Mock()
        self.cell.square = mock.Mock()

    def test_setting_value_reduces_row(self):
        self.cell.value = 3
        self.row.reduce.assert_called_with(3)


class TestCellGroup(unittest.TestCase):
    def setUp(self):
        self.cg = CellGroup()

    def test_knows_constituent_cells(self):
        self.assertTrue(hasattr(self.cg, 'cells'))

    def test_reducing_value_removes_it_from_cells(self):
        cells = [Cell({1, 2, 3, 4}) for _ in range(4)]
        for cell in cells:
            self.cg.append(cell)
        self.cg.reduce(3)
        for cell in cells:
            self.assertNotIn(3, cell.options)

    def test_options_is_a_union_of_cell_options(self):
        cells = [Cell({i+1}) for i in range(4)]
        for cell in cells:
            self.cg.append(cell)
        self.assertSetEqual({1, 2, 3, 4}, self.cg.options)

    def test_appending_cell_adds_it_to_list(self):
        new_cell = Cell
        self.cg.append(Cell)
        self.assertIn(new_cell, self.cg.cells)


class TestRow(unittest.TestCase):
    def setUp(self):
        self.row = Row()
        self.cell = Cell({1, 2, 3, 4})

    def test_adding_cell_sets_row_in_the_cell(self):
        self.row.append(self.cell)
        self.assertEqual(self.row, self.cell.row)
