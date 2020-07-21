from dataclasses import dataclass

import numpy as np
from toolz import thread_last

from sudoku.fp.load import format_sudoku, parse_raw
from sudoku.fp.solve import block_coordinates


@dataclass
class Sudoku:
    grid: np.ndarray

    @classmethod
    def from_string(cls, raw):
        return thread_last(raw, parse_raw, cls)

    def copy(self):
        return type(self)(self.grid.copy())

    @property
    def remaining_blanks(self):
        return (self.grid == 0).sum()

    @property
    def is_solved(self):
        return self.remaining_blanks == 0

    def __init__(self, grid=None):
        self.grid = grid

    def get_row(self, y):
        return self.grid[y, :]

    def get_column(self, x):
        return self.grid[:, x]

    def get_square(self, y, x):
        return self.grid[y, x]

    def get_block_of(self, y, x):
        return self.grid[block_coordinates(y, x)]

    def set_digit(self, y, x, digit, inplace: bool = False):
        if inplace:
            self.grid[y, x] = digit
        else:
            grid = self.grid.copy()
            grid[y, x] = digit
            return type(self)(grid)

    def __repr__(self):
        return format_sudoku(self.grid)
