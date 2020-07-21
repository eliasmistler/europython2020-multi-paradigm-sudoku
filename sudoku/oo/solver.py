import logging
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict

import numpy as np

from sudoku import SolvingException
from sudoku.oo.base import Sudoku


@dataclass
class SudokuSolver(ABC):
    sudoku: Sudoku

    @abstractmethod
    def solve(self):
        pass


class StepBasedSolver(SudokuSolver):
    @abstractmethod
    def solve_step(self):
        pass

    def solve(self):
        initial_blanks = self.sudoku.remaining_blanks

        solving = True
        while solving:
            blanks_before = self.sudoku.remaining_blanks
            self.solve_step()
            solving = (self.sudoku.remaining_blanks < blanks_before)

        if not self.sudoku.is_solved:
            raise SolvingException(
                f'Failed to solve Sudoku ({self.sudoku.remaining_blanks} of {initial_blanks} blanks remain).')

    def repeat_solve(self, max_tries=100):
        for n in range(max_tries):
            try:
                self.solve()
                logging.info(f'Solved Sudoku after {n} tries.')
            except SolvingException:
                continue
        if not self.sudoku.is_solved:
            raise SolvingException(f'Failed to solve Sudoku after {max_tries} tries')


class StepAndMaskBasedSolver(StepBasedSolver):
    """
    A solver that uses masks of possible actions, and iterates over steps
    """
    masks: Dict[int, Sudoku] = {}

    def update_masks(self):
        masks = {}
        for digit in range(1, 10):
            masks[digit] = np.ones((9, 9), dtype='int64')

        for square in self.sudoku.squares:
            if square.digit != 0:
                masks[square.digit][square.y, :] = 0
                masks[square.digit][:, square.x] = 0
                block_x = (square.x // 3) * 3
                block_y = (square.y // 3) * 3
                masks[square.digit][np.index_exp[block_y:block_y + 3, block_x:block_x + 3]] = 0
                masks[square.digit][square.y, square.x] = 1

                for digit in range(1, 10):
                    if digit != square.digit:
                        masks[digit][square.y, square.x] = 0

        for digit, mask in masks.items():
            self.masks[digit] = Sudoku(mask)

    def get_mask(self, digit):
        if not self.masks:
            self.update_masks()
        return self.masks[digit]


class DeterministicSolver(StepAndMaskBasedSolver):
    def solve_step(self):
        self.update_masks()
        for square in self.sudoku.squares:
            if square.digit != 0:
                # already solved
                continue

            for digit in range(1, 10):
                mask = self.get_mask(digit)
                if mask.get_square(square.y, square.x).digit == 1:
                    for mask_section in [mask.get_row(square.y),
                                         mask.get_column(square.x),
                                         mask.get_block_of(square.y, square.x)]:
                        if mask_section.count(1) == 1:
                            square.set_digit(digit)


class RandomSolver(StepAndMaskBasedSolver):
    def solve_step(self):
        self.update_masks()
        digit = random.choice(range(1, 10))
        mask = self.get_mask(digit)
        candidates = mask.get_squares_with_digit(1)
        mask_square = random.choice(candidates)
        square = self.sudoku.get_square(mask_square.y, mask_square.x)
        square.set_digit(digit)


class CombinedSolver(StepBasedSolver):
    def __init__(self, sudoku):
        super().__init__(sudoku)
        self.deterministic_solver = DeterministicSolver(sudoku)
        self.random_solver = RandomSolver(sudoku)

    def solve_step(self):
        try:
            self.deterministic_solver.solve()
        except SolvingException:
            self.random_solver.solve_step()
