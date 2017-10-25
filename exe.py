import pygame
from pygame.locals import *
from pygame.draw import *
import sys
pygame.display.set_caption('Animation')
DISPLAYSURF = pygame.display.set_mode((720, 450))


while True:
    pos = pygame.mouse.get_pos()

    # evt = pygame.evt.poll()
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:

            pos = pygame.mouse.get_pos()
            x = evt.pos[0]
            y = evt.pos[1]
            # mouse_clique(x,y)
            print("X:{}, Y:{}, pos:{}".format(x, y, pygame.mouse.get_pos()))

        pass
        # print('OUT OF FOR')
