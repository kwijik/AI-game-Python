import pygame
from pygame.locals import *
from pygame.draw import *
import sys
import time
from enum import Enum, auto
from Position import Position as Position

from Message import Message as Message


class State(Enum):
	START = auto()
	PLAY_STONE = auto() 
	MOVE = auto()
	GAME_OVER = auto()
	BUTTON = auto()
	ALGO_FAILED_PLAY_STONE = auto()
	ALGO_FAILED_MOVE = auto()

pygame.init()

PLAY_HUMAN = False

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

position_now =  Position(HEIGHT, WIDTH, 4, 4) 

fond = pygame.image.load("background.bmp").convert()

NUMBER_OF_STONES = 10

def alphabeta(node, depth, alpha, beta, maximizingPlayer):
	if (depth == 0 or len(node.empty_cells)==0 ):
		return (node.weight(), False)
	weight1 = node.weight() # weight

	if (weight1 == 9999):
		return (weight1 + depth - 10, node)

	if (weight1 == -9999):
		return (weight1 - depth + 10, node)
	if (maximizingPlayer):
		v = -99999 # weight of position if all the players play their best witg depth 
		v_pos = False # position to go
		node_children = node.get_children(maximizingPlayer)
		for child in node_children: # get all stone's positions
			#print("For is here!")

			temp = alphabeta(child, depth-1, alpha, beta, False) # the best position what human can do
			# print(("   "*(3-depth)), "temp: ", temp[0])
			if (temp[0] > v):  # 
				#print("temp")
				v = temp[0]
				v_pos = child
			alpha = max(alpha, v) # the best position found for stones
			if (beta <= alpha): # alpha  prunning goes here
				break
		#if(v_pos == False):
			#print("v_pos is False!")
		return (v, v_pos)
	else:
		v_pos = False
		v = 99999

		for child in node.get_children(maximizingPlayer):
			#print("For !")
			temp = alphabeta(child, depth-1, alpha, beta, True)
			# print(("   "*(3-depth)), "temp: ", temp[0])
			if (temp[0] < v):
				v = temp[0]
				v_pos = child
			beta = min(beta, v)  # the best position found for human
			if (beta <= alpha):  #  beta prunning goes here
				break
		#if(v_pos == False):
				#print("ELSE: v_pos is False!")
		return (v, v_pos)

def get_direction_human():
	while True:
		for event in pygame.event.get():
			standard_events(event) # standard events as closing window
			if (event.type == pygame.MOUSEBUTTONDOWN):
				pos = pygame.mouse.get_pos()
				res = get_square(pos[0], pos[1])
				if res != False and res in position_now.get_neibours((position_now.x_perso,position_now.y_perso)) and not(res  in position_now.stones):
					return res
			

def calculate_position(x, y, is_perso=False): # returns pixels
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


def get_neibours(n):
	x = n[0]
	y = n[1]
	if y % 2 == 0:
		return [(x - 1, y - 1), (x, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x, y + 1)]
	else:
		return [(x, y - 1), (x + 1, y - 1), (x - 1, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]


def get_direction(position_now):
	known_cells = [] # it's our 
	for b in border_cells():
		if(b not in position_now.stones):
			known_cells.append(b)
	current_cell = 0
	while current_cell < len(known_cells): # go on border cells that are not stones 
		nbs = get_neibours(known_cells[current_cell]) # get neibours of these cells
		for n in nbs:
			#print("N: {} ; stones: {}".format(n, stones))
			if n == (position_now.x_perso, position_now.y_perso): # if person is on this cell
				return known_cells[current_cell]
			if is_exist(n) and (n not in known_cells) and (n not in position_now.stones):
				
				known_cells.append(n)
			
		current_cell += 1

	return False


position_now.placeRandom(NUMBER_OF_STONES) # number of stones

def get_square(x_pix, y_pix):
	for x_sqr in range(0, WIDTH):
		for y_sqr in range(0,HEIGHT):
			x,y = calculate_position(x_sqr, y_sqr)
			if (x_pix>x and y_pix >y + SIZE/5) and (x_pix < x + SIZE and y_pix < y + SIZE): #5 eto ostup
				return (x_sqr,y_sqr)
	return False

#print(get_square(237, 117))

def draw():
	#fond = pygame.image.load("Grass.bmp").convert()
	global fond
	DISPLAYSURF.blit(fond, (0, 0))
	for i in range(0, HEIGHT):
		for j in range(0, WIDTH-1 + (i + 1) % 2):
			# x = 30 + j * 50 + i % 2 * 25
			# y = 30 + i * 50
			x, y = calculate_position(j, i, False) # getting coordinates for hexagon

			polygon(DISPLAYSURF, RED, (
				(x, y + (SIZE / 5)), (x, y + SIZE), (x + SIZE / 2, y + (SIZE / 5 * 6)), (x + SIZE, y + SIZE),
				(x + SIZE, y + SIZE / 5), (x + SIZE / 2, y), (x, y + SIZE / 5)), 2)
	for s in position_now.stones:
		pos = calculate_position(s[0], s[1], True)
		DISPLAYSURF.blit(stoneImg, pos)
	perso_x_pix, perso_y_pix = calculate_position(position_now.x_perso, position_now.y_perso, True)

	DISPLAYSURF.blit(perso, (perso_x_pix, perso_y_pix))
	pygame.display.flip()


draw()


def move(next_state):
	global state, position_now
	if state == State.MOVE or state == State.ALGO_FAILED_MOVE:
		if is_border(position_now.x_perso, position_now.y_perso):
			state = State.GAME_OVER
		else:
			if (PLAY_HUMAN):
				pos = get_direction_human()
			else:
				pos = get_direction(position_now)
			if pos == False:
				state = State.GAME_OVER
			else:
				position_now.setPerson(pos[0], pos[1])
				state = next_state

def mouse_clique(x,y):
	global state
	if state == State.PLAY_STONE:
		s = get_square(x,y)
		if s != False and add_stone(s):
			state = State.MOVE
			draw()

draw()

def buttonPressed():
	global state
	state = State.ALGO_FAILED_PLAY_STONE
state = State.PLAY_STONE
message = Message("Algo failed", 285, 335, 70, 50)

def standard_events(event):
	if event.type == QUIT:
		pygame.quit()
		sys.exit()

while True:
	print(state)
	for event in pygame.event.get():
		standard_events(event)
		message.handle_event(event, buttonPressed )

	if (state == State.GAME_OVER):
		draw()
	elif (state == State.MOVE):
		move(State.PLAY_STONE)
		draw()
	elif(state == State.PLAY_STONE ):
		temp = alphabeta(position_now, 4, -99999, 99999, True)
		if(temp[0] < 0):
			state = State.BUTTON
		else:
			if (temp[1]!= False):
				position_now = temp[1]
				print("Stone is placed on ", position_now.last_move)
				state = State.MOVE
			else:
				state = State.GAME_OVER
		draw()

	elif (state == State.BUTTON):
		message.draw(DISPLAYSURF)
		pygame.display.flip()
	elif (state == State.ALGO_FAILED_MOVE):
		move(State.ALGO_FAILED_PLAY_STONE)
		draw()
	elif( state == State.ALGO_FAILED_PLAY_STONE):

		position_now.add_stone(get_direction(position_now))
		state = State.ALGO_FAILED_MOVE
		draw()
	time.sleep(1)