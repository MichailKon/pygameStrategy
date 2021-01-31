import pygame
from board import Field
import datetime
from constants import FIRST_PLAYER, SECOND_PLAYER
from units import *
from buildings import *
from cell import Cell


class Query:
    def __init__(self, q_type=None, add_info=None):
        self.q_type = q_type
        self.add_info = add_info
        # 1 = key_down
        # 2 = mouse_down


def get_cell_info(cell: Cell, player):
    sc.fill(pygame.Color('black'))
    print(cell.visible)
    if not cell.visible & (1 << player):
        return [f'Cell: {cell.x, cell.y, "f"}']
    ans = []
    ans.append(f'Cell: {cell.x, cell.y, cell.typ}')
    if cell.unit is not None:
        ans.append(f'Unit: {cell.unit.__class__.__name__}')
        ans.append(f'Unit.hp: {cell.unit.hp}')
    if cell.building is not None:
        ans.append(f'Building: {cell.building.__class__.__name__}')
        if isinstance(cell.building, City):
            ans.append(f'Building.level: {cell.building.level}')
    if cell.private:
        ans.append(f'Private: {cell.private[0]}')
    return ans


def print_cell_info(cell):
    font = pygame.font.Font(None, 30)
    text_coord = 10
    ans = get_cell_info(cell, field.player)
    for i in ans:
        string_rendered = font.render(i, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 12 * 64 + 10
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)


pygame.init()
sc = pygame.display.set_mode((1000, 800))
in_step = [2, 2]
cur_money = [5, 5]

field = Field(12, sc)
field.debug_print()

run = 1
now = datetime.datetime.now()
first_pre_last, second_pre_last = Query(), Query()
first_last, second_last = Query(), Query()
while run:
    # if (datetime.datetime.now() - now).total_seconds() > 2:
    #     now = datetime.datetime.now()
    #     field.next_move()
    field.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            cell = field.get_click(event.pos)
            if field.player == FIRST_PLAYER:
                if first_last.q_type is None or first_last.q_type == 2:
                    print_cell_info(cell)
            else:
                if second_last.q_type is None or second_last.q_type == 2:
                    print_cell_info(cell)
    pygame.display.flip()
