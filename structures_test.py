import unittest
from unittest import mock
from itertools import chain

from structures import Cell, CellGroup, Row, Column, Square, LinkedCells


class TestCell(unittest.TestCase):
    def setUp(self):
        self.possible_ones = {1, 2, 3, 4}
        self.cell = Cell(self.possible_ones, 0)

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
        self.cell = Cell(self.possible_ones, 0)

    def test_cell_knows_linked_cells(self):
        cell: Cell = Cell(self.possible_ones, 0)
        expected_cells = set()
        row = Row()
        expected_cells.add(row.append(Cell(self.possible_ones, 0)))
        col = Column()
        expected_cells.add(col.append(Cell(self.possible_ones, 0)))
        sq = Square()
        expected_cells.add(sq.append(Cell(self.possible_ones, 0)))
        for x in (row, col, sq):
            x.append(cell)
        # the cell should now have them added and integrated into linked_cells property
        # through internal mechanisms
        self.assertSetEqual(expected_cells, cell.linked_cells)

    def test_setting_value_reduces_linked_cells(self):
        r, c, s = mock.Mock(), mock.Mock(), mock.Mock()
        l_c = mock.Mock()
        self.cell._set_linked_cells = lambda: None
        self.cell.linked_cells = l_c
        self.cell.row = r
        self.cell.column = c
        self.cell.square = s
        self.cell.value = 3
        l_c.reduce.assert_called_with(3)


class TestCellGroup(unittest.TestCase):
    def setUp(self):
        self.cg = CellGroup()

    def test_knows_constituent_cells(self):
        self.assertTrue(hasattr(self.cg, 'data'))

    def test_options_is_a_union_of_cell_options(self):
        cells = [Cell({i+1}, 0) for i in range(4)]
        for cell in cells:
            self.cg.append(cell)
        self.assertSetEqual({1, 2, 3, 4}, self.cg.options)

    def test_appending_cell_adds_it_to_list(self):
        new_cell = Cell({0}, 0)
        self.cg.append(new_cell)
        self.assertIn(new_cell, self.cg.data)


class TestRow(unittest.TestCase):
    def setUp(self):
        self.row = Row()
        self.cell = Cell({1, 2, 3, 4}, 0)

    def test_adding_cell_sets_row_in_the_cell(self):
        self.row.append(self.cell)
        self.assertEqual(self.row, self.cell.row)


class TestLinkedCells(unittest.TestCase):
    def setUp(self):
        r, c, s = Row(), Column(), Square()
        self.the_cell = None
        self.expected_cells = set()
        cell = Cell({1, 2, 3, 4}, 0)
        r.append(cell)
        c.append(cell)
        s.append(cell)
        self.the_cell = cell
        for i in range(1, 4**2):
            cell = Cell({1, 2, 3, 4}, i)
            include_cell = False
            if 0 < i < 4:
                r.append(cell)
                include_cell = True
            if i % 4 == 0:
                c.append(cell)
                include_cell = True
            if i in (1, 4, 5):
                s.append(cell)
                include_cell = True
            if include_cell:
                self.expected_cells.add(cell)

        self.linked_cells = LinkedCells(r, c, s, self.the_cell)

    def test_cells_interlinked_knows_constituent_cells(self):
        self.assertSetEqual(self.expected_cells, self.linked_cells)

    def test_reducing_value_removes_it_from_cells(self):
        self.linked_cells.reduce(4)
        linked_cells_options = set(chain.from_iterable(cell.options for cell in self.linked_cells))
        self.assertNotIn(4, linked_cells_options)
