import random
from typing import List

import noise

from buildings import *
from cell import Cell
from constants import CELL_TYPES, FIRST_PLAYER, SECOND_PLAYER
from useful_funcs import check_in_rect


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

    def __init__(self, size, screen, in_step, cell_size, god_mode=0):
        self.sc = screen
        self.sz = size
        self.cell_size = cell_size
        self.short_matrix = self.generate_field(size)
        self.long_matrix = [[Cell() for i in range(size)] for i in range(size)]
        for i in range(size):
            for j in range(size):
                tree_coef = (None if self.short_matrix[i][j] in 'wg' else
                             (random.randint(2, 4) if self.short_matrix[i][j] == 'g' else random.randint(4, 8)))
                self.long_matrix[i][j] = Cell(i, j, self.short_matrix[i][j], screen,
                                              tree_coefficient=tree_coef, cell_size=self.cell_size)
                self.long_matrix[i][j].set_visible(3 if god_mode else 0)

        for x in range(1, size - 1):
            try:
                for y in range(1, size - 1):
                    if self.long_matrix[x][y].typ in ['s', 'g']:
                        self.long_matrix[x][y].set_building(City(FIRST_PLAYER, x, y, self, start_city=True))
                        in_step[0] += 2
                        assert False
            except AssertionError:
                break

        for x in range(size - 2, 0, -1):
            try:
                for y in range(size - 2, 0, -1):
                    if self.long_matrix[x][y].typ in ['s', 'g']:
                        self.long_matrix[x][y].set_building(City(SECOND_PLAYER, x, y, self, start_city=True))
                        in_step[1] += 2
                        assert False
            except AssertionError:
                break

        for x in range(2, size - 2):
            for y in range(2, size - 2):
                if self.long_matrix[x][y].typ not in ['g', 's']:
                    continue

                castle_near = False
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        x1, y1 = x + dx, y + dy
                        if check_in_rect(x1, y1, x2=self.sz, y2=self.sz) and \
                                (isinstance(self.long_matrix[x1][y1].building, City) or
                                 isinstance(self.long_matrix[x1][y1].building, Village)):
                            castle_near = True
                if castle_near:
                    continue
                if random.randint(1, 20) <= 3:
                    self.long_matrix[x][y].set_building(Village(x, y, self))

        for x in range(size):
            for y in range(size):
                if self.long_matrix[x][y].typ != 'g' or self.long_matrix[x][y].building:
                    continue
                if random.randint(1, 10) <= 2:
                    self.long_matrix[x][y].set_building(Forest(x, y, self))

        for x in range(size):
            for y in range(size):
                if self.long_matrix[x][y].building:
                    continue
                castle_near = False
                for dx in range(-2, 3):
                    for dy in range(-2, 3):
                        x1, y1 = x + dx, y + dy
                        if check_in_rect(x1, y1, x2=self.sz, y2=self.sz) and \
                                (isinstance(self.long_matrix[x1][y1].building, City) or
                                 isinstance(self.long_matrix[x1][y1].building, Village)):
                            castle_near = True
                if self.long_matrix[x][y].typ == 'g':
                    if random.randint(1, 10) <= 3 and castle_near:
                        self.long_matrix[x][y].set_building(WheatFields(x, y, self))
                elif self.long_matrix[x][y].typ == 's':
                    if random.randint(1, 10) <= 1 and castle_near:
                        self.long_matrix[x][y].set_building(WheatFields(x, y, self))

        self.cur = 0  # количество ходов с начала игры
        self.player = FIRST_PLAYER

    def __getitem__(self, tup):
        x, y = tup
        return self.long_matrix[x][y]

    def debug_print(self):
        print(self.cur)
        for i in self.short_matrix:
            print(i)

    def draw(self):
        for i in range(self.sz):
            for j in range(self.sz):
                self.long_matrix[i][j].draw(self.player)

    def next_move(self, cur_money, in_step):
        for i in range(self.sz):
            for j in range(self.sz):
                if self[i, j].unit is not None:
                    self[i, j].unit.set_use()
                    self[i, j].unit.set_walk()
                    self[i, j].select = None
        self.cur += 1
        cur_money[self.player - 1] += in_step[self.player - 1]
        self.player = FIRST_PLAYER if self.player == SECOND_PLAYER else SECOND_PLAYER

    def get_cell(self, mouse_pos: tuple) -> None or tuple:
        try:
            x = mouse_pos[1] // self.cell_size
            y = mouse_pos[0] // self.cell_size
            if not check_in_rect(x, y, x2=self.sz, y2=self.sz):
                return None
        except IndexError:
            print('Что-то не так с mousePos')
            return None
        except ZeroDivisionError:
            print('Размер клетки 0')
            return None
        except Exception as e:
            print(e.__name__)
            print(e)
            return None
        return y, x

    def on_click(self, x, y):
        return self.long_matrix[x][y]

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        if cell_coords is None or len(cell_coords) != 2:
            return
        return self.on_click(*cell_coords)
