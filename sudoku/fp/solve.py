import logging
import random
from functools import partial
from itertools import product

import numpy as np

from sudoku import SolvingException


def solve(sudoku, step_function, raise_on_not_solved: bool = True):
    sudoku = sudoku.copy()
    initial_blanks = (sudoku == 0).sum()

    solving = True
    blanks_after = 0
    while solving:
        blanks_before = (sudoku == 0).sum()
        sudoku = step_function(sudoku)
        blanks_after = (sudoku == 0).sum()
        solving = (blanks_after < blanks_before)

    if raise_on_not_solved and blanks_after:
        raise SolvingException(f'Failed to solve Sudoku ({blanks_after} of {initial_blanks} blanks remain).')
    return sudoku


def repeat_solve(sudoku, solve_function, max_tries=100):
    for n in range(max_tries):
        try:
            solved = solve_function(sudoku)
            logging.info(f'Solved Sudoku after {n} tries.')
            return solved
        except SolvingException:
            continue
    raise SolvingException(f'Failed to solve Sudoku after {max_tries} tries')


def make_mask(sudoku, digit):
    mask = np.ones_like(sudoku)
    for y, x in product(range(9), range(9)):
        if sudoku[y, x] == 0:
            continue
        elif sudoku[y, x] == digit:
            mask[y, :] = 0
            mask[:, x] = 0
            mask[block_coordinates(y, x)] = 0
            mask[y, x] = 1
        else:
            mask[y, x] = 0

    return mask


def block_coordinates(y, x):
    block_x = (x // 3) * 3
    block_y = (y // 3) * 3
    return np.index_exp[block_y:block_y + 3, block_x:block_x + 3]


def deterministic_step(sudoku):
    sudoku = sudoku.copy()
    for digit in range(1, 10):
        mask = make_mask(sudoku, digit)
        for y, x in product(range(9), range(9)):
            if sudoku[y, x] == 0 and mask[y, x] == 1:
                row = mask[y, :]
                col = mask[:, x]
                block = mask[block_coordinates(y, x)]
                for section in [row, col, block]:
                    if section.sum() == 1:
                        sudoku[y, x] = digit
    return sudoku


solve_deterministic = partial(solve, step_function=deterministic_step)


def random_step(sudoku):
    sudoku = sudoku.copy()
    digit = random.choice(range(1, 10))
    mask = make_mask(sudoku, digit)
    y, x = random.choice(list(zip(*np.where(mask == 1))))
    sudoku[y, x] = digit
    return sudoku


solve_random = partial(solve, step_function=random_step)


def combined_step(sudoku):
    sudoku = solve_deterministic(sudoku, raise_on_not_solved=False)
    if (sudoku == 0).sum() > 0:
        sudoku = random_step(sudoku)
    return sudoku


solve_combined = partial(solve, step_function=combined_step)
