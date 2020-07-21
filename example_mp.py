from toolz import thread_last

from sudoku.fp.load import load_opensudoku
from sudoku.fp.solve import combined_step
from sudoku.mp.base import Sudoku
from sudoku.mp.solve import Solver

thread_last(load_opensudoku('easy')[3],
            Sudoku.from_string,
            Solver(combined_step, max_tries=100),
            print)
