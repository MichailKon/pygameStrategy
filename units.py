from constants import FIRST_PLAYER
from useful_funcs import load_image, change_color
from pygame import Color, Surface, BLEND_RGBA_MULT


class _BaseUnit:
    def __init__(self, x=0, y=0, can_walk=((0 & (1 << 0)) | (1 & (1 << 1)) | (1 & (1 << 2)) | (0 & (1 << 3))),
                 hp=10, energy=1, attack_range=1, attack_func=lambda x: x ** 0.5, player=FIRST_PLAYER,
                 second_attack=lambda x: x ** 0.5, defense: float = 0, image_name=''):
        self._pos_x = x
        self._pos_y = y
        self._can_walk = can_walk
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
        return max(first, second) <= self._attack_range

    def can_move(self, x, y, ind) -> bool:
        if not self._can_use:
            return False
        first = abs(x - self._pos_x)
        second = abs(y - self._pos_y)
        if max(first, second) > self._energy:
            return False
        if not (self._can_walk & (1 << ind)):
            return False
        return True

    def move(self, x, y, ind):
        if not self.can_move(x, y, ind):
            return
        self._pos_x, self._pos_y = x, y

    def get_damage(self, dmg: float):
        self._hp -= dmg * (1 - self._defense)

    def attack(self, enemy, second_strike=False) -> None:
        assert(issubclass(type(enemy), _BaseUnit))
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
    def __init__(self, x, y, attack_func=lambda x: x ** 0.5, player=FIRST_PLAYER):
        super().__init__(x, y, attack_func=attack_func, player=player, hp=10, energy=1, image_name='warrior.png')


class Archer(_BaseUnit):
    def __init__(self, x, y, attack_func=lambda x: x ** 0.5, player=FIRST_PLAYER):
        super().__init__(x, y, attack_range=2, attack_func=attack_func,
                         player=player, hp=10, energy=1, image_name='archer.png')


class JesusChrist(_BaseUnit):
    def __init__(self, x, y, attack_func=lambda x: x ** 0.5, player=FIRST_PLAYER):
        super().__init__(x, y, can_walk=((1 << 3) | (1 << 2) | (1 << 1) | (1 << 0)),
                         attack_func=attack_func, player=player, hp=10, energy=1, image_name='jesus.png')


class ShieldMan(_BaseUnit):
    def __init__(self, x, y, attack_func=lambda x: x ** 0.5, player=1):
        super().__init__(x, y, attack_func=lambda x: x ** 0.5, player=player, image_name='shield_man.png')


if __name__ == '__main__':
    import pygame
    pygame.init()
    sc = pygame.display.set_mode((800, 700))

    a = Archer(0, 0)
    print(a.img_size)
