from __future__ import annotations
from typing import List
from math import sqrt
from random import choice
from structures import Cell, Row, Column, Square


class Board:
    def __init__(self, size: int) -> None:
        self.size: int = size
        options = set(range(1, self.size+1))
        self.cells: List[Cell] = []
        self.rows: List[Row] = [Row() for _ in range(self.size)]
        self.columns: List[Column] = [Column() for _ in range(self.size)]
        self.squares: List[Square] = [Square() for _ in range(self.size)]
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

    @property
    def unfilled(self) -> set:
        return {cell for cell in self.cells if len(cell) > 0}

    @property
    def least_free(self) -> Cell | None:
        try:
            min_len = min(map(len, self.unfilled))
        except ValueError:
            return None
        else:
            return choice([c for c in self.unfilled if len(c) == min_len])

    def fill(self):
        while self.unfilled:
            cell = self.least_free
            cell.choose_value()

    def __str__(self):
        return '\n'.join(map(str, self.rows))


if __name__ == '__main__':
    from time import monotonic as clock
    t0 = clock()
    for rep in range(200):
        board = Board(4)
        try:
            board.fill()
            t1 = clock()
        except ValueError as e:
            t1 = clock()
            print(board)
            print(e)
            break
    print(f'operation took {t1-t0:.2f} seconds over {rep+1} boards, {(t1-t0)/(rep+1):.3f} seconds on average')
