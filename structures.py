from __future__ import annotations
from typing import List, Set, Optional
from random import choice
from collections import UserList


class Cell:
    def __init__(self, options: Set[int], index: int) -> None:
        self.index = index
        self.row: Optional[Row] = None
        self.column: Optional[Column] = None
        self.square: Optional[Square] = None
        self.linked_cells: Optional[LinkedCells] = None
        self.options: set = set(options)  # need to make a copy of parameter set because that one is mutable
        self._value: int | None = None

    @property
    def value(self) -> int | None:
        return self._value

    @value.setter
    def value(self, new_val: int) -> None:
        self._value = new_val
        # TODO: call reduce on linked cells
        self.options = set()

    def reduce(self, val: int) -> None:
        try:
            self.options.remove(val)
        except KeyError:
            pass

    def choose_value(self):
        self.value = choice(tuple(self.options))

    def __len__(self):
        return len(self.options)

    def __str__(self):
        return str(self.value or '_')

    def __repr__(self):
        return str(f'Cell( {self.index} )')


class CellGroup(UserList):
    def __init__(self) -> None:
        self.data: List[Cell]
        super().__init__()

    def append(self, what: Cell) -> None:
        super().append(what)

    @property
    def options(self) -> Set[int]:
        return set().union(*(c.options for c in self))

    def __str__(self):
        max_width_of_number = len(str(len(self.data)))
        return ' '.join(str(cell).center(max_width_of_number) for cell in self.data)

    def __repr__(self):
        return f"Cells({', '.join(str(c.index) for c in self.data)})"


class Row(CellGroup):
    def append(self, what: Cell) -> None:
        super().append(what)
        what.row = self


class Column(CellGroup):
    def append(self, what: Cell) -> None:
        super().append(what)
        what.column = self


class Square(CellGroup):
    def append(self, what: Cell) -> None:
        super().append(what)
        what.square = self


class LinkedCells(set):
    def __init__(self, r: Row, c: Column, s: Square, cell) -> None:
        super().__init__()
        self.update(r, c, s)
        self.remove(cell)

    def reduce(self, val):
        for cell in self:
            cell.reduce(val)

