import pygame

pygame.init()
sc = pygame.display.set_mode((800, 700))

from board import Field

# pygame.init()


field = Field(10, sc, god_mode=1)
field.debug_print()
run = 1
while run:
    field.draw()
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
