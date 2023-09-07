from __future__ import annotations
from typing import List
from math import sqrt
from functools import partial
from random import choice
from structures import Cell, Row, Column, Square, OutOfOptions
from turtle import Turtle, Screen

def x_print(*args, **kwargs):
    pass
    # print(*args, **kwargs)


class Board:
    def __init__(self, size: int) -> None:
        self.size: int = size

        self.screen = self.setup_screen(1000)
        self.screen.listen()
        self.screen.tracer(0)
        self.screen.onclick(self.get_pos)

        self.turtle = self.setup_turtle()

        self.draw_board()

        options = set(range(1, self.size+1))
        self.cells: List[Cell] = []
        self.rows: List[Row] = [Row() for _ in range(self.size)]
        self.columns: List[Column] = [Column() for _ in range(self.size)]
        self.squares: List[Square] = [Square() for _ in range(self.size)]
        self.history: List[Cell] = []
        for i in range(self.size**2):
            pos = self.cell_index_to_pos(i, 1000, self.size)
            cell = Cell(options, i, pos)
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


    def get_pos(self, x,y):
        square_size = self.screen.window_width() // self.size
        x_zero_start = x + self.screen.window_width() // 2
        y_zero_start = y + self.screen.window_width() // 2
        x_i = x_zero_start // square_size
        y_i = abs(y_zero_start // square_size - 8)

        print(self.cells[int(y_i + x_i*self.size)].options)
    @staticmethod
    def cell_index_to_pos(index: int, screen_size: int, board_size:int) -> tuple:
        square_size = screen_size // board_size

        x_pos = index // board_size * square_size + square_size//2
        y_pos = index % board_size * square_size + square_size//2

        return x_pos - screen_size // 2, y_pos - screen_size // 2


    def setup_screen(self, size: int):
        screen = Screen()
        screen.setup(width=size, height=size)
        screen.bgcolor("white")
        screen.title("Sudoku")
        return screen


    def setup_turtle(self):
        turtle = Turtle()
        turtle.hideturtle()
        turtle.speed(0)
        return turtle

    @staticmethod
    def draw_line(t: Turtle, start: tuple, end: tuple, is_bold=False):
        t.penup()
        t.goto(*start)
        t.pendown()
        if is_bold:
            t.pensize(5)
            t.color("red")
        t.goto(*end)
        t.penup()
        t.pensize(1)
        t.color("black")

    def draw_board(self):
        square_width = self.screen.window_width() // self.size
        square_height = self.screen.window_height() // self.size

        screen_x_right_border = self.screen.window_width() // 2
        screen_x_left_border = -1 * screen_x_right_border

        screen_y_upper_border = self.screen.window_height() // 2
        screen_y_down_border = -1 * screen_y_upper_border

        n = screen_y_upper_border-square_height
        c = 0
        bold = False
        while n > screen_y_down_border:
            if c == 2:
                bold = True
                c = 0
            else:
                c += 1
            self.draw_line(self.turtle, (screen_x_left_border, n), (screen_x_right_border, n), bold)
            n = n - square_height
            bold = False

        c = 0
        n = screen_x_right_border - square_width
        bold = False
        while n > screen_x_left_border:
            if c == 2:
                bold = True
                c = 0
            else:
                c += 1
            self.draw_line(self.turtle, (n, screen_y_upper_border), (n, screen_y_down_border), bold)
            n = n - square_height
            bold = False



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
    while True:
        board = Board(9)
        board.fill()
        print(f'the board is {board.validate()}')
        board.screen.resetscreen()
        # from sys import argv
        # from time import monotonic as clock


        # side = int(argv[1]) if len(argv) == 2 else 3
        # t0 = clock()
        # rep: int = 0
        # for rep in range(20_000):
        #     board = Board(side**2)
        #     print(f"New Board {rep}")
        #     try:
        #         board.fill()
        #     except IndexError:
        #         continue
        #     else:
        #         if not board.validate():
        #             print('invalid.')
        #             continue
        #         print(board)
        #         print('=' * (board.size * 2))
        #         validity = 'valid' if board.validate() else 'NOT valid'
        #         print(f'the board is {validity}')
        #         break
        # t1 = clock()
        # print(f'Operation took {t1-t0:.2f} seconds over {rep+1} boards, {(t1-t0)/(rep+1):.3f} seconds on average')
