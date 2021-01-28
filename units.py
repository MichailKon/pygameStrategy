from constants import CELL_TYPES


class _BaseUnit:
    def __init__(self, x=0, y=0, can_walk=((0 & (1 << 0)) | (1 & (1 << 1)) | (1 & (1 << 2)) | (0 & (1 << 3))),
                 hp=10, energy=1, attack_range=1, attack_func=lambda x: x**0.5, player=1):
        self._pos_x = x
        self._pos_y = y
        self._can_walk = can_walk
        self._hp = hp
        self._energy = energy
        self._attack_range = attack_range
        self._attack_func = attack_func
        self._player = player

    def is_alive(self):
        return self._hp > 0

    def can_attack(self, x, y) -> bool:
        first = abs(x - self._pos_x)
        second = abs(y - self._pos_y)
        return max(first, second) == self._attack_range

    def can_move(self, x, y, typ) -> bool:
        first = abs(x - self._pos_x)
        second = abs(y - self._pos_y)
        if max(first, second) > self._energy:
            return False
        ind = 0
        while CELL_TYPES[ind][1] != typ:
            ind += 1
        if not (self._can_walk & (1 << ind)):
            return False
        return True

    def get_damage(self, dmg: float):
        self._hp -= dmg

    def attack(self, enemy, second_strike=False) -> None:
        assert(issubclass(type(enemy), _BaseUnit))
        if not self.can_attack(enemy.pos_x, enemy.pos_y):
            return
        if self._player == enemy.player:
            return
        enemy.get_damage(self._attack_func(self._hp))

        if enemy.is_alive() and not second_strike:
            enemy.attack(self, second_strike=True)

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

    def set_pos_x(self, x):
        self._pos_x = x

    def set_pos_y(self, y):
        self._pos_y = y


class Warrior(_BaseUnit):
    def __init__(self, x, y, hp=10, attack_func=lambda x: x**0.5, player=1, energy=1):
        super().__init__(x, y, attack_func=attack_func, player=player, hp=hp, energy=energy)


class Archer(_BaseUnit):
    def __init__(self, x, y, hp=10, attack_func=lambda x: x**0.5, player=1, energy=1):
        super().__init__(x, y, attack_range=2, attack_func=attack_func, player=player, hp=hp, energy=energy)


class JesusChrist(_BaseUnit):
    def __init__(self, x, y, hp=10, attack_func=lambda x: x**0.5, player=1, energy=1):
        super().__init__(x, y, can_walk=((1 << 3) | (1 << 2) | (1 << 1) | (1 << 0)),
                         attack_func=attack_func, player=player, hp=hp, energy=energy)
