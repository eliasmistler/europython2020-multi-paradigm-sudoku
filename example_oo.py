from sudoku.oo.loader import OpenSudokuLoader
from sudoku.oo.solver import CombinedSolver, DeterministicSolver, RandomSolver

easy_loader = OpenSudokuLoader('easy')
easy_loader.load()

hard_loader = OpenSudokuLoader('very_hard')
hard_loader.load()

sudoku = easy_loader.get_game(5)
print(sudoku)
solver = DeterministicSolver(sudoku)
solver.solve()
print(sudoku)

sudoku = easy_loader.get_game(6)
print(sudoku)
solver = RandomSolver(sudoku)
solver.solve_step()
print(sudoku)

sudoku = hard_loader.get_game(2)
print(sudoku)
solver = CombinedSolver(sudoku)
solver.repeat_solve()  # may need multiple tries because of randomness
print(sudoku)
