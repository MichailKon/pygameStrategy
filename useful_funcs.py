import os
import sys

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


def change_color(image, color):
    img = image.copy()
    img.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    img.fill(color, None, pygame.BLEND_RGB_ADD)

    return img
