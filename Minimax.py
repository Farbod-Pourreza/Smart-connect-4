from tkinter.tix import ROW
import numpy as np
import random
import pygame
import sys
import math
import copy

#pygame colors
BLACK = (0, 0, 0) 
GRAY = (127, 127, 127) 
WHITE = (255, 255, 255)
RED = (255, 0, 0) 
GREEN = (0, 255, 0) 
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0) 
CYAN = (0, 255, 255) 
MAGENTA = (255, 0, 255)

print("rows:")
rows = int(input())


print("columns:")
columns = int(input())

print("how do you want to play:")
print("1 = AI vs AI ")
print("2 = PLAYER VS PLAYER")
print("3 = PLAYER VS AI")
mode = int(input())

EMPTY = 0
PLAYER_1= 0
PLAYER_2 = 1
AI_1 = 0
AI_2 = 1
PLAYER_1_ITEM= 1
PLAYER_2_ITEM = 2
AI_1_ITEM = 1
AI_2_ITEM  = 2
WINDOW_LENGTH = 4
WIN = +10000
DRAW = 1
LOSS = -100000
def create_board():
	board = np.zeros((rows,columns))
	return board

def put_A_circle(board, row, col, piece):
	board[row][col] = piece

def find_open_row(board, col):
	for row in range(rows):
		if board[row][col] == 0:
			return row
	return -1

def valid_location(board, col):
	return board[rows-1][col] == 0

def print_board(board):
	print(np.flip(board, 0))

def evaluate(window, item):
	score = 0
	if item == PLAYER_1_ITEM:
		other_item = AI_2_ITEM
	else:
		other_item = PLAYER_1_ITEM
	if window.count(item) == 4:
		score += 1000
	elif window.count(item) == 2 and window.count(EMPTY) == 2:
		score += 10
	elif window.count(item) == 3 and window.count(EMPTY) == 1:
		score += 100
	if window.count(other_item) == 3 and window.count(EMPTY) == 1:
		score -= 100
	return score

