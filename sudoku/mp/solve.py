from dataclasses import dataclass
from functools import partial
from typing import Callable

from sudoku.fp import solve as _fp_solve
from sudoku.mp.base import Sudoku


def solve(sudoku: Sudoku, step_function: Callable, max_tries: int = 1):
    if max_tries == 1:
        solved_grid = _fp_solve.solve(sudoku.grid, step_function)
    else:
        solved_grid = _fp_solve.repeat_solve(sudoku.grid,
                                             partial(_fp_solve.solve, step_function=step_function),
                                             max_tries=max_tries)
    return Sudoku(solved_grid)


@dataclass(frozen=True)
class Solver:
    step_function: Callable
    max_tries: int = 1

    def __call__(self, sudoku: Sudoku):
        return solve(sudoku, self.step_function, self.max_tries)
