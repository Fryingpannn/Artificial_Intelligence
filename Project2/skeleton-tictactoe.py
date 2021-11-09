
# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3
	# player 1 = player X
	# player 2 = player o
	# size <- board size
	# current_state <- current_state of the board
	# self.winning_line_up_size
	# self.player1_maximum_depth 
	# self.player2_maximum_depth
	# self.allowed_time 
	# self.selected_algorithm #0 minimax #1 for ALPHABETA
	# self.player1_is_AI
	# self.player2_is_AI
	# self.result_if_win
	
	def __init__(self, recommend = True):
		self.initialize_game()
		self.recommend = recommend
	
	def print_stats(self):
		print("Size: "+ str(self.size))
		print("Current State: "+ str(self.current_state))
		print("Winning Line Up Size: "+ str(self.winning_line_up_size))
		print("Time: "+ str(self.allowed_time))
		print("Selected Algorithm: "+ "minimax" if self.selected_algorithm == 0 else "ALPHABETA")
		print("player1_maximum_depth: "+ str(self.player1_maximum_depth))
		print("player2_maximum_depth: "+ str(self.player2_maximum_depth))
		print("player1 is AI: "+ str(self.player1_is_AI))
		print("player2 is AI: "+ str(self.player2_is_AI))
		
		
	def initialize_game(self):
		default_mode = self.input_default_mode()
	    # Player X always plays first
		self.player_turn = 'X'
		self.result_if_win= '.'
		if default_mode:
			self.size = 3
			self.current_state = [['.' for col in range(self.size)] for row in range(self.size)]
			self.winning_line_up_size = 3
			self.allowed_time = 5
			self.selected_algorithm = 0 #MINIMAX
			self.player1_maximum_depth = 5  #no idea, change later
			self.player2_maximum_depth = 5
			self.player1_is_AI = True
			self.player2_is_AI = True
		else:
			self.initialze_board()
			self.initialize_algorithm()
	
	def initialze_board(self):
		# Initializing the board
		self.size = self.input_size()
		self.current_state = [['.' for col in range(self.size)] for row in range(self.size)]
		self.initialize_block()
	   
	def initialize_block(self):
		self.number_of_block = self.input_block()
		self.initialize_block_coordinates();
	  
	def initialize_block_coordinates(self):
		required = self.number_of_block
		while (required >0):
			print("Please input coordinate of the bloc: ")
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				self.current_state[py][px] = '*'
				required -= 1
			else:
				print('The coordinate is not valid! Try again.')
	    
	def initialize_algorithm(self):
		self.winning_line_up_size = self.input_winning_size()
		self.player1_maximum_depth = self.input_maximum_depth(1)
		self.player2_maximum_depth = self.input_maximum_depth(2)
		self.allowed_time = self.input_maximum_time()
		self.selected_algorithm = self.input_algorithm()
		self.player1_is_AI = self.input_player_behaviour(1)
		self.player2_is_AI = self.input_player_behaviour(2)
	    
	def input_default_mode(self):
		while True:
			print("Please pick number 1 if you want default mode, enter any number otherwise")
			number = int(input('enter the selection: '))
			if (number == 1 ):
				return True
			else:
				return False
	    
	def input_player_behaviour(self, player):
	    while True:
	    	print("Press 1 if you want to player "+ str(player) + " to be AI or any other if you want it to be human")
	    	number = int(input('enter the number: '))
	    	if (number == 1 ):
	    		return True
	    	else:
	    		return False
				
	def input_algorithm(self):
		while True:
			print("Please input 1 to select minimax or alphabeta")
			selection = int(input('enter the selection: '))
			if (selection == 0 ):
				return selection
			elif (selection ==1):
				return selection
			else:
				print('The number is invalid! Try again.')
	    
	def input_maximum_time(self):
		while True:
			print("Please input maximum time allowed for AI to make move ")
			number = int(input('enter the number: '))
			if (number > 0 ):
				return number
			else:
				print('The number is invalid! Try again.')
	    
	def input_maximum_depth(self, player):
		while True:
			print("Please input maximum depth for player "+ str(player))
			number = int(input('enter the number: '))
			if (number > 0 ):
				return number
			else:
				print('The number is invalid! Try again.')
				
	def input_winning_size(self):
		while True:
			print("Please input winning line up size: ")
			number = int(input('enter the number: '))
			if (number >= 3 or number <= (self.size)):
				return number
			else:
				print('The size is not within 0 and size! Try again.')
				
	def input_block(self):
		while True:
			print("Please input number of blocs you want to input: ")
			number = int(input('enter the number: '))
			if (number >= 0 or number <= (2*self.size)):
				return number
			else:
				print('The size is not within 0 and 2*size! Try again.')
	    
	def input_size(self):
		while True:
			print("Please input the size of the board: ")
			size = int(input('enter the size: '))
			if (size>=3 and size <=10):
				return size
			else:
				print('The size is not within 3 and 10! Try again.\n')

	def draw_board(self):
		print()
		for y in range(0, self.size):
			for x in range(0, self.size):
				print(F'{self.current_state[x][y]}', end="")
			print()
		print()
		
	def is_valid(self, px, py):
		if px < 0 or px > self.size or py < 0 or py > self.size:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def is_end(self):
		# Vertical win
		if (self.check_vertical_win()):
			return self.result_if_win
		# Horizontal win
		if (self.check_horizontal_win()):
			return self.result_if_win
		# Main diagonal win
		if (self.check_diagonal_left_win()):
			return self.result_if_win
		# Second diagonal win
		if (self.check_diagonal_right_win()):
			return self.result_if_win
		# Is whole board full?
		for i in range(0, self.size):
			for j in range(0, self.size):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None
		# It's a tie!
		return '.'
		
	def check_horizontal_win(self):
		for y in range(0, self.size):
			for x in range(0, self.size - 2):
				if (self.current_state[y][x] != '.' and
					self.current_state[y][x] == self.current_state[y][x+1] and 
					self.current_state[y][x] == self.current_state[y][x+2]):
					self.result_if_win = self.current_state[y][x]
					return True
		return False
				
	def check_vertical_win(self):
		for y in range(0, self.size -2):
			for x in range(0, self.size):
				if (self.current_state[y][x] != '.' and
					self.current_state[y][x] == self.current_state[y+1][x] and 
					self.current_state[y][x] == self.current_state[y+2][x]):
					self.result_if_win = self.current_state[y][x]
					return True
		return False
		
	#facing left wards, from right(downwards) to left(upwards)
	def check_diagonal_left_win(self):
		for y in range(0, self.size - 2):
			for x in range(0, self.size - 2):
				if (self.current_state[y][x] != '.' and
					self.current_state[y][x] == self.current_state[y+1][x+1] and 
					self.current_state[y][x] == self.current_state[y+2][x+2]):
					self.result_if_win = self.current_state[y][x]
					return True
		return False
		
	#Facing Right, from left(downwards) to right(upwards)
	def check_diagonal_right_win(self):
		for y in range(0, self.size -2):
			for x in range(2, self.size):
				if (self.current_state[y][x] != '.' and
					self.current_state[y][x] == self.current_state[y+1][x-1] and 
					self.current_state[y][x] == self.current_state[y+2][x-2]):
					self.result_if_win = self.current_state[y][x]
					return True
		return False
		
	def check_end(self):
		self.result = self.is_end()
		
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(input('enter the x coordinate: '))
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def minimax(self, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.size):
			for j in range(0, self.size):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, self.size):
			for j in range(0, self.size):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)

	def play(self,algo=None,player_x=None,player_o=None):
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False)
				else:
					(_, x, y) = self.minimax(max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.current_state[x][y] = self.player_turn
			self.switch_player()
			
        
def main():
	g = Game(recommend=True)
	g.print_stats()
	g.play(algo= Game.MINIMAX if g.selected_algorithm ==0 else Game.ALPHABETA, player_x= Game.AI if g.player1_is_AI else Game.HUMAN ,player_o=Game.AI if g.player2_is_AI else Game.HUMAN)
	# g.play(algo=Game.ALPHABETA,player_x=Game.AI,player_o=Game.AI)
	# g.play(algo=Game.MINIMAX,player_x=Game.AI,player_o=Game.HUMAN)

if __name__ == "__main__":
	main()
