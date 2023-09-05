from __future__ import annotations
from typing import List, Set, Optional
from random import choice
from collections import UserList
from dataclasses import dataclass, field
from enum import Enum


class StepType(Enum):
    SET_VALUE = 'set value'
    REDUCE = 'reduce'
    NOTHING = 'nothing'


@dataclass
class Step:
    action: StepType
    value: None = None  # value for undo will always be None
    options: set = field(default_factory=set)


class Cell:
    def __init__(self, options: Set[int], index: int) -> None:
        self.index = index
        self.row: Optional[Row] = None
        self.column: Optional[Column] = None
        self.square: Optional[Square] = None
        self.linked_cells: Optional[LinkedCells] = None
        self.options: set = set(options)  # need to make a copy of parameter set because that one is mutable
        self._len = len(options)
        self._value: int | None = None
        self.placeholder = '_'
        self.history: List[Step] = []

    @property
    def value(self) -> int | None:
        return self._value

    @value.setter
    def value(self, new_val: int) -> None:
        self.history.append(
            Step(
                action=StepType.SET_VALUE,
                options=self.options
            )
        )
        self._value = new_val
        # print(f'Setting Cell {self.index} value to {new_val}.')
        if self.linked_cells is None:
            raise ValueError('linked_cells must be established before setting cell value')
        self.linked_cells.reduce(new_val)
        self.options = set()
        
    def set_linked_cells(self) -> None:
        rcs = (self.row, self.column, self.square)
        if all(rcs):
            self.linked_cells = LinkedCells(*rcs, cell=self)

    def reduce(self, val: int) -> None:
        if self.value is None:
            self.history.append(
                Step(
                    action=StepType.REDUCE,
                    options=set(self.options)
                )
            )
            self.options.discard(val)
            if self.options == set():
                self.placeholder = 'X'
                raise OutOfOptions(f'Cell {self.index} cannot discard option {val}. Last element!')
        else:
            self.history.append(
                Step(action=StepType.NOTHING)
            )

    def choose_value(self):
        options = self.options
        self.value = choice(tuple(self.options))
        return options

    def undo(self, reinstate_value=False) -> Step:
        self.placeholder = '_'
        last_step: Step = self.history.pop()
        if last_step.action is not StepType.NOTHING:
            saved_value = self._value
            saved_options = self.options
            self._value = last_step.value
            self.options = last_step.options
            if last_step.action is StepType.SET_VALUE:
                if not reinstate_value:
                    self.options = last_step.options - {saved_value}
                self.placeholder = 'X'
                print(f'Undo in {self!r:<8}. Value rollback from {saved_value}, opts {self.options}')
                self.linked_cells.undo()
            else:
                print(f'Undo in {self!r:<8}. Rollback reduce from {saved_options} to {self.options}')
        return last_step

    def __len__(self):
        return len(self.options)

    def __str__(self):
        return str(self.value or self.placeholder)

    def __repr__(self):
        return str(f'Cell({self.index})')


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
        err = None
        for cell in self:
            try:
                cell.reduce(val)
            except ValueError as e:
                # ignore error to allow all cells reduce values
                err = e
        if err is not None:
            raise err

    def undo(self):
        for cell in self:
            cell.undo()


class OutOfOptions(Exception):
    pass
