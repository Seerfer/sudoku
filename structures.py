from typing import List, Set, Optional


class Cell:
    def __init__(self, options: Set[int]) -> None:
        self.row: Optional[Row] = None
        self.column: Optional[Column] = None
        self.square: Optional[Square] = None
        self.options: set = options
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
