import pygame
from pygame.locals import *
from pygame.draw import *
import sys
from random import *
from enum import Enum, auto


class State(Enum):
	START = auto()
	PLAY_STONE = auto()
	MOVE = auto()



pygame.init()

FPS = 30  # frames per second setting
fpsClock = pygame.time.Clock()
pygame.display.set_caption('Animation')
# Ouverture de la fenêtre Pygame
DISPLAYSURF = pygame.display.set_mode((640, 480))
RED = (255, 0, 0)
SIZE = 70
WIDTH = 8
HEIGHT = 6
stones = []
perso = pygame.image.load("obj.bmp").convert()
x_perso = 3
y_perso = 3
state = State.START

def calculate_position(x, y, is_perso=False):
	x_ = 30 + x * SIZE + y % 2 * (SIZE / 2)
	y_ = 30 + y * SIZE
	if is_perso:
		y_ += SIZE / 5 + 5
		x_ += 10
	return x_, y_


def is_border(x, y):
	return x == 0 or y == 0 or y == HEIGHT-1 or x == WIDTH - 1 - y % 2

def is_exist(n):
	x = n[0]
	y = n[1]
	return x >= 0 and y >= 0 and y <= HEIGHT-1 and x <= WIDTH - 1 - y % 2

def border_cells():
	arr = []
	for i in range(0,WIDTH):
		arr.append((i,0))
		arr.append((i,HEIGHT-1))
	for j in range(1, HEIGHT-1):
		arr.append((0,j))
		arr.append((WIDTH-1-(j%2), j))
	return arr
# weigts = {(1,0): 12

def get_weights():
	dict_weigts = {}
	for y in range(0, 6):
		for x in range(0, 7 + (y + 1) % 2):
			if is_border(x, y):
				dict_weigts[(x, y)] = 0
			else:
				dict_weigts[(x, y)] = 99999
	return dict_weigts


# print(get_weights())

def get_neibours(n):
	x = n[0]
	y = n[1]
	if y % 2 == 0:
		return [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1)]
	else:
		return [(x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]


#print(get_neibours(3, 5))


def dijkstra(x,y, n=0):
	weights = get_weights()
	# for w in weights:
	# if weights[w] > 0:
	count = n
	if is_border(x,y):
		return count
	nbs = get_neibours(x,y)
	for n in nbs:
		count += 1
		weights[n] = count
		return dijkstra(n[0],n[1], count)

# for w in weights:


# dijkstra()


def get_direction(x, y):
	known_cells = border_cells()
	current_cell = 0
	while current_cell < len(known_cells):
		nbs = get_neibours(known_cells[current_cell])
		for n in nbs:
			if n == (x,y):
				return known_cells[current_cell]
			if is_exist(n) and (n not in known_cells) and (n not in stones):
				known_cells.append(n)
		current_cell += 1
	return False

def add_stone(n):
	x = n[0]
	y = n[1]
	if is_exist(n) and (x != x_perso or y != y_perso) and (n not in stones):
		stones.append(n)
		return True
	return False

def gen_stones(num):
	for i in range(0,num):
		while True:
			x = randrange(0, WIDTH)
			y = randrange(0, HEIGHT)
			if add_stone((x,y)):
				break
	#print(stones)

gen_stones(4)

def get_square(x_pix, y_pix):
	for x_sqr in range(0, WIDTH):
		for y_sqr in range(0,HEIGHT):
			x,y = calculate_position(x_sqr, y_sqr)
			if (x_pix>x and y_pix >y + SIZE/5) and (x_pix < x + SIZE and y_pix < y + SIZE):
				return (x,y)
	return False

def draw():
	fond = pygame.image.load("background.bmp").convert()
	DISPLAYSURF.blit(fond, (0, 0))
	for i in range(0, HEIGHT):
		for j in range(0, WIDTH-1 + (i + 1) % 2):
			# x = 30 + j * 50 + i % 2 * 25
			# y = 30 + i * 50
			x, y = calculate_position(j, i, False)

			polygon(DISPLAYSURF, RED, (
				(x, y + (SIZE / 5)), (x, y + SIZE), (x + SIZE / 2, y + (SIZE / 5 * 6)), (x + SIZE, y + SIZE),
				(x + SIZE, y + SIZE / 5), (x + SIZE / 2, y), (x, y + SIZE / 5)), 2)
	perso_x_pix, perso_y_pix = calculate_position(x_perso, y_perso, True)
	DISPLAYSURF.blit(perso, (perso_x_pix, perso_y_pix))
	pygame.display.flip()


draw()

x_perso += 1

def mouse_clique(x,y):
	global state
	if state == State.PLAY_STONE:
		s = get_square(x,y)
		if s != False and add_stone(s):
			state = State.MOVE
	#print(stones)

draw()

state = State.PLAY_STONE

while True:
	pos = pygame.mouse.get_pos()

	#evt = pygame.evt.poll()
	for evt in pygame.event.get():
		if evt.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			# pygame.display.update()
			# fpsClock.tick(FPS)

		if evt.type == pygame.MOUSEBUTTONDOWN and evt.button == 1:
			"""
			pos = pygame.mouse.get_pos()
			x = evt.pos[0]
			y = evt.pos[1]
			#mouse_clique(x, y)
			print("X:{}, Y:{}, pos:{}".format(x, y, pygame.mouse.get_pos()))
			
			UP: 
			b_down - motion -  b_up +
			
			DOWN:
			b_down - motion -  b_up - b_down
			"""


			pos = pygame.mouse.get_pos()
			x = evt.pos[0]
			y = evt.pos[1]
			#mouse_clique(x,y)
			print("X:{}, Y:{}, pos:{}".format(x,y, pygame.mouse.get_pos()))

		pass
	#print('OUT OF FOR')
