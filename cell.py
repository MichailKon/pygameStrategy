from useful_funcs import load_image


class Cell:
    def __init__(self, x=0, y=0, typ='', screen=None, visible_for_first=0, visible_for_second=0,
                 private=0, building=None, unit=None, tree_coefficient=0):
        self._image = {'w': load_image('water.bmp'), 'g': load_image('grass.bmp'),
                       'c': load_image('climbs.bmp'), 's': load_image('sand.bmp'), 'f': load_image('fog.bmp')}

        self._sc = screen
        self._typ = typ
        self._coords = x, y
        self._visible = visible_for_first * 2 + visible_for_second
        self._private = private
        self._building = building
        self._unit = unit
        self._tree_coefficient = tree_coefficient

    @property
    def private(self):
        return self._private

    @property
    def coords(self):
        return self.coords

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
        if player == 0:
            if self._visible > 1:
                self._sc.blit(self._image[self._typ], (x * 70, y * 70))
            else:
                self._sc.blit(self._image['f'], (x * 70, y * 70))
        else:
            if self._visible & 1:
                self._sc.blit(self._image[self._typ], (x * 70, y * 70))
            else:
                self._sc.blit(self._image['f'], (x * 70, y * 70))
