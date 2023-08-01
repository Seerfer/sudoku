class Cell:
    def __init__(self, options):
        self.row = None
        self.column = None
        self.square = None
        self.options: set = options
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_val):
        self._value = new_val
        self.options = set()

    def reduce(self, val):
        self.options.remove(val)


class CellGroup:
    def __init__(self):
        self.cells = []

    def reduce(self, val):
        for cell in self.cells:
            cell.reduce(val)

    def append(self, what: Cell) -> None:
        self.cells.append(what)

    @property
    def options(self):
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
