import os
import random

import pygame

from board import Field
from buildings import *
from cell import Cell
from constants import CELL_SIZE, SKIP_BUTTON_X, SKIP_BUTTON_Y, SKIP_BUTTON_WIDTH, SKIP_BUTTON_HEIGHT, \
    FIELD_SIZE
from useful_funcs import check_in_rect
from units import *


def clear_cell_info():
    pygame.draw.rect(sc, pygame.Color('grey'), (10 * CELL_SIZE + 10, 70, 300, 400))


def get_cell_info(cell: Cell, player):
    if cell is None:
        return []
    clear_cell_info()
    if not cell.visible & (1 << player):
        return [f'Cell: {cell.x, cell.y}', 'Cell type: fog']
    ans = [f'Cell coords: {cell.x, cell.y}',
           f'Cell type: {dict([("w", "water"), ("g", "grass"), ("s", "sand"), ("c", "climbs")])[cell.typ]}']
    if cell.unit is not None:
        ans.append(f'Unit: {cell.unit.__class__.__name__}')
        ans.append(f'Unit HP: {cell.unit.hp}')
    if cell.building is not None:
        ans.append(f'Building: {cell.building.__class__.__name__}')
        if isinstance(cell.building, City):
            ans.append(f'Level of Сity: {cell.building.level} remained'
                       f':{cell.building.progress - cell.building.cur_lev}')
            ans.append(f'units: {cell.building.count_of_units}/{cell.building.max_units_count}')
    if cell.private:
        ans.append(f'Private: {cell.private[0]}')
    return ans


def print_cell_info(cell: Cell):
    font = pygame.font.Font(None, 30)
    text_coord = 70
    ans = get_cell_info(cell, field.player)
    for i in ans:
        string_rendered = font.render(i, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10 * CELL_SIZE + 10
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)


def print_balance(player):
    global in_step, cur_money
    ans = [f'Current money: {cur_money[player - 1]}', f'Money in step: {in_step[player - 1]}']
    font = pygame.font.Font(None, 30)
    text_coord = 10
    pygame.draw.rect(sc, 'grey',
                     (10 * CELL_SIZE + 10, 0, 200, 70))
    for i in ans:
        string_rendered = font.render(i, True, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10 * CELL_SIZE + 10
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)


def del_all_selection():
    for i in range(field.sz):
        for j in range(field.sz):
            field[i, j].select = None


def del_all_capturing():
    for i in range(field.sz):
        for j in range(field.sz):
            if isinstance(field[i, j].building, Village) or isinstance(field[i, j].building, City):
                field[i, j].building.is_capture = False


