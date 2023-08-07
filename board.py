from typing import List
from math import sqrt
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
            cell = Cell(options)
            self.cells.append(cell)
            sq_size = int(sqrt(self.size))
            row = i // self.size
            col = i % self.size
            sq = (row // sq_size) * sq_size + col // sq_size
            self.rows[row].append(cell)
            self.columns[col].append(cell)
            self.squares[sq].append(cell)

