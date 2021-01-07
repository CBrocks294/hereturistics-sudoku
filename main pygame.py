import copy
import time
import pygame
pygame.init()
def drawPygame(Board):
	def message_display(text,XPos,YPos, col):
		text_size = pygame.font.Font('freesansbold.ttf',int(50))
		TextSurf, TextRect = text_objects(text, text_size, col)
		TextRect.center = (XPos,YPos)
		screen.blit(TextSurf, TextRect)


	def text_objects(text,font,col):
		textSurface = font.render(text, True, col)
		return textSurface, textSurface.get_rect()

	screen=pygame.display.set_mode((600,600))
	clock = pygame.time.Clock()
	screen.fill((255,255,255))
	for ypos, y in enumerate(Board):
		for xpos, x in enumerate(y):
			black = (0,0,0)
			if type(x)!= list:
				x = str(x)
				message_display(x, xpos*600/9+300/9, ypos*600/9+300/9, black) 
			#else:  message_display('0', xpos*600/9+300/9, ypos*600/9+300/9, black)
	pygame.display.update()


def heuristics(Board):
	Pos = [0,0]
	Box = [(0,3),(3,6),(6,9)]
	for Pos[0], Y in enumerate(Board):
		for Pos[1], X in enumerate(Y):
			if X == 0:
				PossibleNums  = []
				for Number in range(1,10):
					InXOrY = False
					InGrid = False
					#checks the x and y for the number
					for SearchPos in range (9):
						if Board[Pos[0]][SearchPos] == Number or Board[SearchPos][Pos[1]] == Number:
							InXOrY = True
							break
					if InXOrY: continue
					#checks 3x3 box for the number
					LoopParamsY = (Box[int(Pos[0]/3)])
					for BoxY in range(int(LoopParamsY[0]), LoopParamsY[1]):
						LoopParamsX = (Box[int(Pos[1]/3)])
						for BoxX in range (int(LoopParamsX[0]), LoopParamsX[1]):
							if Board[BoxY][BoxX] == Number: 
								InGrid = True
								break
						if InGrid: break
					if InGrid: continue
					PossibleNums.append(Number)
				if len(PossibleNums)>0:
					Board[Pos[0]][Pos[1]] = PossibleNums
				else: return False
	return(Board)
	
def heuristicscheck(Board):
	Box = [(0,3),(3,6),(6,9)]
	ContinueSearch = False
	for YPos, Y in enumerate(Board):
		for XPos, Values in enumerate(Y):
			if type(Values) == list:
				ContinueSearch = True
				for ValuePos,Check in enumerate(Values):
					InXOrY = False
					InGrid = False
					#checks the x and y for the number
					for SearchPos in range (9):
						if (Board[YPos][SearchPos] == Check or Board[SearchPos][XPos] == Check):
							InXOrY = True
							break
					if InXOrY:
						Values.pop(ValuePos)
						continue
					if InXOrY: continue
					#checks 3x3 box for the number
					LoopParamsY = (Box[int(YPos/3)])
					for BoxY in range(int(LoopParamsY[0]), LoopParamsY[1]):
						LoopParamsX = (Box[int(XPos/3)])
						for BoxX in range (int(LoopParamsX[0]), LoopParamsX[1]):
							if Board[BoxY][BoxX] == Check: 
								InGrid = True
								break
						if InGrid: break
					if InGrid:
						Values.pop(ValuePos)
						continue
				if len(Values)== 0:
					return False
				else: 
					Board[YPos][XPos] == Values
	if not ContinueSearch: 
		print(Board)
		print (time.time()-(start))
		exit()
	return(Board)
					
def solve(Board):
	Short = 10
	ShortPos= []
	for YPos,Y in enumerate(Board):
		for XPos, Value in enumerate(Y):
			if type(Value) == list:
				if len(Value) < Short:
					Short = len(Value)
					ShortPos = [YPos,XPos]
	for TestValue in (Board[ShortPos[0]][ShortPos[1]]):
		NewBoard =  copy.deepcopy(Board)
		NewBoard[ShortPos[0]][ShortPos[1]] = TestValue
		NewBoard = heuristicscheck(NewBoard)
		if NewBoard == False: continue
		drawPygame(NewBoard)
		solve(NewBoard)	
	return

def makeBoard():
	Board = [
[0,0,0,2,6,0,7,0,1],
[6,8,0,0,7,0,0,9,0],
[1,9,0,0,0,4,5,0,0],
[8,2,0,1,0,0,0,4,0],
[0,0,4,6,0,2,9,0,0],
[0,5,0,0,0,3,0,2,8],
[0,0,9,3,0,0,0,7,4],
[0,4,0,0,5,0,0,3,6],
[7,0,3,0,1,8,0,0,0]]
	return Board


start = time.time()
Board = makeBoard()
Board = heuristics(Board)
if Board == False:
	print('there are no possible solutions')
	exit()
solve(Board)