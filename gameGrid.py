import pygame
# will chang
# Define colors


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
        hitRequest = ""
        hitRequest2 = ""
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

                # this sees where the hit is either left or right, only suports up 
                # todo tomorrow 
                if column < AMOUNT and row < AMOUNT:
                    hitRequest = "HIT [" + str(row) + "," + str(column) + "] GM1\r\nEND"
                    print(hitRequest)
                elif column > AMOUNT and row < AMOUNT:
                    self.grid2[row][column - AMOUNT  - XOff] = 1 #have not figure out whta changes the 2 constant
                elif column < AMOUNT and row > AMOUNT:
                    hitRequest2 = "HIT [" + str(row) + "," + str(column) + "] GM1\r\nEND"
                elif column > AMOUNT and row > AMOUNT:
                    self.grid4[row - AMOUNT - YOff][column - AMOUNT - XOff] = 1

                
        # Set the screen background
        self.screen.fill(WHITE)

        # Draw the grid
        for row in range(self.AMOUNT):
            for column in range(self.AMOUNT):

                color = self.color_single_grid(self.grid, row, column)
                self.draw_grid_1st(row, column, 0,color)
                color2 = self.color_2nd(self.grid2, row, column)
                self.draw_2nd(row, column, 0, color2)
                #bottom grids are built
                color = self.color_single_grid(self.grid3, row, column) #left bottom 
                self.draw_grid_1st(row, column, YOff,color)                #left bottom
                
                color2 = self.color_2nd(self.grid4, row, column)        #right bottom
                self.draw_2nd(row, column, YOff, color2)                #right bottom
        # Limit to 60 frames per second
        self.clock.tick(60)
        pygame.display.flip()
        return hitRequest, hitRequest2

    def end(self):
        pygame.quit()
    
    def readMessege(self, request):
        split = request.split(' ')
        is_hit_message = False
        if split[0] == "HIT":
            cord = (split[1])[1:-1].split(",")
            x = int(cord[0])
            y = int(cord[1])
            self.grid2[x][y] = 2
            self.grid[x][y] = 1
            print("here")
    
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
            
            if hitMessage[0] is "":
                continue

            #send p1.message across
            p1.readMessege(hitMessage[0])
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

p1 = BoardGame(WINDOW_X, WINDOW_Y *2, square_size, MARGIN, AMOUNT)
p1.make_grid(1,1)
p1.make_window()

main_LOOP(p1)
pygame.quit()