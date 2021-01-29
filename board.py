import random

import noise

from cell import Cell
from constants import CELL_TYPES
from typing import List


class Field:
    @staticmethod
    def generate_field(size) -> List[List[str]]:
        _seed = random.randint(1, 0xffffff)
        field = [['' for i in range(size)] for i in range(size)]
        for y in range(size):
            for x in range(size):
                v = int((noise.pnoise3(float(x + 50) * 0.3, float(y + 50) * 0.3,
                                       _seed) + 1) * 128)
                typ = CELL_TYPES[0]
                for num, (val, cell_type) in enumerate(CELL_TYPES):
                    if v < val:
                        typ = CELL_TYPES[num - 1]
                        break
                assert typ != -1
                field[x][y] = typ[1]

        return field

    def __init__(self, size, screen, god_mode=0):
        self.sc = screen
        self.sz = size
        self.short_matrix = self.generate_field(size)
        self.long_matrix = [[Cell() for i in range(size)] for i in range(size)]
        for i in range(size):
            for j in range(size):
                tree_coef = (None if self.short_matrix[i][j] in 'wg' else
                             (random.randint(2, 4) if self.short_matrix[i][j] == 'g' else random.randint(4, 8)))
                self.long_matrix[i][j] = Cell(i, j, self.short_matrix[i][j], screen,
                                              tree_coefficient=tree_coef)
                self.long_matrix[i][j].set_visible(3 if god_mode else 0)
        self.cur = 0  # количество ходов с начала игры

    def __getitem__(self, tup):
        x, y = tup
        return self.long_matrix[x][y]

    def debug_print(self):
        print(self.cur)
        for i in self.short_matrix:
            print(i)

    def draw(self):
        cur_player = self.cur % 2
        for i in range(self.sz):
            for j in range(self.sz):
                self.long_matrix[i][j].draw(cur_player)
