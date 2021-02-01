import pygame
from board import Field
import datetime
from constants import FIRST_PLAYER, SECOND_PLAYER
from units import *
from buildings import *
from cell import Cell


def clear_cell_info(cell: Cell):
    pygame.draw.rect(sc, pygame.Color('grey'), (10 * 64 + 10, 70, 300, 400))


def get_cell_info(cell: Cell, player):
    if cell is None:
        return []
    clear_cell_info(cell)
    if not cell.visible & (1 << player):
        print(cell.visible)
        return [f'Cell: {cell.x, cell.y}', 'Cell type: fog']
    ans = []
    ans.append(f'Cell coords: {cell.x, cell.y}')
    ans.append(f'Cell type: {dict([("w", "water"), ("g", "grass"), ("s", "sand"), ("c", "climbs")])[cell.typ]}')
    if cell.unit is not None:
        ans.append(f'Unit: {cell.unit.__class__.__name__}')
        ans.append(f'Unit HP: {cell.unit.hp}')
    if cell.building is not None:
        ans.append(f'Building: {cell.building.__class__.__name__}')
        if isinstance(cell.building, City):
            ans.append(f'Level of Сity: {cell.building.level} ___ 0 \ {cell.building.progress - cell.building.cur_lev}')
    if cell.private:
        ans.append(f'Private: {cell.private[0]}')
    return ans


def print_cell_info(cell):
    font = pygame.font.Font(None, 30)
    text_coord = 70
    ans = get_cell_info(cell, field.player)
    for i in ans:
        string_rendered = font.render(i, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10 * 64 + 10
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)


def print_balance(player):
    global in_step, cur_money
    ans = []
    ans.append(f'Current money: {cur_money[player - 1]}')
    ans.append(f'Money in step: {in_step[player - 1]}')
    font = pygame.font.Font(None, 30)
    text_coord = 10
    pygame.draw.rect(sc, 'grey',
                     (10 * 64 + 10, 0, 200, 70))
    for i in ans:
        string_rendered = font.render(i, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10 * 64 + 10
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)


def del_all_selection():
    for i in range(field.sz):
        for j in range(field.sz):
            field[i, j].select = None


pygame.init()
sc = pygame.display.set_mode((1000, 10 * 64))
fon_img = load_image('fon.png')
skip_img = load_image('skip.png')

run_app = 1
now = datetime.datetime.now()

while run_app:
    local_run = 1
    while local_run and run_app:
        sc.blit(fon_img, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_ESCAPE:
                run_app = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                print(1)
                local_run = 0
    if local_run == 1:
        break

    sc.fill('grey')
    run_game = 1
    in_step = [2, 2]
    cur_money = [5, 5]
    field = Field(10, sc)
    field.debug_print()

    last = None

    while run_game and run_app:
        field.draw()
        sc.blit(skip_img, (1000 - 162, 640 - 40))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_app = 0
            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_ESCAPE:
                run_game = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if -162 <= x - 1000 <= 0 and -40 <= y - 640 <= 0:
                    field.next_move(cur_money, in_step)
                    clear_cell_info(last)
                    last = None
                else:
                    cell = field.get_click(event.pos)
                    if cell is not None:
                        f = 0
                        if cell.select == 1:
                            last.unit.move(cell.x, cell.y)
                            clear_cell_info(cell)
                            f = 1
                            del_all_selection()
                            last = cell
                        elif cell.select == 2:
                            last.unit.attack(cell.x, cell.y)
                            clear_cell_info(cell)
                            del_all_selection()
                            f = 1
                        else:
                            del_all_selection()
                            if cell.unit is not None and cell.unit.player == field.player:
                                for i in range(field.sz):
                                    for j in range(field.sz):
                                        if cell.unit.can_move(i, j) and (i, j) != (cell.x, cell.y):
                                            field[i, j].select_one()
                                        elif cell.unit.can_attack(i, j) and (i, j) != (cell.x, cell.y):
                                            field[i, j].select_two()
                            last = cell
                            clear_cell_info(last)
                        if not f:
                            last = cell
                            clear_cell_info(last)
                    print_cell_info(cell)
                    field.draw()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c and \
                    isinstance(last, Cell) and isinstance(last.building, Forest) and \
                    last.private and last.private[0] == field.player and cur_money[field.player-1] >= 2:
                last.building.cut_down(in_step, cur_money)
                clear_cell_info(last)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p and \
                    isinstance(last, Cell) and isinstance(last.building, WheatFields) and \
                    last.private and last.private[0] == field.player and cur_money[field.player-1] >= 5:
                last.building.plough(in_step, cur_money)
                clear_cell_info(last)
        print_balance(field.player)
        pygame.display.flip()
