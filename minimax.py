import copy

SIZE = 3
player_dict = {0: 'X', 1:'O'}
winning_combos = ['XXX', 'OOO']

def gameOver(board):
	diag_left, diag_right = '', ''
	for i in range(SIZE):
		rows, cols = '', ''
		for j in range(SIZE):
			if i == j: diag_left = diag_left + str(board[i][j])
			if (i == 0 and j == SIZE-1) or (i == SIZE-1 and j == 0) or (i == 1 and j == 1): 
				diag_right = diag_right + str(board[i][j]) 
			rows = rows + str(board[i][j])
			cols = cols + str(board[j][i])
		if rows in winning_combos: 
			return winning_combos.index(rows)
		elif cols in winning_combos: 
			return winning_combos.index(cols)

	if diag_left in winning_combos: 
		return winning_combos.index(diag_left)
	elif diag_right in winning_combos: 
		return winning_combos.index(diag_right)
	if len(posMoves(board)) == 0:
		return 2
	return -1

def getScore(board, depth, ai_player):
	winner = gameOver(board)
	if ai_player == winner: 
		return 10 - depth
	elif winner == 2:
		return 0 # draw
	else: 
		return depth - 10
		
def initBoard(board):
	dummy_val = 1
	dummy_dict = dict()
	for i in range(SIZE):
		for j in range(SIZE):
			board[i][j] = dummy_val
			dummy_dict[dummy_val] = (i,j)
			dummy_val += 1
	return dummy_dict

def printBoard(board):
	print('Game board\n')
	for i in range(SIZE):
		print '|',
		for j in range(SIZE):
			print board[i][j], '|',
		print '\n'

def findBestMove(board, ai_player):
	best_move = None
	best_move_score = -1000
	for move in posMoves(board):
		board_temp = copy.deepcopy(board)
		board_temp[move[0]][move[1]] = player_dict[ai_player]
		score = minimax(board_temp, depth=0, ai_player=ai_player, ai_active=False)
		if score >= best_move_score:
			best_move_score = score
			best_move = move
		print score, move
	return best_move

def posMoves(board):
	pos_moves = []
	for i in range(SIZE):
		for j in range(SIZE):
			if board[i][j] in [x for x in range(1,10)]:
				pos_moves.append([i,j])
	return pos_moves

def minimax(board, depth, ai_player, ai_active):
	if gameOver(board) >= 0:
		return getScore(board, depth, ai_player)

	if ai_active:
		best_score = -1000
		for move in posMoves(board):
			board_temp = copy.deepcopy(board)
			board_temp[move[0]][move[1]] = player_dict[ai_player]
			score = minimax(board_temp, depth+1, ai_player, False)
			best_score = max(best_score, score)
		return best_score
	else:
		best_score = 1000
		for move in posMoves(board):
			player = 0 if ai_player == 1 else 1
			board_temp = copy.deepcopy(board)
			board_temp[move[0]][move[1]] = player_dict[player]
			score = minimax(board_temp, depth+1, ai_player, True)
			best_score = min(best_score, score)
		return best_score

def main():
	board = [[None for i in range(SIZE)] for j in range(SIZE)]

	while True:
		dummy_dict = initBoard(board)
		player_first = raw_input('Would you like to go first [y/n]: ')
		if player_first == 'y': 
			player, ai_player = 0, 1
		else: 
			player, ai_player = 1, 0
		print 'Alright! Your marker is ', player_dict[player], '.\n'
		printBoard(board)

		turn = 0
		while gameOver(board) < 0:
			if (player_first == 'y' and turn == 0) or turn > 0:
				dummy = raw_input('Choose a tile from 1-9: ')
				player_move = dummy_dict[int(dummy)]
				board[player_move[0]][player_move[1]] = player_dict[player]
				printBoard(board)

			if gameOver(board) < 0:
				print 'Ai is thinking...'
				ai_move = findBestMove(board, ai_player)
				board[ai_move[0]][ai_move[1]] = player_dict[ai_player]
				printBoard(board)
				turn += 1
			else: 
				break

		print 'Game over! ',
		if gameOver(board) == 2:
			print("It's a tie.")
		elif gameOver(board) == ai_player:
			print('You lose, AI wins!')
		else:
			print('Congrats, you win!')
		response = raw_input('Would you like to play again? [y/n]: ')
		if response == 'n':
			break

if __name__ == '__main__':
    main()

