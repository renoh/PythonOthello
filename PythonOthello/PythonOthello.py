all_direction = [-11, -10, -9, -1, 1, 9, 10, 11]
empty, black, white, outer = range(4)
all_squares = [x for x in range(11, 88 + 1) if ( 1 <= x%10 <= 8)]

def name_of (piece):
  return ".@O?"[piece]

def opponent (player):
  return white if player == black else black

def initial_board ():
  board = [outer] * 100
  for x in all_squares: board[x] = empty
  board[44], board [45] = white, black
  board[54], board [55] = black, white
  return board

def print_board (board):
  print "   1 2 3 4 5 6 7 8   [{0}={1} {2}={3} ({4:+})]".format(
      name_of(black), board.count(black),
      name_of(white), board.count(white),
      count_difference(black, board)
      )
  for row in range (1, 9):
    print "{0}".format(row * 10),
    for col in range (1, 9):
      print "{0}".format(name_of(board[10*row + col])),
    print"" 
  print""

def count_difference (player, board):
  return board.count(player) - board.count(opponent(player))

import numbers
def valid_p (move):
  return isinstance(move, numbers.Integral) and 11 <=  move <= 88 and 1 <= move%10 <= 8

def legal_p (move, player, board):
  return board[move] is empty and any ([would_flip(move, player, board, dir) is not None for dir in all_direction])

def would_flip(move, player, board, dir):
  c = move + dir
  return None if board[c] is not opponent(player) else find_bracketing_piece (c + dir, player, board, dir)

def find_bracketing_piece(square, player, board, dir):
  if   board[square] is player: return square
  elif board[square] is opponent(player): return find_bracketing_piece(square + dir, player, board, dir)
  else: return None

def make_move (move, player, board):
  board[move] = player
  for dir in all_direction: make_flips(move, player, board, dir)

def make_flips (move, player, board, dir):
  bracketer = would_flip(move, player, board, dir)
  if bracketer is not None:
    c = move
    while c is not bracketer:
      board[c] = player
      c += dir

def any_legal_move (player, board):
  return any ([legal_p(move, player, board) for move in all_squares])

def next_to_play (board, previous_player, boolPrint = True):
  opp = opponent(previous_player)
  if   any_legal_move(opp, board): return opp
  elif any_legal_move (previous_player, board): 
    if boolPrint: print "{0} has no moves and must pass.".format(name_of(opp))
    return previous_player
  else: None

def get_move (strategy, player, board, boolPrint = True):
  if boolPrint: print_board(board)
  boardAux = list(board)
  move = strategy(player, boardAux)
  if valid_p(move) and legal_p(move, player, board):
    if boolPrint: print "{0} moves to {1}.".format(name_of(player), move)
    make_move(move, player, board)
  else:
    if boolPrint: print "Illegal move: {0}".format(move)
    get_move(strategy, player, board, boolPrint)

# strategies:
# human
def human(player, board):
  return input("{0} to move: ".format(name_of(player)))

# random
import random
def random_strategy(player, board):
  return random.choice(legal_moves(player, board))
def legal_moves(player, board):
  return [move for move in all_squares if legal_p(move, player, board)]


def othello(bl_strategy, wh_strategy, boolPrint = True):
  board = initial_board()
  player = black
  while player is not None:
    strategy = bl_strategy if player is black else wh_strategy
    get_move(strategy, player, board, boolPrint)
    player = next_to_play(board, player, boolPrint)
  #if boolPrint: 
  print "The game is over. Final result: {0:+}".format(count_difference(black, board))
  print_board(board)


print "start of the game"
othello(random_strategy, random_strategy, False)
print "end of the game"


#print "\ntests constants"
#print all_direction
#print empty, black, white, outer
#print all_squares

#print "\ntests function name_of"
#print name_of(empty)
#print name_of(black)
#print name_of(white)
#print name_of(outer)

#print "\ntests function opponent"
#print name_of(opponent(black))
#print name_of(opponent(white))

#print "\ntests function initial_board"
#board = initial_board()
#board[1] = 99
#board2 = initial_board()
#board3 = list(board)
#board[2] = 98
#print board
#print board2
#print board3

#print "\ntests function print_board"
#board = initial_board()
#print_board(board)
#board[11] = black
#print_board(board)
#board[12] = white
#print_board(board)
#board[13] = white
#print_board(board)
#board[14] = black
#print_board(board)

#print "\ntests function valid_p"
#print valid_p(11)
#print valid_p(20)
#print valid_p(200)
#print valid_p('a')
#print valid_p("a")

#print "\ntests function legal_p, would_flip, find_bracketing_piece"
#board = initial_board()
#print_board(board)
#print "11 = " + str(legal_p(11, black, board))
#print "54 = " + str(legal_p(54, black, board))
#print "56 = " + str(legal_p(56, black, board))
#print "65 = " + str(legal_p(65, black, board))
#print "76 = " + str(legal_p(76, black, board))
#print "64 = " + str(legal_p(64, black, board))

#print "\ntests function make_move, make_flips"
#board = initial_board()
#print_board(board)
#make_move(65, black, board)
#print_board(board)

#print "\ntests func any_legal_move next_to_play"
#board = initial_board()
#print_board(board)
#print next_to_play (board, white)
#print next_to_play (board, black)
#print any_legal_move(black, board)
#make_move(65, black, board)
#print_board(board)
#print any_legal_move(black, board)
#print next_to_play (board, white)
#print next_to_play (board, black)
#make_move(33, black, board)
#print_board(board)
#print any_legal_move(black, board)
#print next_to_play (board, white)
#print next_to_play (board, black)

#print "\ntests function get_move, legal_moves, random_strategy, human"
#board = initial_board()
#print legal_moves(black, board)
#get_move(human, black, board)
#print_board(board)

