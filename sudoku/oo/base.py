from abc import ABC
from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class Square:
    """
    Represents a single-digit square on the Sudoku field
    """
    y: int
    x: int
    digit: int = 0
    locked: bool = False

    def set_digit(self, digit):
        if self.digit != 0 and self.locked and digit != self.digit:
            raise Exception('Digit is locked and already set!')
        self.digit = digit


@dataclass
class SquaresCollection(ABC):
    """
    Any collection of squares
    """
    squares: List[Square]

    def count(self, digit: int):
        result = 0
        for square in self.squares:
            if square.digit == digit:
                result += 1
        return result

    @property
    def remaining_blanks(self):
        return self.count(0)


class Row(SquaresCollection):
    def __repr__(self):
        string_numbers = [str(square.digit) if square.digit else ' ' for square in self.squares]
        return '| ' + ' | '.join(string_numbers) + ' |'


class Column(SquaresCollection):
    pass


class Block(SquaresCollection):
    pass


class Sudoku(SquaresCollection):
    rows: List[Row]
    cols: List[Column]
    blocks: List[Block]
    squares: List[Square]

    @classmethod
    def from_string(cls, raw):
        values = []
        for idx, digit in enumerate(raw):
            values.append(int(digit))
        values = np.array(values, dtype='int64').reshape((9, 9))
        return cls(values)

    def __init__(self, values=None):
        values = values if values is not None else np.zeros(9, 9)
        rows = [[] for _ in range(9)]
        cols = [[] for _ in range(9)]
        blocks = [[] for _ in range(9)]
        self.squares = []

        # create rows / cols / blocks up-front as collections
        for y, value_row in enumerate(values):
            for x, digit in enumerate(value_row):
                square = Square(y, x, digit, locked=(digit != 0))
                self.squares.append(square)
                rows[y].append(square)
                cols[x].append(square)
                blocks[(y // 3) * 3 + (x // 3)].append(square)

        self.rows = [Row(row) for row in rows]
        self.cols = [Column(col) for col in cols]
        self.blocks = [Block(block) for block in blocks]

    @property
    def is_solved(self):
        return self.remaining_blanks == 0

    def get_squares_with_digit(self, digit):
        empty_squares = []
        for square in self.squares:
            if square.digit == digit:
                empty_squares.append(square)
        return empty_squares

    def get_row(self, y):
        return self.rows[y]

    def get_column(self, x):
        return self.cols[x]

    def get_square(self, y, x):
        return self.squares[y * 9 + x]

    def get_block_of(self, y, x):
        return self.blocks[(y // 3) * 3 + (x // 3)]

    def __repr__(self):
        row_delim = '+---+---+---+---+---+---+---+---+---+'
        print_lines = [row_delim]
        for row in self.rows:
            print_lines.append(repr(row))
            print_lines.append(row_delim)

        return '\n'.join(print_lines)
