from __future__ import annotations
from typing import List, Set, Optional
from random import choice


class Cell:
    def __init__(self, options: Set[int], index: int) -> None:
        self.index = index
        self.row: Optional[Row] = None
        self.column: Optional[Column] = None
        self.square: Optional[Square] = None
        self.options: set = set(options)  # need to make a copy of parameter set because that one is mutable
        self._value: int | None = None

    @property
    def value(self) -> int | None:
        return self._value

    @value.setter
    def value(self, new_val: int) -> None:
        self._value = new_val
        self.row.reduce(new_val)
        self.column.reduce(new_val)
        self.square.reduce(new_val)
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

class CellGroup:
    def __init__(self) -> None:
        self.cells: List[Cell] = []

    def reduce(self, val) -> None:
        for cell in self.cells:
            cell.reduce(val)

    def append(self, what: Cell) -> None:
        self.cells.append(what)

    @property
    def options(self) -> Set[int]:
        return set().union(*(c.options for c in self.cells))

    def __str__(self):
        max_width_of_number = len(str(len(self.cells)))
        return ' '.join(str(cell).center(max_width_of_number) for cell in self.cells)

    def __repr__(self):
        return f"Cells({', '.join(str(c.index) for c in self.cells)})"

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
