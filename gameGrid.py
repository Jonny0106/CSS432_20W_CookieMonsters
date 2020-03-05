import pygame
import battleship
import player

#each player gets a board
class BoardGame:
    #constructor 
    def __init__(self, WINDOW_X, WINDOW_Y, square_size, margin, AMOUNT):
        self.WINDOW_X = WINDOW_X
        self.square_size = square_size
        self.margin = margin
        self.AMOUNT = AMOUNT
        self.WINDOW_Y = WINDOW_Y

    
    def make_grid(self, x, y):
        self.grid = []
        self.grid2 = []
        self.grid3 = []
        self.grid4 = []

        for row in range(self.AMOUNT):
            self.grid.append([])
            self.grid2.append([])
            self.grid3.append([])
            self.grid4.append([])

            for column in range(self.AMOUNT):
                self.grid[row].append(0) 
                self.grid2[row].append(0)
                self.grid3[row].append(0)
                self.grid4[row].append(0)
                
        self.WINDOW_SIZE = [self.WINDOW_X, self.WINDOW_Y + 20]
        

    def make_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Array Backed Grid")
        self.clock = pygame.time.Clock()
        self.done = False

    def game_logic(self):    
        hitRequest = ""         # hit request for player1
        hitRequest2 = ""        # hit request for player2
        #for loop  records the mouse clicks
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                self.done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // ( self.square_size + self.margin)
                row = pos[1] // (self.square_size + self.margin)
                # Set that location to one check location 
                # this wil also have a check so there is no switching

                # this sees where the hit is either left or right, bottom or top 
                # this is where either hits are rjected or not


                # next lines check what grid was clicked. Amount is the length in row and column direction 
            
                # top grids
                if column < AMOUNT and row < AMOUNT and PLAYER1.isTurn:    #left 
                    hitRequest = self.makeRequestMssg(row, column)
                    print(hitRequest)
                    PLAYER1.changeTurn()
                
                elif column > AMOUNT and row < AMOUNT:  #right
                    column = column - AMOUNT  - XOff
                    #checks the column is in range
                    if column < AMOUNT and column >= 0:
                        self.grid2[row][column] = 1 
                
                #bottom grids 
                elif column < AMOUNT and row > AMOUNT and PLAYER2.isTurn:          # left
                    row = row - AMOUNT - YOff                   # taking acount offset created by space between grids and -Amount so it is in graph bounds
                    if row < AMOUNT and row >= 0:               # sanity check and chking if clicked area was a border not an actual grid
                        hitRequest2 = self.makeRequestMssg(row, column)
                        PLAYER2.changeTurn()

                elif column > AMOUNT and row > AMOUNT:          # right
                    row = row - AMOUNT - YOff
                    column = column - AMOUNT - XOff             
                    if row < AMOUNT and row >= 0 and column < AMOUNT and column >= 0:
                        self.grid4[row][column] = 1
      
        # Set the screen background
        self.screen.fill(WHITE)

        # Draw the grid no mouse action monitoring here
        for row in range(self.AMOUNT):
            for column in range(self.AMOUNT):
                #top grids are made
                color = self.color_single_grid(self.grid, row, column)  #left top
                self.draw_grid_1st(row, column, 0,color)                #

                color2 = self.color_2nd(self.grid2, row, column)    #right top
                self.draw_2nd(row, column, 0, color2)
                #bottom grids are built
                color = self.color_single_grid(self.grid3, row, column) #left bottom 
                self.draw_grid_1st(row, column, YOff,color)                #left bottom
                
                color2 = self.color_2nd(self.grid4, row, column)        #right bottom
                self.draw_2nd(row, column, YOff, color2)                #right bottom
        # Limit to 60 frames per second
        self.clock.tick(60)
        pygame.display.flip()
        return hitRequest, hitRequest2      #tupple of request

    def end(self):
        pygame.quit()
    #reads the message passed through the socket(that will be passed)
    def readMessege(self, request, isTop):
        split = request.split(' ')
        is_hit_message = False
        if split[0] == "HIT":
            cord = (split[1])[1:-1].split(",")
            x = int(cord[0])
            y = int(cord[1])
            if isTop:
                self.grid4[x][y] = 2
                self.grid[x][y] = 1
                PLAYER2.changeTurn()
            else:
                self.grid2[x][y] = 2
                self.grid3[x][y] = 1
                PLAYER1.changeTurn()


            print("here")
    
    #request sent to server
    def makeRequestMssg(self, row, column):
        return "HIT [" + str(row) + "," + str(column) + "] GM1\r\nEND"

    # draws the left grid (the one clicked on)
    def color_single_grid(self, Grid, row, column):
        color = BLUE
        if Grid[row][column] == 1:
            color = RED
        return color
    
    # left side color in
    def draw_grid_1st(self, row, column, positionY, color):
        pygame.draw.rect(self.screen,
            color,
            [(MARGIN + self.square_size) * column + MARGIN,
            (MARGIN + self.square_size) * row + MARGIN + ((MARGIN + self.square_size) * positionY) * (AMOUNT * positionY + 1),
            self.square_size,
            self.square_size])

    #draws the one that shows hits right side
    def color_2nd(self, Grid, row, column):
        color = BLUE
        if Grid[row][column] == 1:
            color = BLACK
        elif Grid[row][column] == 2:
            color = RED
        return color

    # right side color in 
    def draw_2nd(self, row, column, positionY, color2):
        pygame.draw.rect(self.screen,
        color2,
        [((MARGIN + self.square_size) * column + MARGIN ) + (MARGIN + self.square_size)* (AMOUNT * XOff + 1),
        (MARGIN + self.square_size) * row + MARGIN + ((MARGIN + self.square_size) * positionY) * (AMOUNT * positionY + 1),
        self.square_size,
        self.square_size]) 
    
     


            
        


 
            # Go ahead and update the screen with what we've drawn.
        
    # Be IDLE friendly. If you forget t
    # his line, the program will 'hang'
    # on exit.

def main_LOOP(p1):
    while not p1.done:
        if not p1.done:
            hitMessage = p1.game_logic()
            
            if hitMessage[0] is not "":
                #send p1.message across
                p1.readMessege(hitMessage[0], True)
                #send p1.response
            if hitMessage[1] is not "":
                #send p1.message across
                p1.readMessege(hitMessage[1], False)
                #send p1.response

        

XOff = 1 #amount of tiles apart are the left and right grids 
YOff = 1 #amount of tiles apart are the top and bottom grids

BLUE = (135,206,250)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WINDOW_X= 400
WINDOW_Y= 400 
square_size = 14
MARGIN = 1
AMOUNT = WINDOW_Y//(square_size + MARGIN)
WINDOW_X = WINDOW_Y * 2 + 50

PLAYER1 = player.Player(1, 1, True)
PLAYER2 = player.Player(1, 2, False)

p1 = BoardGame(WINDOW_X, WINDOW_Y *2, square_size, MARGIN, AMOUNT)
p1.make_grid(1,1)
p1.make_window()

main_LOOP(p1)
pygame.quit()