def calculate_score(board, item):
	score = 0
	center_array = [int(i) for i in list(board[:, columns//2])]
	center_count = center_array.count(item)
	score += center_count * 3

	for row in range(rows):
		row_array = [int(i) for i in list(board[row,:])]
		for column in range(columns-3):
			window = row_array[column:column+WINDOW_LENGTH]
			score += evaluate(window, item)

	for column in range(columns):
		col_array = [int(i) for i in list(board[:,column])]
		for row in range(rows-3):
			window = col_array[row:row+WINDOW_LENGTH]
			score += evaluate(window, item)

	for row in range(rows-3):
		for column in range(columns-3):
			window = [board[row+i][column+i] for i in range(WINDOW_LENGTH)]
			score += evaluate(window, item)

	for row in range(rows-3):
		for column in range(columns-3):
			window = [board[row+3-i][column+i] for i in range(WINDOW_LENGTH)]
			score += evaluate(window, item)

	return score
def get_available_loc(board):
	avalable_locs = []
	for col in range(columns):
		if valid_location(board, col):
			avalable_locs.append(col)
	return avalable_locs
	
def finishing_move(board):
	if (win_move(board, PLAYER_1_ITEM) or win_move(board, AI_2_ITEM) or len(get_available_loc(board)) == 0):
		return True
	return False

def win_move(board, piece):
	for colum in range(columns):
		for row in range(rows-3):
			if board[row][colum] == piece and board[row+1][colum] == piece and board[row+2][colum] == piece and board[row+3][colum] == piece:
				return True

	for colum in range(columns-3):
		for row in range(rows):
			if board[row][colum] == piece and board[row][colum+1] == piece and board[row][colum+2] == piece and board[row][colum+3] == piece:
				return True
	for colum in range(columns-3):
		for row in range(rows-3):
			if board[row][colum] == piece and board[row+1][colum+1] == piece and board[row+2][colum+2] == piece and board[row+3][colum+3] == piece:
				return True

	for colum in range(columns-3):
		for row in range(3, rows):
			if board[row][colum] == piece and board[row-1][colum+1] == piece and board[row-2][colum+2] == piece and board[row-3][colum+3] == piece:
				return True



def draw_board(board):
	for colum in range(columns):
		for row in range(rows):
			pygame.draw.rect(screen, GREEN, (colum*SIZE_OF_SQUARE, row*SIZE_OF_SQUARE+SIZE_OF_SQUARE, SIZE_OF_SQUARE, SIZE_OF_SQUARE))
			pygame.draw.circle(screen, BLUE, (int(colum*SIZE_OF_SQUARE+SIZE_OF_SQUARE/2), int(row*SIZE_OF_SQUARE+SIZE_OF_SQUARE+SIZE_OF_SQUARE/2)), CIRCLE_R)
	
	for colum in range(columns):
		for row in range(rows):		
			if board[row][colum] == PLAYER_1_ITEM:
				pygame.draw.circle(screen, RED, (int(colum*SIZE_OF_SQUARE+SIZE_OF_SQUARE/2), height-int(row*SIZE_OF_SQUARE+SIZE_OF_SQUARE/2)), CIRCLE_R)
			elif board[row][colum] == PLAYER_2_ITEM: 
				pygame.draw.circle(screen, BLACK, (int(colum*SIZE_OF_SQUARE+SIZE_OF_SQUARE/2), height-int(row*SIZE_OF_SQUARE+SIZE_OF_SQUARE/2)), CIRCLE_R)
	pygame.display.update()





def minimax(board, depth, alpha, beta, maximize):
	finishing = finishing_move(board)
	avalable_locs = get_available_loc(board)
	if finishing:
		if win_move(board, AI_2_ITEM):
			return (None, 1000000)
		elif win_move(board, PLAYER_1_ITEM):
			return (None, -1000000)
		else: 
			return (None, 0)
	if depth == 0: 
			return (None, calculate_score(board, AI_2_ITEM))
	if maximize:
		value = -math.inf
		column = 0
		for col in avalable_locs:
			row = find_open_row(board, col)
			copy_of_board = board.copy()
			put_A_circle(copy_of_board, row, col, AI_2_ITEM)
			new_score = minimax(copy_of_board, depth-1, alpha, beta, False)[1]
			if new_score > value:
				column = col
				value = new_score
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: 
		value = math.inf
		column = 0
		for col in avalable_locs:
			row = find_open_row(board, col)
			copy_of_board = board.copy()
			put_A_circle(copy_of_board, row, col, PLAYER_1_ITEM)
			new_score = minimax(copy_of_board, depth-1, alpha, beta, True)[1]
			if new_score < value:
				column = col
				value = new_score
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value


			


board = create_board()
print_board(board)
pygame.init()
SIZE_OF_SQUARE = 50
CIRCLE_R = int(SIZE_OF_SQUARE/2 - 5)
width = columns * SIZE_OF_SQUARE
height = (rows+1) * SIZE_OF_SQUARE
size = (width, height)
screen = pygame.display.set_mode(size)
draw_board(board)
turn = random.randint(PLAYER_1, PLAYER_2)
pygame.display.update()
myfont = pygame.font.SysFont("arial", 20)
game_over = False




if(mode == 2 or mode == 3):
	while not game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()            
			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, GRAY, (0,0, width, SIZE_OF_SQUARE))
				posx = event.pos[0]
			pygame.display.update()
			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(screen, GRAY, (0,0, width, SIZE_OF_SQUARE))
				if turn == PLAYER_1:
					posx = event.pos[0]
					col = int(math.floor(posx/SIZE_OF_SQUARE))

					if valid_location(board, col):
						row = find_open_row(board, col)
						put_A_circle(board, row, col, PLAYER_1_ITEM)

						if win_move(board, PLAYER_1_ITEM):
							label = myfont.render("winner is player 1!", 1, RED)
							screen.blit(label, (180,10))
							game_over = True
						print_board(board)
						draw_board(board)
				if(mode == 2):
					if turn == PLAYER_2:
						posx = event.pos[0]
						col = int(math.floor(posx/SIZE_OF_SQUARE))
						if valid_location(board, col):
							row = find_open_row(board, col)
							put_A_circle(board, row, col, PLAYER_2_ITEM)

							if win_move(board, PLAYER_2_ITEM):
								label = myfont.render("winner is player 2!", 1, BLACK)
								screen.blit(label, (180,10))
								game_over = True        
							print_board(board)
							draw_board(board)
				turn += 1
				turn = turn % 2
		if(mode == 3):
			if turn == AI_2 and not game_over:
				best_move , value = minimax(board, 5  , -math.inf, math.inf , True)
				if valid_location(board, best_move):
					row = find_open_row(board, best_move)
					put_A_circle(board, row, best_move, AI_2_ITEM)
					if win_move(board, AI_2_ITEM):
						label = myfont.render("winner is player 2!", 1, BLACK)
						screen.blit(label, (180,10))
						game_over = True
					print_board(board)
					draw_board(board)
				turn += 1
				turn = turn % 2
		if game_over:
			pygame.time.wait(3000)
if(mode == 1):
	 while not game_over:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
			if turn == AI_2 and not game_over:
				best_move  , value = minimax(board, 5  , -math.inf, math.inf , True)
				if valid_location(board, best_move):
					row = find_open_row(board, best_move)
					put_A_circle(board, row, best_move, AI_2_ITEM)
					if win_move(board, AI_2_ITEM):
						label = myfont.render("winner is player 1!", 1, BLACK)
						screen.blit(label, (180,10))
						game_over = True
					print_board(board)
					draw_board(board)
				turn += 1
				turn = turn % 2
			if turn == AI_1 and not game_over:
				best_move  , value = minimax(board, 5  , -math.inf, math.inf , True)
				if valid_location(board, best_move):
					row = find_open_row(board, best_move)
					put_A_circle(board, row, best_move, AI_1_ITEM)
					if win_move(board, AI_1_ITEM):
						label = myfont.render("winner is player 2!", 1, BLACK)
						screen.blit(label, (180,10))
						game_over = True
					print_board(board)
					draw_board(board)
				turn += 1
				turn = turn % 2


		



