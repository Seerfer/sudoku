from __future__ import annotations
from typing import List
from math import sqrt
from random import choice
from structures import Cell, Row, Column, Square, OutOfOptions


def x_print(*args, **kwargs):
    pass
    # print(*args, **kwargs)


class Board:
    def __init__(self, size: int) -> None:
        self.size: int = size
        options = set(range(1, self.size+1))
        self.cells: List[Cell] = []
        self.rows: List[Row] = [Row() for _ in range(self.size)]
        self.columns: List[Column] = [Column() for _ in range(self.size)]
        self.squares: List[Square] = [Square() for _ in range(self.size)]
        self.history: List[Cell] = []
        for i in range(self.size**2):
            cell = Cell(options, i)
            self.cells.append(cell)
            sq_size = int(sqrt(self.size))
            row = i // self.size
            col = i % self.size
            sq = (row // sq_size) * sq_size + col // sq_size
            self.rows[row].append(cell)
            self.columns[col].append(cell)
            self.squares[sq].append(cell)
        for cell in self.cells:
            cell.set_linked_cells()
        self.last_cell = self.cells[0]

    @property
    def unfilled(self) -> set:
        return {cell for cell in self.cells if len(cell) > 0}

    @property
    def least_free(self) -> Cell | None:
        return self._least_free()

    @property
    def filled_cells(self):
        return self.size ** 2 - [cell.value for cell in self.cells].count(None)

    def _least_free(self) -> Cell | None:
        try:
            min_len = min(map(len, self.unfilled))
        except ValueError:
            return None
        else:
            return choice([c for c in self.unfilled if len(c) == min_len])

    def fill_one(self, fixed_cell=None):
        cell = fixed_cell or self.least_free
        self.history.append(cell)
        c = cell.choose_value()
        x_print(self, '=' * self.size ** 2, sep='\n')
        return c

    def undo_one(self):
        last_set_cell = self.history.pop()
        last_set_cell.undo()
        return last_set_cell

    def fill(self):
        undone_cell = None
        while self.unfilled:
            try:
                self.fill_one(undone_cell)
            except OutOfOptions:
                x_print(*[c.index for c in self.history][::-1])
                undone_cell = self.undo_one()
                while len(undone_cell) <= 1:
                    undone_cell = self.undo_one()

    def validate(self):
        return \
            all(x.validate() for x in self.rows) and\
            all(x.validate() for x in self.columns) and\
            all(x.validate() for x in self.squares)

    def __str__(self):
        return '\n'.join(map(str, self.rows))


if __name__ == '__main__':
    from sys import argv
    from time import monotonic as clock
    side = int(argv[1]) if len(argv) == 2 else 3
    t0 = clock()
    rep: int = 0
    for rep in range(20_000):
        board = Board(side**2)
        print(f"New Board {rep}")
        try:
            board.fill()
        except IndexError:
            continue
        else:
            if not board.validate():
                print('invalid.')
                continue
            print(board)
            print('=' * (board.size * 2))
            validity = 'valid' if board.validate() else 'NOT valid'
            print(f'the board is {validity}')
            break
    t1 = clock()
    print(f'Operation took {t1-t0:.2f} seconds over {rep+1} boards, {(t1-t0)/(rep+1):.3f} seconds on average')
