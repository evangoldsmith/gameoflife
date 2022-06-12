import copy
import time

start = True
row = 0
col = 0
selections = []
board = []

#Defines function for outputing different colors in console
def prRedSpace(skk): print("\033[91m {}\033[00m" .format(skk), end = " ")
def prGreenSpace(skk): print("\033[92m {}\033[00m" .format(skk), end = " ")
def prRed(skk): print("\033[91m {}\033[00m" .format(skk) + '\n')
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk) + '\n')


#Title sequence and resolution selection
while (start):
	game = "\033[1;32;40m Conway's Game of Life!"
	response = input("Welcome to " + "\033[1m" + game + "\033[0m" + "\nSelect Your Number of Rows and Columns\n")
	mid = 0
	try:
		mid = response.index('x')
	except ValueError:
		print ("ERROR\nUse 1x1 format")
	else:
		row = int(response[:mid])
		col = int(response[mid + 1:])
		board = [0] * (row * col)
		start = False


#Prints original board
def printBoard(rows, cols):
	board = [0] * (row * col)
	tot = 0
	update = False
	for x in range(cols):
		print('r' + str(x), end = ' ')
	print('\n')
	for i in range(rows):
		for j in range(cols):
			tot = tot + 1
			for k in selections:
				if (tot == k):
					update = True

			if (tot % cols < 1):
				if (update):
					prGreen('1')
					update = False
					board.append(1)
				else:
					prRed('0')
					board.append(0)
			else:
				if (update):
					prGreenSpace('1')
					update = False
					board.append(1)
				else:
					prRedSpace('0')
					board.append(0)


#Checks each living cell and updates board, then prints new board
def playBoard():
	x = 0
	y = 0
	length = (col * row) - 1
	newboard = board.copy()


	for j in range(0, length):
		if (checkTouching(j) > 0):
			if (checkTouching(j) == 3):
				if (board[j] == 0):
					print('cell born! at ' + str(j))
					newboard[j] = 1
			if (checkTouching(j) > 3):
				if (board[j] == 1):
					print('cell killed! at ' + str(j))
					newboard[j] = 0
			if (checkTouching(j) < 2):
				if (board[j] == 1):
					print('cell killed! at ' + str(j))
					newboard[j] = 0
				
	print('\n\n\n')
	for i in newboard:
		x = x + 1
		if (x % col < 1):
			if (i == 1):
				prGreen(str(i))
				selections.append(y + 1)
			if (i == 0):
				prRed(str(i))
			board[y] = i
		else:
			if (i == 1):
				prGreenSpace(str(i))
				selections.append(y + 1)
			if (i == 0):
				prRedSpace(str(i))
			
			board[y] = i
		y = y + 1
	
		

#Returns number of alive cells touching selected cell
def checkTouching(cell):
	touching = 0
	corner = 0
	if ((cell + 1) % col == 0):
		corner = 1
	if (cell % col == 0):
		corner = 2
	if (corner == 0):
		positions = [(cell - col) - 1, cell - col, (cell - col) + 1, cell - 1, cell + 1, (cell + col) - 1, cell + col, (cell + col) + 1]
	if (corner == 1):
		positions = [(cell - col) - 1, cell - col, cell - 1, (cell + col) - 1, cell + col]
	if (corner == 2):
		positions = [cell - col, (cell - col) + 1, cell + 1, cell + col, (cell + col) + 1]
	for i in positions:
		if (i > 0 & i < (col * row) - 1):
			if (i < (col * row)):
				if (board[i] == 1):
					touching = touching + 1
	
	return touching


			
#Formats selections into input for simulation
def readSelection(choice):
	mid = 0
	aspot = 0
	num = 0
	try:
		mid = choice.index('x')
		aspot = choice.index('r')
	except ValueError:
		print ("ERROR\nUse A1x1 format")
	else:
		num = (int(choice[mid + 1:]) * col) + (int(choice[aspot + 1:mid]))
		prGreen(str(num))	
		board[num] = 1
		selections.append(num + 1)
		printBoard(row, col)

#Animates board changes every 0.2s
def timePlay(frames):
	for i in range(0, frames):
		time.sleep(0.2)
		playBoard()
		
		

printBoard(row, col)
selecting = True
prRed('COMMANDS: ')
print('r0x0  :  Selects cell')
print('clear  :  Clears board')
print('play x  : Plays board for selected number of frames')
print('stop  :  Ends program')
print('glider  :  Spawns glider')
while (selecting):
	tileselect = input("Select command ")
	if (tileselect == "stop"):
		break
	elif (tileselect == 'help'):
		prRed('COMMANDS: ')
		print('r0x0  :  Selects cell')
		print('clear  :  Clears board')
		print('play x  : Plays board for selected number of frames')
		print('stop  :  Ends program')
		print('glider  :  Spawns glider')
	elif (tileselect == ' '):
		selections = []
		playBoard()
	elif (tileselect == 'clear'):
		selections = []
		board = [0] * (row * col)
		printBoard(row, col)
	elif ('play' in tileselect):
		selections = []
		try:
			mid = tileselect.index(' ')
		except ValueError:
			print("ERROR\nIncorrect Format")
		else:
			numframes = int(tileselect[mid + 1:])
			timePlay(numframes)
	elif (tileselect == 'undo'):
		sellength = len(selections)

		if (sellength > 0):
			board[(selections[sellength -  1]) - 1] = 0
			selections.pop(sellength - 1)
			
			printBoard(row, col)
	elif (tileselect == 'glider'):
		if (col > 2 and row > 2):
			selections = [(col * 2) + 1, (col * 2) + 2, (col * 2) + 3, col + 3, 2]
			for i in selections:
				board[i - 1] = 1
			printBoard(row, col)
		else:
			print('ERROR \nWindow Not Large Enough')
	elif (tileselect == 'allone'):
		for i in range(0, (row * col) + 1):
			selections.append(i)
		for i in selections:
			board[i - 1] = 1
		printBoard(row, col)
	else:
		readSelection(tileselect)
	


	