import pygame
from pygame.locals import *
from pygame.draw import *
import sys
from enum import Enum, auto
from Position import Position as Position

#print(Position)
class State(Enum):
    START = auto()
    PLAY_STONE = auto()
    MOVE = auto()
    GAME_OVER = auto()


pygame.init()

FPS = 30  # frames per second setting
fpsClock = pygame.time.Clock()
pygame.display.set_caption('Animation')
# Ouverture de la fenêtre Pygame
DISPLAYSURF = pygame.display.set_mode((640, 720))
RED = (255, 0, 0)
SIZE = 70
WIDTH = 8
HEIGHT = 9
perso = pygame.image.load("obj.bmp").convert()
stoneImg = pygame.image.load("stone.bmp").convert()

state = State.START

position_now =  Position(HEIGHT, WIDTH, 5, 4)
#position_now.setPerson(5,4)

