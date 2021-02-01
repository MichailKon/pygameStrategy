from constants import FIRST_PLAYER, SECOND_PLAYER
from useful_funcs import load_image, change_color, copy_class
from pygame import Color, Surface, BLEND_RGBA_MULT


class _BaseUnit(object):
    def __init__(self, field, x=0, y=0,
                 hp=10, energy=1, attack_range=1, attack_func=lambda x: x ** 0.5, player=FIRST_PLAYER,
                 second_attack=lambda x: x ** 0.5, defense: float = 0, image_name=''):
        self.field = field
        self._pos_x = x
        self._pos_y = y
        self._can_walk = True
        self._hp = hp
        self._energy = energy
        self._attack_range = attack_range
        self._attack_func = attack_func
        self._player = player
        self._second_attack = second_attack
        self._defense = defense
        self._img = load_image(image_name)
        self._img_size = self._img.get_size()
        self._can_use = True
        if player != FIRST_PLAYER:
            self._img = change_color(self._img, Color('red'))

    def is_alive(self):
        return self._hp > 0

    def can_attack(self, x, y) -> bool:
        if not self._can_use:
            return False
        first = abs(x - self._pos_x)
        second = abs(y - self._pos_y)
        return self.field[x, y].unit is not None and self.field[x, y].unit.player != self.player and max(first, second) <= self._attack_range

    def can_move(self, x, y) -> bool:
        if not self._can_use or not self._can_walk:
            return False
        first = abs(x - self._pos_x)
        second = abs(y - self._pos_y)
        if max(first, second) > self._energy or self.field[x, y].unit is not None or (self.field[x, y].typ in 'cw' and \
                not isinstance(self, JesusChrist)):
            return False
        return True

    def move(self, x, y):
        if not self.can_move(x, y):
            return
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


    def attack(self, enemy, second_strike=False) -> None:
        if not self.can_attack(enemy.pos_x, enemy.pos_y):
            return
        if self._player == enemy.player:
            return
        if not second_strike:
            enemy.get_damage(self._attack_func(self._hp))
        else:
            enemy.get_damage(self._second_attack(self._hp))

        if enemy.is_alive() and not second_strike:
            enemy.attack(self, second_strike=True)
        if not second_strike:
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

    @property
    def set_walk(self):
        self._can_walk = True

    @property
    def set_use(self):
        self._can_use = True

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
    def __init__(self, field, x, y, attack_func=lambda x: x ** 0.5, player=FIRST_PLAYER):
        super().__init__(field, x, y, attack_func=attack_func, player=player, hp=10, energy=1, image_name='warrior.png')


class Archer(_BaseUnit):
    def __init__(self, field, x, y, attack_func=lambda x: x ** 0.5, player=FIRST_PLAYER):
        super().__init__(field, x, y, attack_range=2, attack_func=attack_func,
                         player=player, hp=10, energy=1, image_name='archer.png')


class JesusChrist(_BaseUnit):
    def __init__(self, field, x, y, attack_func=lambda x: x ** 0.5, player=FIRST_PLAYER):
        super().__init__(field, x, y, can_walk=((1 << 3) | (1 << 2) | (1 << 1) | (1 << 0)),
                         attack_func=attack_func, player=player, hp=10, energy=1, image_name='jesus.png')


class ShieldMan(_BaseUnit):
    def __init__(self, field, x, y, attack_func=lambda x: x ** 0.5, player=1):
        super().__init__(field, x, y, attack_func=lambda x: x ** 0.5, player=player, image_name='shield_man.png')


if __name__ == '__main__':
    import pygame
    pygame.init()
    sc = pygame.display.set_mode((800, 700))

    a = Archer(0, 0)
    print(a.img_size)
