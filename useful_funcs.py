import os
import sys
from constants import FIELD_SIZE

import pygame


def load_image(name, colorkey=None) -> pygame.image:
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


def change_color(image, color, find=(0, 0, 0)):
    img = image.copy()
    img.fill(find, None, pygame.BLEND_RGBA_MULT)
    img.fill(color, None, pygame.BLEND_RGB_ADD)

    return img


def check_in_rect(i, j, x1=0, y1=0, x2=FIELD_SIZE, y2=FIELD_SIZE):
    return x1 <= i < x2 and y1 <= j < y2
