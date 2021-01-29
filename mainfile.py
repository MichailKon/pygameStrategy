import pygame
from board import Field

pygame.init()
sc = pygame.display.set_mode((800, 700))
in_step = [2, 2]
cur_money = [5, 5]

field = Field(10, sc, god_mode=1)
field.debug_print()
run = 1
while run:
    field.draw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
