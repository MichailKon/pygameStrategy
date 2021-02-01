import units
from constants import FIRST_PLAYER, SECOND_PLAYER
from useful_funcs import load_image, change_color
from pygame import Color


class _BaseCity:
    def __init__(self, x, y, field, filename: str):
        self.x, self.y = x, y
        self.field = field
        self.cell = field[(x, y)]
        self.img = load_image(filename)


class City(_BaseCity):
    def __init__(self, player, x, y, field, start_city=False):
        super().__init__(x, y, field, 'city.png')
        self.pl = player
        self.list_of_levels = [x * (x + 5) // 2 for x in range(0, 30)]
        self.cur_lev = 0
        self.level = 1
        self.make_private(1, 1)
        if start_city:
            self.spawn_unit(units.Warrior(field, x, y, player=player))
        self.img = change_color(self.img, Color('white'))

    def make_private(self, len1, len2):
        for i in range(self.x - len1, self.x + len2 + 1):
            for j in range(self.y - len1, self.y + len2 + 1):
                if 0 <= i < self.field.sz and 0 <= j < self.field.sz:
                    if not self.field[(i, j)].private:
                        self.field[(i, j)].set_private([self.pl, self])
                    self.field[i, j].set_visible(self.field[i, j].visible
                                                 | ((1 << FIRST_PLAYER) if self.pl == FIRST_PLAYER
                                                    else (1 << SECOND_PLAYER)))

    @property
    def progress(self):
        for i in range(len(self.list_of_levels)):
            if self.list_of_levels[i] <= self.cur_lev:
                self.level = i + 1
            else:
                return self.list_of_levels[i]

    def add_lev(self, inc, in_step):
        old = self.level
        self.cur_lev += inc
        for i in range(len(self.list_of_levels)):
            if self.list_of_levels[i] <= self.cur_lev:
                self.level = i + 1
            else:
                break
        if old < self.level:
            self.update(in_step)

    def current_level(self):
        return self.level

    def spawn_unit(self, unit):
        self.cell.set_unit(unit)

    def update(self, in_step):
        in_step[self.pl - 1] += 1
        if self.level == 2:
            in_step[self.pl - 1] += 2
        elif self.level == 3:
            self.make_private(2, 2)
        elif self.level > 3:
            self.spawn_unit(units.JesusChrist(self.field, *self.cell.coords, player=self.pl))


class Village(_BaseCity):
    def __init__(self, x, y, field):
        super().__init__(x, y, field, 'village.png')

    def capture(self, pl):
        # захват
        nan = City(pl, self.cell.x, self.cell.y, self.field)
        self.cell.set_building(nan)
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if 0 <= i <= 10 and 0 <= j <= 10:
                    if self.field[(i, j)].private == 0:
                        self.field[(i, j)].set_private([pl, nan])


class Forest(_BaseCity):
    def __init__(self, x, y, field):
        super().__init__(x, y, field, 'forest.png')

    def cut_down(self, in_step, cur_money):
        near_city = self.cell.private[1]
        near_city.add_lev(2, in_step)
        self.cell.set_building(None)
        cur_money[self.cell.private[0] - 1] -= 2


class LumberHut(_BaseCity):
    def __init__(self, in_step, player, x, y, field):
        super().__init__(x, y, field, 'lumberhut.png')
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i <= 10 and 0 <= j <= 10 and isinstance(self.field[(i, j)].building, Forest):
                    in_step[player - 1] += 1


class WindMill(_BaseCity):
    def __init__(self, in_step, player, x, y, field):
        super().__init__(x, y, field, 'windmill.png')
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i <= 10 and 0 <= j <= 10 and isinstance(self.field[(i, j)].building, WheatFields) and \
                        self.field[i, j].worked:
                    in_step[player - 1] += 1


class WheatFields(_BaseCity):
    def __init__(self, x, y, field):
        super().__init__(x, y, field, 'wheat.png')
        self.worked = 0

    def plough(self, in_step, cur_money):
        near_city = self.cell.private[1]
        near_city.add_lev(3, in_step)
        cur_money[self.cell.private[0]-1] -= 5
        self.img = load_image('worked_wheat.png')
        self.worked = 1
