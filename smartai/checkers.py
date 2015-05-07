import json, sys
import copy

def get_color(piece):
	""" This function takes in the piece you are playing as a string
	    then return the string of the color being played.
	"""
	if piece in ('r', 'R'):
		return 'red'

	if piece in ('b', 'B'):
		return 'black'

def is_king(piece):
	if piece in ('R', 'B'):
		return True
	return False

def location_in_board(pos):
	r, c = pos
	if r < 0 or c < 0:
		return False

	if r > 7 or c > 7:
		return False

	return True

def execute_move(s, move):	
	state = copy.deepcopy(s)
	for item in move:
		sr, sc = item[0]
		dr, dc = item[1]

		state[sr][sc], state[dr][dc] = ' ', state[sr][sc]

		if dr == 7 and get_color(state[dr][dc]) == 'black':
			state[dr][dc] = 'B'
		elif dr == 0 and get_color(state[dr][dc]) == 'red':
			state[dr][dc] = 'R'

		ir = sr - dr
		ic = sc - dc
		mr = sr-abs(ir)/ir
		mc = sc-abs(ic)/ic
		if (mr, mc) != (dr, dc) and location_in_board((mr, mc)):
			state[mr][mc] = ' '
	return state

def get_pos_pieces(state):
	""" This function returns pieces locations in the order of (black, red)
	"""
	# get location of black and red pieces
	black = []
	red = []
	for r in range(len(state)):
		for c in range(len(state[r])):
			if get_color(state[r][c]) == 'black':
				black.append((r,c))
			elif get_color(state[r][c]) == 'red':
				red.append((r,c))

	return (black, red)

def check_for_jump(state, my_color, e_pos, inc, d):
	if d == 'left':
		z = -1
	elif d == 'right':
		z = 1

	# check to see if e_pos is enemy piece
	r, c = e_pos
	if get_color(state[r][c]) == my_color: 
		return None

	# check to see if spot after e_pos is a space
	r1 = r + 1*inc
	c1 = c + z
	if location_in_board((r1, c1)): 
		if state[r1][c1] == ' ':
			return (r1, c1)

	return None

def check_move(s, my_color, pos, cpos, inc, direction, c_type = 'Normal'):
	state = copy.deepcopy(s)
	r, c = pos
	cr, cc = cpos
	moves = []
	if location_in_board(cpos):
		if state[cr][cc] != ' ': 
			move = check_for_jump(state, my_color, cpos, inc, direction)
			if move:
				temp = [((r,c), (move[0], move[1]))]
				checkL = (move[0]+1*inc, move[1]-1)
				checkR = (move[0]+1*inc, move[1]+1)

				left = check_move(state, my_color, move, checkL, inc, 'left', 'Jump')
				right = check_move(state, my_color, move, checkR, inc, 'right', 'Jump')

				for item in left:
					temp += item

				for item in right:
					temp += item

				moves.append((temp))		
		else:
			if c_type == 'Normal':
				moves.append(('nj', [((r,c), (cr, cc))]))
	return moves

def get_move_piece(state, my_color, pos, inc):
	r, c = pos
	checkL = (r+1*inc, c-1)
	checkR = (r+1*inc, c+1)

	moves = []
	left = check_move(state, my_color, pos, checkL, inc, 'left')
	moves += left

	right = check_move(state, my_color, pos, checkR, inc, 'right')
	moves += right

	if is_king(state[r][c]):
		KcheckL = (r+1*inc*-1, c-1)
		KcheckR = (r+1*inc*-1, c+1)
		kLeft = check_move(state, my_color, pos, KcheckL, inc*-1, 'left')
		moves += kLeft

		kRight = check_move(state, my_color, pos, KcheckR, inc*-1, 'right')
		moves += kRight

	return state, moves

def check_for_split(move):
	pops = []
	s = (0, 0)
	d = move[0][0]
	for item in move:
		cs = item[0]
		cd = item[1]
		if cs != d:
			move.pop(move.index((s, d)))
			move.pop(move.index((cs, cd)))
			pops.append((s, d))
			pops.append((cs, cd))
		s, d = (cs, cd)

	if pops:
		new_list = []
		for item in pops:
			new_list += [move + [item]]
	else:
		new_list = [move]

	return new_list

