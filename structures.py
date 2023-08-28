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
                    options=self.options
                )
            )
            self.options.discard(val)
            if self.options == set():
                self.placeholder = 'X'
                raise ValueError(f'Cell {self.index} cannot discard option {val} last element! {self.options}')
        else:
            self.history.append(
                Step(
                    action=StepType.NOTHING,
                )
            )

    def choose_value(self):
        self.value = choice(tuple(self.options))

    def undo(self) -> Step:
        self.placeholder = '_'
        last_step: Step = self.history.pop()
        if last_step.action is not StepType.NOTHING:
            self._value = last_step.value
            self.options = last_step.options
            if last_step.action is StepType.SET_VALUE:
                self.linked_cells.undo()
                self.placeholder = 'X'
        return last_step

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

    def undo(self):
        for cell in self:
            cell.undo()
