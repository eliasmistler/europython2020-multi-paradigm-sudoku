import numpy as np
import requests
import xmltodict
from toolz import get_in, interpose, map, pluck, thread_last


def parse_raw(raw_sudoku):
    raw_sudoku = raw_sudoku.strip().replace('\n', '')
    return np.array(list(map(int, raw_sudoku)), dtype='int64').reshape((9, 9))


def load_opensudoku(difficulty):
    resp = requests.get(f'https://opensudoku.moire.org/sudoku/{difficulty}.opensudoku')
    parsed = xmltodict.parse(resp.text)
    return thread_last(parsed,
                       (get_in, ['opensudoku', 'game']),
                       (pluck, '@data'),
                       tuple)


def format_sudoku(sudoku):
    def format_row(row):
        return '| ' + ' | '.join(map(lambda s: str(s) if s else ' ', row)) + ' |'

    row_delim = '+---+---+---+---+---+---+---+---+---+'
    formatted_rows = map(format_row, sudoku)
    print_lines = (row_delim, *interpose(row_delim, formatted_rows), row_delim)
    return '\n'.join(print_lines)
