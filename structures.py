from __future__ import annotations
from typing import List, Set, Optional
from random import choice
from collections import UserList


class Cell:
    def __init__(self, options: Set[int], index: int) -> None:
        self.index = index
        self._row: Optional[Row] = None
        self._column: Optional[Column] = None
        self._square: Optional[Square] = None
        self.linked_cells: Optional[LinkedCells] = None
        self.options: set = set(options)  # need to make a copy of parameter set because that one is mutable
        self._len = len(options)
        self._value: int | None = None
        self.placeholder = '_'

    @property
    def value(self) -> int | None:
        return self._value

    @value.setter
    def value(self, new_val: int) -> None:
        self._value = new_val
        if self.linked_cells is None:
            raise ValueError('linked_cells must be established before setting cell value')
        self.linked_cells.reduce(new_val)
        self.options = set()

    @property
    def row(self) -> Row:
        return self._row

    @row.setter
    def row(self, r: Row) -> None:
        self._row = r
        self._set_linked_cells()

    @property
    def column(self) -> Column:
        return self._column
    
    @column.setter
    def column(self, c: Column) -> None:
        self._column = c
        self._set_linked_cells()

    @property
    def square(self) -> Square:
        return self._square

    @square.setter
    def square(self, s: Square) -> None:
        self._square = s
        self._set_linked_cells()
        
    def _set_linked_cells(self) -> None:
        rcs = (self._row, self._column, self._square)
        if all(rcs):
            self.linked_cells = LinkedCells(*rcs, cell=self)

    def reduce(self, val: int) -> None:
        self.options.discard(val)
        if self.value is not None and (self.options) == 0:
            self.placeholder = 'X'
            raise ValueError(f'Cell {self.index} cannot discard option {val} last element! {self.options}')

    def choose_value(self):
        self.value = choice(tuple(self.options))

    def __len__(self):
        return len(self.options)

    def __str__(self):
        return str(self.value or self.placeholder)

    def __repr__(self):
        return str(f'Cell( {self.index} )')


class CellGroup(UserList):
    def __init__(self) -> None:
        self.data: List[Cell]
        super().__init__()

    def append(self, what: Cell) -> Cell:
        super().append(what)
        return what

    @property
    def options(self) -> Set[int]:
        return set().union(*(c.options for c in self))

    def __str__(self):
        max_width_of_number = len(str(len(self.data)))
        return ' '.join(str(cell).center(max_width_of_number) for cell in self.data)

    def __repr__(self):
        return f"Cells({', '.join(str(c.index) for c in self.data)})"


class Row(CellGroup):
    def append(self, what: Cell) -> Cell:
        super().append(what)
        what.row = self
        return what


class Column(CellGroup):
    def append(self, what: Cell) -> Cell:
        super().append(what)
        what.column = self
        return what


class Square(CellGroup):
    def append(self, what: Cell) -> Cell:
        super().append(what)
        what.square = self
        return what


class LinkedCells(set):
    def __init__(self, r: Row, c: Column, s: Square, cell) -> None:
        super().__init__()
        self.update(r, c, s)
        self.remove(cell)

    def reduce(self, val):
        for cell in self:
            cell.reduce(val)
