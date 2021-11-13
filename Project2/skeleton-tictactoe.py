#!/usr/bin/env pypy
# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import numpy as np

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
      print("n="+ str(self.size) + " b=" + str(self.number_of_block)+ " s="+str(self.winning_line_up_size)+" t=" + str(self.allowed_time))
      print("blocs="+ str(self.location_of_block))
      if (self.player1_is_AI):
         print("player1: AI"+ " d=" + str(self.player1_maximum_depth) + " a=" +("False" if self.selected_algorithm == 0 else "True") + " e1 (simple)")
      else:
         print("Player1: Human")
      if (self.player2_is_AI):
         print("player2: AI"+ " d=" + str(self.player2_maximum_depth) + " a=" +("False" if self.selected_algorithm == 0 else "True") +  " e2 (advanced)")
      else:
         print("Player2: Human")
      
      
   def initialize_game(self):
      default_mode = self.input_default_mode()
       # Player X always plays first
      self.player_turn = 'X'
      self.result_if_win= '.'
      if default_mode:
         self.size = 3
         self.number_of_block = 0
         self.location_of_block = []
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
      self.location_of_block = []
      while (required >0):
         print("Please input coordinate of the bloc: ")
         px = int(input('enter the x coordinate: '))
         py = int(input('enter the y coordinate: '))
         if self.is_valid(px, py):
            self.current_state[py][px] = '*'
            required -= 1
            self.location_of_block.append([px,py])
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
         print("Please input 0 to select minimax or 1 to select alphabeta")
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
      winning_line = False
      for y in range(0, self.size):
         for x in range(0, self.size - self.winning_line_up_size + 1):
            winning_line = True
            owner = self.current_state[y][x]
            if (owner != '.' and owner != '*'):
               for j in range (1,self.winning_line_up_size):
                  if (self.current_state[y][x+j] == '.' or self.current_state[y][x+j] == '*' or self.current_state[y][x+j] != owner):
                     winning_line = False
                     break
            else:
               winning_line = False
            if winning_line == True:
               self.result_if_win = owner
               return True
      return winning_line

   def check_vertical_win(self):
      winning_line = False
      for y in range(0, self.size - self.winning_line_up_size + 1):
         for x in range(0, self.size):
            winning_line = True
            owner = self.current_state[y][x]
            if (owner != '.' and owner != '*'):
               for j in range (1,self.winning_line_up_size):
                  if (self.current_state[y+j][x] == '.' or self.current_state[y+j][x] == '*' or self.current_state[y+j][x] != owner):
                     winning_line = False
                     break
            else:
               winning_line = False
            if winning_line == True:
               self.result_if_win = owner
               return True
      return winning_line

   #facing left wards, from right(downwards) to left(upwards)
   def check_diagonal_left_win(self):
      winning_line = False
      for y in range(0, self.size - self.winning_line_up_size + 1):
         for x in range(0, self.size - self.winning_line_up_size + 1):
            winning_line = True
            owner = self.current_state[y][x]
            if (owner != '.' and owner != '*'):
               for j in range (1,self.winning_line_up_size):
                  if (self.current_state[y+j][x+j] == '.' or
                     self.current_state[y+j][x+j] == '*' or
                     self.current_state[y+j][x+j] != owner):
                     winning_line = False
                     break
            else:
               winning_line = False
            if winning_line == True:
               self.result_if_win = owner
               return True
      return winning_line

   #Facing Right, from left(downwards) to right(upwards)
   def check_diagonal_right_win(self):
      winning_line = False
      for y in range(0, self.size - self.winning_line_up_size + 1):
         for x in range(0, self.size):
            winning_line = True
            owner = self.current_state[y][x]
            if (owner != '.' and owner != '*'):
               for j in range (1,self.winning_line_up_size):
                  if (self.current_state[y+j][x-j] == '.' or
                     self.current_state[y+j][x-j] == '*' or
                     self.current_state[y+j][x-j] != owner):
                     winning_line = False
                     break
            else:
               winning_line = False
            if winning_line == True:
               self.result_if_win = owner
               return True
      return winning_line

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

   def update_v(self, count_o, count_x, values):
      index = max(count_o,count_x)
      if count_o >= count_x:
         return values[index]
      else:
         return -values[index]

   # generate all diagonals of a matrix, need numpy
   def generate_diagonals(self):
       # create a default array of specified dimensions
       a = np.array(self.current_state)

       diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
       
       # Now back to the original array to get the upper-left-to-lower-right diagonals,
       # starting from the right, so the range needed for shape (x,y) was y-1 to -x+1 descending.
       diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
       
       # Another list comp to convert back to Python lists from numpy arrays
       return [n.tolist() for n in diags]

   # difference with e2: this one only checks 2 diagonals
   def e1(self):
      values = [0, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000, 10000000000]
      v = 0

      # checking number of X and Os in each ROW
      for i in range(self.size):
         count_o = 0
         count_x = 0
         for k in range(self.size):
            if self.current_state[i][k] == "O":
               count_o += 1
            elif self.current_state[i][k] == "X":
               count_x += 1

         # calculating e(n) value depending on the winning condition size
         v += self.update_v(count_o, count_x, values)

      # checking number of Xs and Os in each COLUMN
      for i in range(self.size):
         count_o = 0
         count_x = 0
         for k in range(self.size):
            if self.current_state[k][i] == "O":
               count_o += 1
            elif self.current_state[k][i] == "X":
               count_x += 1

         v += self.update_v(count_o, count_x, values)

      count_o, count_x = 0, 0
      # checking number of Xs and Os in left DIAGONAL
      for i in range(self.size):
         if self.current_state[i][i] == "O":
            count_o += 1
         elif self.current_state[i][i] == "X":
            count_x += 1

      v += self.update_v(count_o, count_x, values)

      count_o, count_x = 0, 0
      # checking number of Xs and Os in right DIAGONAL
      for i in range(self.size):
         if self.current_state[i][self.size-i-1] == "O":
            count_o += 1
         elif self.current_state[i][self.size-i-1] == "X":
            count_x += 1

      v += self.update_v(count_o, count_x, values)
      return v


   # difference with e1: this one checks all diagonals
   def e2(self):
      values = [0, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000, 10000000000]
      v = 0

      # checking number of X and Os in each ROW
      for i in range(self.size):
         count_o = 0
         count_x = 0
         for k in range(self.size):
            if self.current_state[i][k] == "O":
               count_o += 1
            elif self.current_state[i][k] == "X":
               count_x += 1

         # calculating e(n) value depending on the winning condition size
         v += self.update_v(count_o, count_x, values)

      # checking number of Xs and Os in each COLUMN
      for i in range(self.size):
         count_o = 0
         count_x = 0
         for k in range(self.size):
            if self.current_state[k][i] == "O":
               count_o += 1
            elif self.current_state[k][i] == "X":
               count_x += 1

         v += self.update_v(count_o, count_x, values)

      # checking number of Xs and Os in all DIAGONALS
      diagonals = self.generate_diagonals()
      for diag in diagonals:
         count_o, count_x = 0, 0
         if len(diag) >= self.winning_line_up_size:
            for k in range(len(diag)):
               if diag[k] == "O":
                  count_o += 1
               elif diag[k] == "X":
                  count_x += 1

         v += self.update_v(count_o, count_x, values)
      
      return v

   def minimax(self, max_depth, start_time, max=False):
      # Minimizing for 'X' and maximizing for 'O'
      # Possible values are:
      # -1 - win for 'X'
      # 0  - a tie
      # 1  - loss for 'X'
      # We're initially setting it to 2 or -2 as worse than the worst case:
      value = (10**(self.size) * self.size**2)
      if max:
         value = -1* (10**(self.size) * self.size**2)
      x = None
      y = None
      result = self.is_end()
      if (max_depth == 0 or result == 'X' or result == 'Y' or result == '.' or start_time + self.allowed_time < time.time()):
        if self.player_turn == 'X': 
            return (self.e1(), x, y)
        else:
            return (self.e2(), x, y)
      for i in range(0, self.size):
         for j in range(0, self.size):
            if self.current_state[i][j] == '.':
               if max:
                  self.current_state[i][j] = 'O'
                  (v, _, _) = self.minimax(max_depth-1,start_time,max=False)
                  if v > value:
                     value = v
                     x = i
                     y = j
               else:
                  self.current_state[i][j] = 'X'
                  (v, _, _) = self.minimax(max_depth-1,start_time,max=True)
                  if v < value:
                     value = v
                     x = i
                     y = j
               self.current_state[i][j] = '.'
      return (value, x, y)

   def alphabeta(self, max_depth, start_time, alpha=-2, beta=2, max=False):
      # Minimizing for 'X' and maximizing for 'O'
      # Possible values are:
      # -1 - win for 'X'
      # 0  - a tie
      # 1  - loss for 'X'
      # We're initially setting it to 2 or -2 as worse than the worst case:
      value = (10**(self.size) * self.size**2)
      if max:
         value = -1* (10**(self.size) * self.size**2)
      x = None
      y = None
      result = self.is_end()
      if (max_depth == 0 or result == 'X' or result == 'Y' or result == '.' or start_time + self.allowed_time < time.time()):
        if self.player_turn == 'X': 
            return (self.e1(), x, y)
        else:
            return (self.e2(), x, y)
      for i in range(0, self.size):
         for j in range(0, self.size):
            if self.current_state[i][j] == '.':
               if max:
                  self.current_state[i][j] = 'O'
                  (v, _, _) = self.alphabeta(max_depth-1,start_time, alpha, beta, max=False)
                  if v > value:
                     value = v
                     x = i
                     y = j
               else:
                  self.current_state[i][j] = 'X'
                  (v, _, _) = self.alphabeta(max_depth-1,start_time, alpha, beta, max=True)
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
               (_, x, y) = self.minimax(self.player1_maximum_depth,time.time(),max=False)
            else:
               (_, x, y) = self.minimax(self.player2_maximum_depth,time.time(),max=True)
         else: # algo == self.ALPHABETA
            if self.player_turn == 'X':
               (m, x, y) = self.alphabeta(self.player1_maximum_depth,time.time(),max=False)
            else:
               (m, x, y) = self.alphabeta(self.player2_maximum_depth,time.time(),max=True)
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

