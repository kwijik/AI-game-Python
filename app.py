import pygame
from pygame.locals import *
from pygame.draw import *
import sys

pygame.init()

FPS = 30 # frames per second setting
fpsClock = pygame.time.Clock()
pygame.display.set_caption('Animation')
#Ouverture de la fenêtre Pygame
DISPLAYSURF = pygame.display.set_mode((640, 480))
RED =  (255, 0, 0)
SIZE = 70


def calculate_position(x,y, is_perso):
	x_ = 30 + x * SIZE + y % 2 * (SIZE / 2)
	y_ = 30 + y * SIZE
	if is_perso:
		y_ += SIZE/5 + 5
		x_+= 10
	return x_,y_

def is_border(x,y):
	return x==0 or y==0 or y==5 or x == 7 - y % 2
#weigts = {(1,0): 12

def get_weights():
	dict_weigts = {}
	for y in range(0, 6):
		for x in range(0, 7 + (y + 1) % 2):
			if is_border(x,y):
				dict_weigts[(x,y)]=0
			else:
				dict_weigts[(x, y)] = 99999
	return dict_weigts

# добавляем матрицу с

print(get_weights())

def get_neibours(x,y):
	if y%2 == 0 :
		return [(x-1,y-1),(x,y-1), (x-1,y), (x+1, y), (x-1, y+1),(x, y+1)]
	else:
		return [(x,y-1), (x+1,y-1),(x-1,y), (x+1, y), (x, y+1),(x+1, y+1)]

print(get_neibours(6,1))


def get_direction(x,y):
	neibours= get_neibours(x,y)
	for n in neibours:
		if is_border(n):
			return n, 1

fond = pygame.image.load("background.bmp").convert()
DISPLAYSURF.blit(fond, (0,0))

perso = pygame.image.load("perso1.bmp").convert()
perso_x, perso_y = calculate_position(2,3,True)

direction = 'right'
DISPLAYSURF.blit(perso, (perso_x,perso_y))

for i in range(0,6):
	for j in range (0,7+(i+1)%2):
		#x = 30 + j * 50 + i % 2 * 25
		#y = 30 + i * 50
		x,y = calculate_position(j,i,False)
		polygon(DISPLAYSURF, RED, ((x, y+(SIZE/5)), (x, y+SIZE), (x+SIZE/2, y+(SIZE/5*6)), (x+SIZE, y+SIZE),(x+SIZE, y+SIZE/5),(x+SIZE/2, y),(x, y+SIZE/5)), 2)
		print("X:{}, Y:{}".format(x,y))

pygame.display.flip()

while True:
	#if direction== 'right':
		#perso_x += 1

	#DISPLAYSURF.blit(perso, (perso_x, perso_y))

	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	#pygame.display.update()
	#fpsClock.tick(FPS)