def draw_borders():
    for i in range(field.sz):
        for j in range(field.sz):
            if not field[i, j].visible & (1 << field.player):
                continue
            if field[i, j].private and field[i, j].private[0]:
                p = field[i, j].private[0]
                if p == 1:
                    if i == 0:
                        sc.blit(field[i, j].im['l1'], (i * CELL_SIZE, j * CELL_SIZE))
                    if j == 0:
                        sc.blit(field[i, j].im['u1'], (i * CELL_SIZE, j * CELL_SIZE))
                    if i == field.sz - 1:
                        sc.blit(field[i, j].im['r1'], (i * CELL_SIZE, j * CELL_SIZE))
                    if j == field.sz - 1:
                        sc.blit(field[i, j].im['d1'], (i * CELL_SIZE, j * CELL_SIZE))
                else:
                    if i == 0:
                        sc.blit(field[i, j].im['l2'], (i * CELL_SIZE, j * CELL_SIZE))
                    if j == 0:
                        sc.blit(field[i, j].im['u2'], (i * CELL_SIZE, j * CELL_SIZE))
                    if i == field.sz - 1:
                        sc.blit(field[i, j].im['r2'], (i * CELL_SIZE, j * CELL_SIZE))
                    if j == field.sz - 1:
                        sc.blit(field[i, j].im['d2'], (i * CELL_SIZE, j * CELL_SIZE))
    for i in range(field.sz - 1):
        for j in range(field.sz):
            if not field[i, j].visible & (1 << field.player):
                continue
            if field[i, j].private:
                p = field[i, j].private[0]
                if p == 1:
                    if not field[i + 1, j].private or field[i + 1, j].private[0] != 1:
                        sc.blit(field[i, j].im['r1'], (i * CELL_SIZE, j * CELL_SIZE))
                else:
                    if not field[i + 1, j].private or field[i + 1, j].private[0] != 2:
                        sc.blit(field[i, j].im['r2'], (i * CELL_SIZE, j * CELL_SIZE))

    for i in range(field.sz):
        for j in range(field.sz - 1):
            if not field[i, j].visible & (1 << field.player):
                continue
            if field[i, j].private:
                p = field[i, j].private[0]
                if p == 1:
                    if not field[i, j + 1].private or field[i, j + 1].private[0] != 1:
                        sc.blit(field[i, j + 1].im['d1'], (i * CELL_SIZE, j * CELL_SIZE))
                else:
                    if not field[i, j + 1].private or field[i, j + 1].private[0] != 2:
                        sc.blit(field[i, j].im['d2'], (i * CELL_SIZE, j * CELL_SIZE))

    for i in range(1, field.sz):
        for j in range(field.sz):
            if not field[i, j].visible & (1 << field.player):
                continue
            if field[i, j].private:
                p = field[i, j].private[0]
                if p == 1:
                    if not field[i - 1, j].private or field[i - 1, j].private[0] != 1:
                        sc.blit(field[i, j].im['l1'], (i * CELL_SIZE, j * CELL_SIZE))
                else:
                    if not field[i - 1, j].private or field[i - 1, j].private[0] != 2:
                        sc.blit(field[i, j].im['l2'], (i * CELL_SIZE, j * CELL_SIZE))

    for i in range(field.sz):
        for j in range(1, field.sz):
            if not field[i, j].visible & (1 << field.player):
                continue
            if field[i, j].private:
                p = field[i, j].private[0]
                if p == 1:
                    if not field[i, j - 1].private or field[i, j - 1].private[0] != 1:
                        sc.blit(field[i, j - 1].im['u1'], (i * CELL_SIZE, j * CELL_SIZE))
                else:
                    if not field[i, j - 1].private or field[i, j - 1].private[0] != 2:
                        sc.blit(field[i, j].im['u2'], (i * CELL_SIZE, j * CELL_SIZE))


def make_next_move():
    field.next_move(cur_money, in_step)
    del_all_selection()
    del_all_capturing()
    clear_cell_info()
    for i in range(field.sz):
        for j in range(field.sz):
            if field[i, j].typ == 'g' and not field[i, j].building:
                if random.randint(1, 20) == 1:
                    field[i, j].set_building(Forest(i, j, field))
                    for k in range(i - 1, i + 2):
                        for l in range(j - 1, j + 2):
                            if check_in_rect(k, l) and isinstance(field[k, l].building, LumberHut):
                                in_step[field[k, l].private[0] - 1] += 1
                                field[k, l].private[1].doxod += 1
            if field[i, j].unit and (
                    isinstance(field[i, j].building, City) and
                    field[i, j].unit.player != field[i, j].building.pl or
                    isinstance(field[i, j].building, Village)):
                field[i, j].building.is_capture = True


