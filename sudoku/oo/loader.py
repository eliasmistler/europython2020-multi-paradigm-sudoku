from xml.etree import ElementTree

import requests

from sudoku.oo.base import Sudoku


class OpenSudokuLoader:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.games = []

    def load(self):
        resp = requests.get(f'https://opensudoku.moire.org/sudoku/{self.difficulty}.opensudoku')
        et = ElementTree.fromstring(resp.text)

        self.games = []
        for game in et.findall('game'):
            self.games.append(game.attrib['data'])

    def get_game(self, idx):
        return Sudoku.from_string(self.games[idx])
