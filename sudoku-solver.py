# import pygame, clingo and re library
import pygame
import clingo
import re

# initialise the pygame font
pygame.font.init()

# Total window
screen = pygame.display.set_mode((500, 600))

# Title and Icon
pygame.display.set_caption("SUDOKU AI SOLVER")

x = 0
y = 0
dif = 500 / 9
val = 0
# Default Empty Sudoku Board.
grid =[
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0]
	]

# Load test fonts for future use
font1 = pygame.font.SysFont("comicsans", 30)
font2 = pygame.font.SysFont("comicsans", 20)
def get_cord(pos):
	global x
	x = pos[0]//dif
	global y
	y = pos[1]//dif

# Highlight the cell selected
def draw_box():
	for i in range(2):
		pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i)*dif), (x * dif + dif + 3, (y + i)*dif), 7)
		pygame.draw.line(screen, (255, 0, 0), ( (x + i)* dif, y * dif ), ((x + i) * dif, y * dif + dif), 7)

# Function to draw required lines for making Sudoku grid		
def draw():
	# Draw the lines
		
	for i in range (9):
		for j in range (9):
			if grid[i][j]!= 0:

				# Fill color in already numbered grid
				pygame.draw.rect(screen, (255, 255, 0), (i * dif, j * dif, dif + 1, dif + 1))

				# Fill grid with default numbers specified
				text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
				screen.blit(text1, (i * dif + 15, j * dif + 15))
	# Draw lines horizontally and verticallyto form grid		
	for i in range(10):
		if i % 3 == 0 :
			thick = 7
		else:
			thick = 1
		pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
		pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)	

# Fill value entered in cell	
def draw_val(val):
	text1 = font1.render(str(val), 1, (0, 0, 0))
	screen.blit(text1, (x * dif + 15, y * dif + 35))

# Raise error when wrong values entered
def raise_error():
	text1 = font1.render("WRONG !!!", 1, (178, 34, 34))
	screen.blit(text1, (20, 560)) 

# Create context for clingo
class Context:
	def id(x):
		return x
	def seq(x, y):
		return [x, y]

# return result atoms as a string
models= ""
def addModel(m):
	global models
	models = str(m)

# Solves the sudoku board using Answer Set Programming
def solve():
	prg= clingo.Control()
	# read ASP encoding from file
	file = open("./solver-encoding.lp")
	encoding = file.read().replace("\n", " ")
	file.close()
	prg.add("sudoku", [], encoding)
	# add numbers already present in the grid
	for j in range(0,9):
		for i in range(0,9):
			if grid[i][j] != 0:
				prg.add("sudoku", [], "cell("+str(grid[i][j])+","+str(i)+","+str(j)+").")
		
	prg.ground([("sudoku", [])], context=Context())
	# the AI solves the problem
	prg.solve(on_model=addModel)
	if models == "":
		return False
	atoms = models.split(" ")
	# cells are filled with values found by AI
	for atom in atoms:
		res = re.findall(r'[0-9]', atom)
		i = int(res[1])
		j = int(res[2])
		grid[i][j] = int(res[0])
		global x, y
		x = i
		y = j
		# white color background
		screen.fill((255, 255, 255))
		draw()
		draw_box()
		pygame.display.update()
		pygame.time.delay(20)
	return True

# Display instruction for the game
def instruction():
	text1 = font2.render("PRESS R TO EMPTY", 1, (0, 0, 0))
	text2 = font2.render("ENTER VALUES AND PRESS ENTER TO SOLVE", 1, (0, 0, 0))
	screen.blit(text1, (20, 520))	
	screen.blit(text2, (20, 540))

run = True
flag1 = 0
flag2 = 0
rs = 0
error = 0
# The loop thats keep the window running
while run:
	
	# White color background
	screen.fill((255, 255, 255))
	# Loop through the events stored in event.get()
	for event in pygame.event.get():
		# Quit the game window
		if event.type == pygame.QUIT:
			run = False
		# Get the mouse position to insert number
		if event.type == pygame.MOUSEBUTTONDOWN:
			flag1 = 1
			pos = pygame.mouse.get_pos()
			get_cord(pos)
		# Get the number to be inserted if key pressed
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				x-= 1
				flag1 = 1
			if event.key == pygame.K_RIGHT:
				x+= 1
				flag1 = 1
			if event.key == pygame.K_UP:
				y-= 1
				flag1 = 1
			if event.key == pygame.K_DOWN:
				y+= 1
				flag1 = 1
			if event.key == pygame.K_1:
				val = 1
			if event.key == pygame.K_2:
				val = 2
			if event.key == pygame.K_3:
				val = 3
			if event.key == pygame.K_4:
				val = 4
			if event.key == pygame.K_5:
				val = 5
			if event.key == pygame.K_6:
				val = 6
			if event.key == pygame.K_7:
				val = 7
			if event.key == pygame.K_8:
				val = 8
			if event.key == pygame.K_9:
				val = 9
			if event.key == pygame.K_RETURN:
				flag2 = 1
			# If R pressed clear the sudoku board and other variables
			if event.key == pygame.K_r:
				rs = 0
				error = 0
				flag2 = 0
				models = ""
				grid =[
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0],
				[0, 0, 0, 0, 0, 0, 0, 0, 0]
				]
	if flag2 == 1:
		if solve()== False:
			error = 1
		else:
			rs = 1
		flag2 = 0
	if val != 0:		
		draw_val(val)
		grid[int(x)][int(y)]= val
		flag1 = 0
		val = 0
	if error == 1:
		raise_error()
	draw()
	if flag1 == 1:
		draw_box()	
	instruction()

	# Update window
	pygame.display.update()

# Quit pygame window
pygame.quit()	
	
