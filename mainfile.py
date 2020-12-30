import noise
import pygame
import random
import sys
import os

CELL_TYPES = [(50, 'w'), (125, 's'), (200, 'g'), (256, 'c')]

pygame.init()
sc = pygame.display.set_mode((800, 700))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', 'images', name)
    image = pygame.image.load(fullname)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    if colorkey is not None:
        image = image.convert()
    if colorkey == -1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


_image = {'w': load_image('water.bmp'), 'g': load_image(
    'grass.bmp'), 'c': load_image('climbs.bmp'), 's': load_image('sand.bmp'), 'f': load_image('fog.bmp')}


class Cell:
    def __init__(self, x, y, typ, screen, visible_for_first=0, visible_for_second=0,
                 private=0, buildings=[], unit=None, tree_coefficient=0, ):
        self.sc = screen
        self.typ = typ
        self.coords = x, y
        self.visible = visible_for_first * 2 + visible_for_second
        self.private = private
        self.buildings = buildings

    def draw(self, player):
        x, y = self.coords
        if player == 0:
            if self.visible > 1:
                self.sc.blit(_image[self.typ], (x * 70, y * 70))
            else:
                self.sc.blit(_image['f'], (x * 70, y * 70))
        else:
            if self.visible & 1:
                self.sc.blit(_image[self.typ], (x * 70, y * 70))
            else:
                self.sc.blit(_image['f'], (x * 70, y * 70))


class Field:
    @staticmethod
    def generate_field(size):
        field = [[0 for i in range(size)] for i in range(size)]
        for y in range(size):
            for x in range(size):
                v = int((noise.pnoise3(float(x + 50) * 0.3, float(y + 50) * 0.3,
                                       random.randint(1, 0xffffff)) + 1) * 128)
                for val, cell_type in CELL_TYPES:
                    if v < val:
                        typ = cell_type
                        break
                if v < 100:
                    typ = 'w'  # water
                elif 100 <= v < 120:
                    typ = 's'  # sand
                elif 120 <= v < 190:
                    typ = 'g'  # grass
                else:
                    typ = 'c'  # climbs
                field[x][y] = typ

        return field

    def __init__(self, size, screen, god_mode=0):
        self.sc = screen
        self.sz = size
        self.short_matrix = self.generate_field(size)
        self.long_matrix = [[None for i in range(size)] for i in range(size)]
        for i in range(size):
            for j in range(size):
                tree_coef = (None if self.short_matrix[i][j] in 'wg' else (random.randint(2, 4) if self.short_matrix[i][j] == 'g' else random.randint(4, 8)))
                self.long_matrix[i][j] = Cell(i, j, self.short_matrix[i][j], screen,
                                              tree_coefficient=tree_coef)
                self.long_matrix[i][j].visible = 3 if god_mode else 0
        self.cur = 0  # количество ходов с начала игры

    def debug_print(self):
        print(self.cur)
        for i in self.short_matrix:
            print(i)

    def draw(self):
        cur_player = self.cur % 2
        for i in range(self.sz):
            for j in range(self.sz):
                self.long_matrix[i][j].draw(cur_player)


field = Field(10, sc, god_mode=1)
field.debug_print()
run = 1
while run:
    field.draw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
