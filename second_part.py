from tkinter.tix import ROW
import numpy as np
import random
import pygame
import sys
import math
import copy
import time
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

def get_available_loc(board):
	avalable_locs = []
	for col in range(columns):
		if valid_location(board, col):
			avalable_locs.append(col)
	return avalable_locs
	
def next_state(board , turn):
	# Retuns next state
	aux = copy.deepcopy(board)
	moves =get_available_loc(aux)
	if len(moves) > 0 :
		ind = random.randint(0,len(moves)-1)
		row = aux.tryMove(moves[ind])
		aux.board[row][moves[ind]] = turn
		aux.last_move = [ row, moves[ind] ]
	return aux 

def win_move(board, piece):
	# Check vertical  for win
	for colum in range(columns):
		for row in range(rows-3):
			if board[row][colum] == piece and board[row+1][colum] == piece and board[row+2][colum] == piece and board[row+3][colum] == piece:
				return True

	# Check horizontal for win
	for colum in range(columns-3):
		for row in range(rows):
			if board[row][colum] == piece and board[row][colum+1] == piece and board[row][colum+2] == piece and board[row][colum+3] == piece:
				return True
	# Check  diaganols
	for colum in range(columns-3):
		for row in range(rows-3):
			if board[row][colum] == piece and board[row+1][colum+1] == piece and board[row+2][colum+2] == piece and board[row+3][colum+3] == piece:
				return True

	# Check negatively diaganols
	for colum in range(columns-3):
		for row in range(3, rows):
			if board[row][colum] == piece and board[row-1][colum+1] == piece and board[row-2][colum+2] == piece and board[row-3][colum+3] == piece:
				return True

def terminal(board):
	# Returns true when the game is finished, otherwise false.
	for i in range(len(board[0])):
		if ( board[0][i] == 0 ):
			return False
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
	return score + 1

def initialize_population(n, m):
	return np.random.randint(0, m, (n, 1))

def evaluate_fitness(population, board, player):
	fitness = np.zeros(population.shape[0])
	for i in range(population.shape[0]):
		move = int(population[i, 0])
		next_board = play_move(board, move, player)
		fitness[i] = calculate_score(next_board, player)
	return fitness

def play_move(board, move, player):
	next_board = np.copy(board)
	for i in range(board.shape[0]):
		if next_board[i, move] == 0:
			next_board[i, move] = player
			break
	return next_board


def roulette_wheel_selection(population, fitness):
	fitness_sum = np.sum(fitness) / fitness.shape[0]
	fitness_normalized = fitness / fitness_sum
	fitness_cumulative = np.cumsum(fitness_normalized)
	selected = []
	for i in range(population.shape[0]):
		r = np.random.uniform(0, 1)
		for j in range(population.shape[0]):
			if r <= fitness_cumulative[j]:
				selected.append(population[j])
				break
	
	return np.array(selected)

def crossover(selected, p_crossover):
	offspring = np.zeros((selected.shape[0], selected.shape[1]))
	for i in range(0, selected.shape[0], 2):
		parent1 = selected[i, :]
		parent2 = selected[i+1, :]
		if np.random.uniform(0, 1) < p_crossover:
			offspring[i, :] = parent2
			offspring[i+1, :] = parent1
		else:
			offspring[i, :] = parent1
			offspring[i+1, :] = parent2
	return offspring



def mutation(population, p_mutation, m):
	for i in range(population.shape[0]):
		if np.random.uniform(0, 1) < p_mutation:
			population[i, 0] = np.random.randint(0, m)
	return population

def genetic_algorithm(board, player, n, m, p_crossover, p_mutation, max_generations):
	population = initialize_population(n, m)
	for generation in range(max_generations):
		fitness = evaluate_fitness(population, board, player)
		selected = roulette_wheel_selection(population, fitness)
		offspring = crossover(selected, p_crossover)
		population = mutation(offspring, p_mutation, m)
	
	fitness = evaluate_fitness(population, board, player)
	best_index = np.argmax(fitness)
	best_move = population[best_index, 0]
	return best_move





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
				best_move  = genetic_algorithm(board , AI_2_ITEM , 50 , columns , 0.7 , 0.03 ,200)
				print(best_move)
				best_move = int(best_move)
				if valid_location(board, best_move):
					#pygame.time.wait(500)
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
				best_move  = genetic_algorithm(board , AI_2_ITEM , 50 , columns , 0.7 , 0.03 ,200)
				best_move = int(best_move)
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
				best_move  = genetic_algorithm(board , AI_1_ITEM , 50 , columns , 0.7 , 0.03 ,200)
				best_move = int(best_move)
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
		# if game_over:
		# 	pygame.time.wait(3000)

		



