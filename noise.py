# Copyright (c) 2008, Casey Duncan (casey dot duncan at gmail dot com)

from math import floor, fmod, sqrt
from random import randint

# 3D Gradient vectors
_GRAD3 = ((1, 1, 0), (-1, 1, 0), (1, -1, 0), (-1, -1, 0),
          (1, 0, 1), (-1, 0, 1), (1, 0, -1), (-1, 0, -1),
          (0, 1, 1), (0, -1, 1), (0, 1, -1), (0, -1, -1),
          (1, 1, 0), (0, -1, 1), (-1, 1, 0), (0, -1, -1),
          )

# 4D Gradient vectors
_GRAD4 = ((0, 1, 1, 1), (0, 1, 1, -1), (0, 1, -1, 1), (0, 1, -1, -1),
          (0, -1, 1, 1), (0, -1, 1, -1), (0, -1, -1, 1), (0, -1, -1, -1),
          (1, 0, 1, 1), (1, 0, 1, -1), (1, 0, -1, 1), (1, 0, -1, -1),
          (-1, 0, 1, 1), (-1, 0, 1, -1), (-1, 0, -1, 1), (-1, 0, -1, -1),
          (1, 1, 0, 1), (1, 1, 0, -1), (1, -1, 0, 1), (1, -1, 0, -1),
          (-1, 1, 0, 1), (-1, 1, 0, -1), (-1, -1, 0, 1), (-1, -1, 0, -1),
          (1, 1, 1, 0), (1, 1, -1, 0), (1, -1, 1, 0), (1, -1, -1, 0),
          (-1, 1, 1, 0), (-1, 1, -1, 0), (-1, -1, 1, 0), (-1, -1, -1, 0))


_F2 = 0.5 * (sqrt(3.0) - 1.0)
_G2 = (3.0 - sqrt(3.0)) / 6.0
_F3 = 1.0 / 3.0
_G3 = 1.0 / 6.0


class BaseNoise:
    permutation = (151, 160, 137, 91, 90, 15,
                   131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8,
                   99, 37, 240, 21, 10, 23, 190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62,
                   94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33, 88, 237, 149, 56, 87, 174,
                   20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166, 77, 146,
                   158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245,
                   40, 244, 102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187,
                   208, 89, 18, 169, 200, 196, 135, 130, 116, 188, 159, 86, 164, 100, 109, 198,
                   173, 186, 3, 64, 52, 217, 226, 250, 124, 123, 5, 202, 38, 147, 118, 126, 255,
                   82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183,
                   # Welcome to the cum zone
                   170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43,
                   172, 9, 129, 22, 39, 253, 9, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112,
                   104, 218, 246, 97, 228, 251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162,
                   241, 81, 51, 145, 235, 249, 14, 239, 107, 49, 192, 214, 31, 181, 199, 106,
                   157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205,
                   93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180)

    period = len(permutation)
    permutation = permutation * 2

    def __init__(self, period=None, permutation_table=None):
        if period is not None and permutation_table is not None:
            raise ValueError(
                'Can specify either period or permutation_table, not both')
        if period is not None:
            self.randomize(period)
        elif permutation_table is not None:
            self.permutation = tuple(permutation_table) * 2
            self.period = len(permutation_table)

    def randomize(self, period=None):
        if period is not None:
            self.period = period
        perm = list(range(self.period))
        perm_right = self.period - 1
        for i in list(perm):
            j = randint(0, perm_right)
            perm[i], perm[j] = perm[j], perm[i]
        self.permutation = tuple(perm) * 2


def lerp(t, a, b):
    return a + t * (b - a)


def grad3(hash, x, y, z):
    g = _GRAD3[hash % 16]
    return x * g[0] + y * g[1] + z * g[2]


class TileableNoise(BaseNoise):
    def noise3(self, x, y, z, repeat, base=0.0):
        i = int(fmod(floor(x), repeat))
        j = int(fmod(floor(y), repeat))
        k = int(fmod(floor(z), repeat))
        ii = (i + 1) % repeat
        jj = (j + 1) % repeat
        kk = (k + 1) % repeat
        if base:
            i += base
            j += base
            k += base
            ii += base
            jj += base
            kk += base

        x -= floor(x)
        y -= floor(y)
        z -= floor(z)
        fx = x ** 3 * (x * (x * 6 - 15) + 10)
        fy = y ** 3 * (y * (y * 6 - 15) + 10)
        fz = z ** 3 * (z * (z * 6 - 15) + 10)

        perm = self.permutation
        A = perm[i]
        AA = perm[A + j]
        AB = perm[A + jj]
        B = perm[ii]
        BA = perm[B + j]
        BB = perm[B + jj]

        return lerp(fz, lerp(fy, lerp(fx, grad3(perm[AA + k], x, y, z),
                                      grad3(perm[BA + k], x - 1, y, z)),
                             lerp(fx, grad3(perm[AB + k], x, y - 1, z),
                                  grad3(perm[BB + k], x - 1, y - 1, z))),
                    lerp(fy, lerp(fx, grad3(perm[AA + kk], x, y, z - 1),
                                  grad3(perm[BA + kk], x - 1, y, z - 1)),
                         lerp(fx, grad3(perm[AB + kk], x, y - 1, z - 1),
                              grad3(perm[BB + kk], x - 1, y - 1, z - 1))))


def pnoise3(x, y, z):
    return TileableNoise().noise3(x, y, z, BaseNoise().period)
