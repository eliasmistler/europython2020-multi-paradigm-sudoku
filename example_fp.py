from sudoku.fp.load import format_sudoku, load_opensudoku, parse_raw
from sudoku.fp.solve import repeat_solve, solve_combined, solve_deterministic

easy_raws = load_opensudoku('easy')
hard_raws = load_opensudoku('very_hard')

sudoku = parse_raw(easy_raws[5])
solved = solve_deterministic(sudoku)
print(format_sudoku(sudoku))
print(format_sudoku(solved))

sudoku = parse_raw(hard_raws[3])
solved = repeat_solve(sudoku, solve_combined)
print(format_sudoku(sudoku))
print(format_sudoku(solved))
