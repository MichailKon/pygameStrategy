import units
from board import Field


class City:
    def __init__(self, player, x, y, field: Field):
        self.pl = player
        self.x = x
        self.y = y
        self.list_of_levels = [x * (x + 3) // 2 for x in range(0, 30)]
        self.cur_lev = 0
        self.level = 1
        self.cell = field[(x, y)]
        self.field = field

    def add_lev(self, inc, in_step, cur_money):
        old = self.level
        self.cur_lev += inc
        for i in range(len(self.list_of_levels)):
            if self.list_of_levels[i] <= self.cur_lev:
                self.level = i + 1
            else:
                break
        if old < self.level:
            self.update(in_step, cur_money)

    def current_level(self):
        return self.level

    def spawn_unit(self, unit):
        self.cell.set_unit(unit)

    def update(self, in_step, cur_money):
        in_step[self.pl - 1] += 1
        if self.level == 2:
            in_step[self.pl - 1] += 2
        if self.level == 3:
            cur_money[self.pl - 1] += 20
        if self.level == 4:
            for i in range(self.x - 2, self.x + 3):
                for j in range(self.y - 2, self.y + 3):
                    if 0 <= i <= 10 and 0 <= j <= 10:
                        if self.field[(i, j)].private() == 0:
                            self.field[(i, j)].set_private([self.pl, self])
        else:
            self.spawn_unit(units.JesusChrist(*self.cell.coords, player=self.pl))


class Village:
    def __init__(self, x, y, field: Field):
        self.x = x
        self.y = y
        self.cell = field[(x, y)]
        self.field = field

    def capture(self, pl):
        # захват
        nan = City(pl, self.cell)
        self.cell.set_building(nan)
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                if 0 <= i <= 10 and 0 <= j <= 10:
                    if self.field[(i, j)].private() == 0:
                        self.field[(i, j)].set_private([pl, nan])


class Forest:
    def __init__(self, x, y, field: Field):
        self.x = x
        self.y = y
        self.cell = field[(x, y)]
        self.field = field

    def cut_down(self, in_step, cur_money):
        near_city = self.cell.private()[1]
        near_city.add_lev(2, in_step, cur_money)
        self.cell.set_building(None)


class LumberHut:
    def __init__(self, in_step, player, x, y, field: Field):
        self.x = x
        self.y = y
        self.cell = field[(x, y)]
        self.field = field
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i <= 10 and 0 <= j <= 10 and isinstance(self.field[(i, j)].building, Forest):
                    in_step[player - 1] += 1


class WindMill:
    def __init__(self, in_step, player, x, y, field: Field):
        self.x = x
        self.y = y
        self.cell = field[(x, y)]
        self.field = field
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i <= 10 and 0 <= j <= 10 and isinstance(self.field[(i, j)].building, WheatFields):
                    in_step[player - 1] += 1


class WheatFields:
    def __init__(self, x, y, field: Field):
        self.x = x
        self.y = y
        self.cell = field[(x, y)]
        self.field = field

    def plough(self, in_step, cur_money):
        near_city = self.cell.private()[1]
        near_city.add_lev(3, in_step, cur_money)
        self.cell.set_building(None)
