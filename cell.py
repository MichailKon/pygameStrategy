from useful_funcs import load_image
from constants import FIRST_PLAYER, SECOND_PLAYER


class Cell:
    def __init__(self, x=0, y=0, typ='', screen=None, visible_for_first=0, visible_for_second=0,
                 private=None, building=None, unit=None, tree_coefficient=0, cell_size=64):
        self._image = {'w': load_image('water.bmp'), 'g': load_image('grass.bmp'),
                       'c': load_image('climbs.bmp'), 's': load_image('sand.bmp'), 'f': load_image('fog.bmp')}
        self.select = None
        self.sel_move = load_image('blue_target.png', colorkey=-1)
        self.sel_target = load_image('red_target.png', colorkey=-1)
        self._sc = screen
        self._typ = typ
        self._coords = x, y
        self._visible = visible_for_first * 2 + visible_for_second
        self._private = private
        self._building = building
        self._unit = unit
        self._tree_coefficient = tree_coefficient
        self._cell_size = cell_size

    @property
    def private(self):
        return self._private

    @property
    def coords(self):
        return self._coords

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]

    @property
    def unit(self):
        return self._unit

    @property
    def visible(self):
        return self._visible

    @property
    def building(self):
        return self._building

    def set_unit(self, unit):
        self._unit = unit

    def set_building(self, building):
        self._building = building

    def set_visible(self, visible):
        self._visible = visible

    def set_private(self, private):
        self._private = private

    def draw(self, player):
        x, y = self.coords
        if self._visible & (1 << player):
            self._sc.blit(self._image[self._typ], (x * self._cell_size, y * self._cell_size))
        else:
            self._sc.blit(self._image['f'], (x * self._cell_size, y * self._cell_size))
        if self._building is not None:
            if self._visible & (1 << player):
                self._sc.blit(self._building.img, (x * self._cell_size, y * self._cell_size))
        if self._unit is not None:
            if self._visible & (1 << player):
                dx, dy = self.unit.img_size
                pos_x, pos_y = ((x + 1) * self._cell_size - 1 - dx, (y + 1) * self._cell_size - 1 - dy)
                self._sc.blit(self._unit.img, (pos_x, pos_y))
        if self.select is not None:
            if self.select == 2:
                self._sc.blit(self.sel_target, (x * self._cell_size, y * self._cell_size))
            else:
                self._sc.blit(self.sel_move, (x * self._cell_size, y * self._cell_size))

    def select_one(self):
        self.select = 1

    def select_two(self):
        self.select = 2

    @property
    def typ(self):
        return self._typ