def game_end(text_coord, ans):
    win_image = load_image('win_black.png')
    font = pygame.font.Font(None, 60)
    sc.blit(win_image, (0, 0))

    for i in ans:
        string_rendered = font.render(i, True, pygame.Color('blue'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 25
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)


pygame.init()
pygame.display.set_caption('Half-battle of Polytopia')
sc = pygame.display.set_mode((1000, FIELD_SIZE * CELL_SIZE))
fon_img = load_image('fon.png')
skip_img = load_image('skip.png')

run_app = 1

while run_app:
    pygame.mixer.music.stop()
    local_run = 1
    while local_run and run_app:
        sc.blit(fon_img, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_ESCAPE:
                run_app = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                local_run = 0
    if local_run == 1:
        break

    sc.fill('grey')
    run_game = 1
    in_step = [0, 0]
    cur_money = [5, 5]
    field = Field(FIELD_SIZE, sc, in_step, cell_size=CELL_SIZE, god_mode=0)

    pygame.mixer.music.load(os.path.join('data', 'music', 'main_music.mp3'))
    pygame.mixer.music.play()

    last = None
    while run_game > 0 and run_app:
        field.draw()
        draw_borders()
        sc.blit(skip_img, (SKIP_BUTTON_X - SKIP_BUTTON_WIDTH, SKIP_BUTTON_Y - SKIP_BUTTON_HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_app = 0
            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_ESCAPE:
                run_game = 0
            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_RETURN:
                make_next_move()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if check_in_rect(x - SKIP_BUTTON_X, y - SKIP_BUTTON_Y, -SKIP_BUTTON_WIDTH, -SKIP_BUTTON_HEIGHT, 0, 0):
                    make_next_move()
                else:
                    cell = field.get_click(event.pos)
                    if cell is not None:
                        f = 0
                        if cell.select == 1:
                            last.unit.move(cell.x, cell.y)
                            clear_cell_info()
                            f = 1
                            del_all_selection()
                            if (isinstance(last.building, Village) or isinstance(last.building, City)) and \
                                    last.building.is_capture:
                                last.building.is_capture = False
                            last = cell
                        elif cell.select == 2:
                            plx = last.unit.player
                            ply = cell.unit.player
                            last.unit.attack(cell.x, cell.y)
                            clear_cell_info()
                            del_all_selection()
                            if (isinstance(last.building, Village) or isinstance(last.building, City)) and \
                                    last.building.is_capture and (
                                    not last.unit or last.unit and last.unit.player != plx):
                                last.building.is_capture = False
                            if (isinstance(cell.building, Village) or isinstance(cell.building, City)) and \
                                    cell.building.is_capture and (
                                    not cell.unit or cell.unit and cell.unit.player != ply):
                                cell.building.is_capture = False
                            f = 1
                        else:
                            del_all_selection()
                            cell.select_three()
                            if cell.unit is not None and cell.unit.player == field.player:
                                for i in range(field.sz):
                                    for j in range(field.sz):
                                        if cell.unit.can_move(i, j) and (i, j) != (cell.x, cell.y) and \
                                                field[i, j].visible & (1 << field.player):
                                            field[i, j].select_one()
                                        elif cell.unit.can_attack(i, j) and (i, j) != (cell.x, cell.y) and \
                                                field[i, j].visible & (1 << field.player):
                                            field[i, j].select_two()
                            last = cell
                            clear_cell_info()
                        if not f:
                            last = cell
                            clear_cell_info()
                    print_cell_info(cell)
                    field.draw()
                    draw_borders()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_c and \
                    isinstance(last, Cell) and isinstance(last.building, Forest) and \
                    last.private and last.private[0] == field.player and cur_money[field.player - 1] >= 2:
                for i in range(last.x - 1, last.x + 2):
                    for j in range(last.y - 1, last.y + 2):
                        if check_in_rect(i, j) and isinstance(field[i, j].building, LumberHut):
                            in_step[field[i, j].private[0] - 1] -= 1
                            field[i, j].private[1].doxod -= 1
                last.building.cut_down(in_step, cur_money)
                clear_cell_info()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p and \
                    isinstance(last, Cell) and isinstance(last.building, WheatFields) and \
                    last.private and last.private[0] == field.player and cur_money[field.player - 1] >= 5:
                last.building.plough(in_step, cur_money)
                for i in range(last.x - 1, last.x + 2):
                    for j in range(last.y - 1, last.y + 2):
                        if check_in_rect(i, j) and isinstance(field[i, j].building, WindMill):
                            in_step[field[i, j].private[0] - 1] += 2
                            field[i, j].private[1].doxod += 2
                clear_cell_info()

            can_spawn = isinstance(last, Cell) and isinstance(last.building, City)
            if can_spawn and last.private and last.unit \
                    is None:
                can_spawn &= last.private[0] == field.player
            else:
                can_spawn = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a and can_spawn and \
                    cur_money[field.player - 1] >= 10 and last.building.current_level() >= 3 and \
                    last.building.count_of_units < last.building.max_units_count:
                new_unit = Archer(field, last.x, last.y, player=field.player, city=last.building)
                new_unit.set_use(False)
                del_all_selection()
                last.set_unit(new_unit)
                last.building.count_of_units += 1
                cur_money[field.player - 1] -= 10
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w and can_spawn and \
                    cur_money[field.player - 1] >= 5 and last.building.current_level() >= 1 and \
                    last.building.count_of_units < last.building.max_units_count:
                new_unit = Warrior(field, last.x, last.y, player=field.player, city=last.building)
                new_unit.set_use(False)
                last.set_unit(new_unit)
                del_all_selection()
                last.building.count_of_units += 1
                cur_money[field.player - 1] -= 5
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s and can_spawn and \
                    cur_money[
                        field.player - 1] >= 7 and last.building.current_level() >= 2 and \
                    last.building.count_of_units < last.building.max_units_count:
                new_unit = ShieldMan(field, last.x, last.y, player=field.player, city=last.building)
                new_unit.set_use(False)
                last.set_unit(new_unit)
                del_all_selection()
                last.building.count_of_units += 1
                cur_money[field.player - 1] -= 7
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and last and last.unit and \
                    last.unit.player == field.player and (
                    isinstance(last.building, Village) or isinstance(last.building, City)) and \
                    last.building.is_capture:
                if isinstance(last.building, City):
                    last.building.pl = field.player
                    in_step[field.player - 1] += last.building.doxod
                    in_step[2 - field.player] -= last.building.doxod
                    for i in range(field.sz):
                        for j in range(field.sz):
                            if field[i, j].private and field[i, j].private[1] == last.building:
                                field[i, j].private[0] = field.player
                    last.building.is_capture = False
                    last.unit.set_use(False)
                else:
                    last.set_building(City(last.unit.player, last.x, last.y, field))
                    in_step[field.player - 1] += 2
                    last.unit.set_use(False)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m and last and not last.building and \
                    last.private and last.private[0] == field.player and \
                    cur_money[field.player - 1] >= 20 and last.typ in 'gcs':
                last.set_building(WindMill(in_step, field.player, last.x, last.y, field))
                cur_money[field.player - 1] -= 20

            if event.type == pygame.KEYDOWN and event.key == pygame.K_l and last and not last.building and \
                    last.private and last.private[0] == field.player and \
                    cur_money[field.player - 1] >= 15 and last.typ in 'gcs':
                last.set_building(LumberHut(in_step, field.player, last.x, last.y, field))
                cur_money[field.player - 1] -= 15

        print_balance(field.player)
        if in_step[0] == 0:
            run_game = -2
        elif in_step[1] == 0:
            run_game = -1
        pygame.display.flip()

    if -run_game == FIRST_PLAYER:
        text_coord = 200
        ans = [f'The first player won by scoring {in_step[0]} points per turn',
               f'                           Play again?']
        game_end(text_coord, ans)
    elif -run_game == SECOND_PLAYER:
        text_coord = 200
        ans = [f'The second player won by scoring {in_step[1]} points per turn',
               f'                           Play again?']
        game_end(text_coord, ans)
    else:
        continue

    local_run = 1
    while local_run:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                local_run = 0
pygame.quit()
