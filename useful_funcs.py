import os
import sys
import pygame


def copy_class(c, name=None):
    if not name:
        name = 'CopyOf' + c.__class__.__name__
    if hasattr(c.__class__, '__slots__'):
        slots = c.__class__.__slots__ if type(c.__class__.__slots__) != str else (c.__class__.__slots__,)
        dict_ = dict()
        sloted_members = dict()
        for k, v in c.__class__.__dict__.items():
            if k not in slots:
                dict_[k] = v
            elif type(v) != types.MemberDescriptorType:
                sloted_members[k] = v
        CopyOfc = type(name, c.__class__.__bases__, dict_)
        for k, v in sloted_members.items():
            setattr(CopyOfc, k, v)
        return CopyOfc
    else:
        dict_ = dict(c.__class__.__dict__)
        return type(name, c.__class__.__bases__, dict_)


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
