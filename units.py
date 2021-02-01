from constants import FIRST_PLAYER, SECOND_PLAYER
from useful_funcs import load_image, change_color, copy_class
from pygame import Color, Surface, BLEND_RGBA_MULT


class _BaseUnit(object):
    def __init__(self, field, x=0, y=0,
                 hp=10, energy=1, attack_range=1, potential_attack=5, player=FIRST_PLAYER,
                 potential_second_attack=5, attack_func=lambda hp, max_hp, p: max(0.6, hp / max_hp) * p,
                 defense: float = 0, image_name=''):
        self.field = field
        self._pos_x = x
        self._pos_y = y
        self._can_walk = True
        self._hp = hp
        self._max_hp = hp
        self._energy = energy
        self._attack_range = attack_range
        self._attack_func = attack_func
        self._player = player
        self._attack = potential_attack
        self._second_attack = potential_second_attack
        self._defense = defense
        self._img = load_image(image_name)
        self._img_size = self._img.get_size()
        self._can_use = True
        if player != FIRST_PLAYER:
            self._img = change_color(self._img, Color('red'))

    def die(self):
        self.field[self._pos_x, self._pos_y].set_unit(None)
        del self

    def is_alive(self):
        return self._hp > 0

    def can_attack(self, x, y) -> bool:
        if not self._can_use:
            return False
        first = abs(x - self._pos_x)
        second = abs(y - self._pos_y)
        return self.field[x, y].unit is not None and self.field[x, y].unit.player != self.player and \
                max(first, second) <= self._attack_range and not isinstance(self, JesusChrist)

    def check_energy(self):
        if not self._can_use or not self._can_walk:
            return False
        return True

    def can_move(self, x, y, check_energy=True) -> bool:
        if check_energy:
            if not self.check_energy():
                return False
        first = abs(x - self._pos_x)
        second = abs(y - self._pos_y)
        if max(first, second) > self._energy or self.field[x, y].unit is not None or \
                (self.field[x, y].typ in 'cw' and not isinstance(self, JesusChrist)):
            return False
        return True

    def move(self, x, y):
        old_x, old_y = self.pos_x, self.pos_y
        self.field[x, y].set_unit(self)
        self.field[x, y].unit.set_pos_x(x)
        self.field[x, y].unit.set_pos_y(y)
        self.field[old_x, old_y].set_unit(None)
        for i in range(self.pos_x - 1, self.pos_x + 1 + 1):
            for j in range(self.pos_y - 1, self.pos_y + 1 + 1):
                if 0 <= i < self.field.sz and 0 <= j < self.field.sz:
                    self.field[i, j].set_visible(self.field[i, j].visible
                                                 | ((1 << FIRST_PLAYER) if self.field.player == FIRST_PLAYER
                                                    else (1 << SECOND_PLAYER)))
        self._can_walk = False

    def get_damage(self, dmg: float):
        self._hp -= dmg * (1 - self._defense)

    def attack(self, x, y, second_strike=False) -> None:
        enemy = self.field[x, y].unit
        if not second_strike:
            enemy.get_damage(self._attack_func(self._hp, self._max_hp, self._attack))
        else:
            enemy.get_damage(self._attack_func(self._hp, self._max_hp, self._second_attack))
        if not enemy.is_alive() and not second_strike and not isinstance(self, Archer) and self.can_move(x, y, False):
            self.move(x, y)
            return
        elif not enemy.is_alive():
            enemy.die()
            self._can_use = False
            return

        if enemy.is_alive() and not second_strike:
            if enemy.can_attack(self.pos_x, self.pos_y):
                enemy.attack(self.pos_x, self.pos_y, second_strike=True)
        self._can_use = False

    @property
    def can_use(self):
        return self._can_use

    @property
    def pos_x(self):
        return self._pos_x

    @property
    def pos_y(self):
        return self._pos_y

    @property
    def attack_range(self):
        return self._attack_range

    @property
    def hp(self):
        return self._hp

    @property
    def energy(self):
        return self._energy

    @property
    def player(self):
        return self._player

    def set_walk(self, new_val=True):
        self._can_walk = new_val

    def set_use(self, new_val=True):
        self._can_use = new_val

    @property
    def img(self):
        return self._img

    def set_pos_x(self, x):
        self._pos_x = x

    def set_pos_y(self, y):
        self._pos_y = y

    @property
    def img_size(self):
        return self._img_size


class Warrior(_BaseUnit):
    def __init__(self, field, x, y, player=FIRST_PLAYER):
        super().__init__(field, x, y, player=player, hp=10, energy=1, image_name='warrior.png')


class Archer(_BaseUnit):
    def __init__(self, field, x, y, player=1):
        super().__init__(field, x, y, attack_range=2,
                         player=player, hp=10, energy=1, image_name='archer.png')


class JesusChrist(_BaseUnit):
    def __init__(self, field, x, y, player=1):
        super().__init__(field, x, y, player=player, hp=20, energy=2, image_name='jesus.png', potential_attack=0,
                         potential_second_attack=0)


class ShieldMan(_BaseUnit):
    def __init__(self, field, x, y, player=1):
        super().__init__(field, x, y, player=player, image_name='shield_man.png', potential_attack=3,
                         potential_second_attack=7, defense=0.3)


if __name__ == '__main__':
    import pygame

    pygame.init()
    sc = pygame.display.set_mode((800, 700))

    a = Archer(0, 0)
    print(a.img_size)