def list_of_moves(state, my_color, pieces, inc):
	moves = []
	for piece in pieces:
		state, move = get_move_piece(state, my_color, piece, inc)
		if move:
			for item in move:
				moves.append(item)

	jumps = []
	non_jumps = []
	for item in moves:
		if item[0] == 'nj':
			non_jumps.append(item[1])
		else:
			move = check_for_split(item)
			for m in move:
				jumps.append(m)

	moves = []
	if jumps:
		moves = jumps
	else:
		moves = non_jumps

	return moves

# positive -> black
# negitive -> red
def grade_board(state):
	grade = 0
	for row in range(len(state)):
		for col in range(len(state[row])):
			if get_color(state[row][col]) == 'black':
				inc = 1
			elif get_color(state[row][col]) == 'red':
				inc = -1
			
			if is_king(state[row][col]):
				grade += 2 * inc
			elif i != ' ':
				grade += 1 * inc

			if row == 7 or col == 7 or row == 0 or col == 0:
				grade += 5 * inc
	return grade

def minimax(s, my_color):
	state = copy.deepcopy(s)
	val = -1
	if my_color == 'black':
		move = max_value(state, 5,5)
	elif my_color == 'red':
		move  = min_value(state, 5,5)
	return move

def max_value(s, depth, max_depth):
	state = copy.deepcopy(s)
	if depth == 0:
		return grade_board(state)

	v = -10000
	p = get_pos_pieces(state)
	pieces = p[0]
	best = None
	moves = list_of_moves(state, 'black', pieces, 1)
	for move in moves:
		s = execute_move(state, move)
		m = min_value(s, depth-1, max_depth)
		if m < v:
			return v
		if m >= v:
			v = m
			best = move

	if depth == max_depth or not p[0] or not p[1]:
		return best
	else:
		return v

def min_value(s, depth, max_depth):
	state = copy.deepcopy(s)
	if depth == 0:
		return grade_board(state)

	v = 10000
	p = get_pos_pieces(state)
	pieces = p[1]
	best = None
	moves = list_of_moves(state, 'red', pieces, -1)
	for move in moves:
		s = execute_move(state, move)
		m = max_value(s, depth-1, max_depth)
		if m > v:
			return v
		if m <= v:
			v = m
			best = move

	if depth == max_depth or not p[0] or not p[1]:
		return best
	else:
		return v

def get_move(state, time_limit, turn):
	""" This function takes in the json string of board state,
	    the timer as an integer, and what color you are playing as r or b.
	    Then returns the json string of the move sequence which is a list of lists of lists
	"""
	state = json.loads(state)
	my_color = get_color(turn)
	pieces_location = get_pos_pieces(state)
	if my_color == 'black':
		pieces = pieces_location[0]
		inc = 1
	elif my_color == 'red':
		pieces = pieces_location[1]
		inc = -1
	
	move = minimax(list(state), my_color)
	# if not move:
	# 	print 'bad'
	# 	import random
	# 	move = random.choice(list_of_moves(s, my_color, pieces, inc))

	choice = json.dumps(move)
	return choice


def print_board(state):
	num = 0

	# print top numbers
	print '  ',
	for x in range(8):
		sys.stdout.write(str(x))
	print

	# print side numbers and board
	print ' ', '-'*8
	for item in state:
		print num, 
		num += 1
		sys.stdout.write('|')
		for i in item:
			sys.stdout.write(i)
		print '|'
	print ' ', '-'*8

if __name__ == "__main__":
	state = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', 'b'],
			 [' ', ' ', 'b', ' ', ' ', ' ', ' ', ' '],
			 [' ', 'r', ' ', ' ', ' ', ' ', ' ', 'b'],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', 'b', ' ', 'b', ' ', ' '],
			 ['b', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			 [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'r'],
			 [' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ']]

	print_board(state)
	move = get_move(json.dumps(state), 10, 'b')
	print move