import pygame
import battleship
import player
import enum
import client

# each player gets a board
class BoardGame:
    # constructor
    def __init__(self, WINDOW_X, WINDOW_Y, square_size, margin, AMOUNT):
        self.WINDOW_X = WINDOW_X
        self.square_size = square_size
        self.margin = margin
        self.AMOUNT = AMOUNT
        self.WINDOW_Y = WINDOW_Y

    def make_window(self):
        self.WINDOW_SIZE = [self.WINDOW_X, self.WINDOW_Y + 20]
        pygame.init()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Array Backed Grid")
        self.clock = pygame.time.Clock()
        self.done = False

    def game_Event(self):
        hitRequest = ""  # hit request for player1
        # for loop  records the mouse clicks
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                self.endGameBoard()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (self.square_size + self.margin)
                row = pos[1] // (self.square_size + self.margin)
                # Set that location to one check location
                # this wil also have a check so there is no switching

                # this sees where the hit is either left or right, bottom or top
                # this is where either hits are rjected or not

                # next lines check what grid was clicked. Amount is the length in row and column direction

                # top grids
                if column < AMOUNT and row < AMOUNT and PLAYER1.isTurn:  # left
                    if PLAYER1.grid[row][column] == 0:
                        hitRequest = self.makeRequestMssg(row, column)
                        print(hitRequest)
                        PLAYER1.changeTurn()

                elif column > AMOUNT and row < AMOUNT and PLAYER1.buildTime:  # right
                    column = column - AMOUNT - XOff
                    # checks the column is in range
                    if column < AMOUNT and column >= 0:
                        PLAYER1.creatingBoat(row, column)
                        if not PLAYER1.buildTime:
                            self.sendStartGame()
        return hitRequest
    
    def game_Coloring(self):
        # Set the screen background
        self.screen.fill(WHITE)

        # Draw the grid no mouse action monitoring here
        for row in range(self.AMOUNT):
            for column in range(self.AMOUNT):
                # top grids are made
                color = self.color_single_grid(PLAYER1.grid, row, column)  # left top
                self.draw_grid_1st(row, column, 0, color)  #

                color2 = self.color_2nd(PLAYER1.grid2, row, column)  # right top
                self.draw_2nd(row, column, 0, color2)
            
        # Limit to 60 frames per second
        self.clock.tick(60)
        pygame.display.flip()

    #reads the message passed through the socket(that will be passed)
    # at this moment no socket so all done localy
    def sendMessege(self, request):
        sendMessage = ""
        response = socClient.sendGuess(request)
        return sendMessage

    # reads response message and updates board    
    def readRespMessege(self, response): 
        print("response") 
        split = response.split(' ')
        is_hit_message = False
        cord = (split[1])[1:-1].split(",")
        row = int(cord[0])
        column = int(cord[1])
        socClient.sendHit((row, column), 1)
        
        if split[0] == "HIT":
            PLAYER1.grid[row][column] = 2
        elif split[0] == "MISS":
            PLAYER1.grid[row][column] = 1
        elif split[0] == "END":
            if row == 1:
                PLAYER1.win = True
                PLAYER1.grid = [[2 for i in range(self.AMOUNT)] for j in range(self.AMOUNT)] 
                # when end the screen turns red
            self.done = True
                
    
    # request sent to server
    def makeRequestMssg(self, row, column):
        return  str(row) + "," + str(column)

    # draws the left grid (the one clicked on)
    def color_single_grid(self, Grid, row, column):
        color = BLUE
        if Grid[row][column] == 1:
            color = BLACK
        elif Grid[row][column] == 2:
            color = RED
        return color

    # left side color in
    def draw_grid_1st(self, row, column, positionY, color):
        pygame.draw.rect(self.screen,
                         color,
                         [(MARGIN + self.square_size) * column + MARGIN,
                          (MARGIN + self.square_size) * row + MARGIN + ((MARGIN + self.square_size) * positionY) * (
                                      AMOUNT * positionY + 1),
                          self.square_size,
                          self.square_size])

    #draws the one that shows hits right side
    def color_2nd(self, Grid, row, column):
        color = BLUE
        if Grid[row][column] == 1:
            color = BLACK
        elif Grid[row][column] == 2:
            color = WHITE
        elif Grid[row][column] == 3:
            color = RED
        return color

    # right side color in
    def draw_2nd(self, row, column, positionY, color2):
        pygame.draw.rect(self.screen,
                         color2,
                         [((MARGIN + self.square_size) * column + MARGIN) + (MARGIN + self.square_size) * (
                                     AMOUNT * XOff + 1),
                          (MARGIN + self.square_size) * row + MARGIN + ((MARGIN + self.square_size) * positionY) * (
                                      AMOUNT * positionY + 1),
                          self.square_size,
                          self.square_size])

    # this makes makes the game go from setting up to acually guessing
    def sendStartGame(self):
        PLAYER1.startGussing()                      # player is ready
        ready = self.createReadyMssg()              # creates ready message
        response = socClient.sendMessage(ready)     # sends ready messege to other player
        self.readRespMessege(response)              # make sure it is a ready/ could be an end message
                                     
    def endGameBoard(self):
        endMssg = self.makeEndMssg()                # create end messege
        while not self.done:                            # makes sure that server is on track with exit
            response = socClient.sendMessage(endMssg)   # send endmessage
            self.readRespMessege(response)              # make sure it is a ready/ could be an end message
            # self.done = True    will be called in readMessege      # Flag that we are done so we exit this loop 
        
def main_LOOP(p1):
    timeOut = 0
    while not p1.done and timeOut < 2:
        if not p1.done:
            hitMessage = p1.game_Event()
            if hitMessage is not "":
                response = p1.sendMessege(hitMessage) # send p1.message across
                p1.readRespMessege(response)          # send p1.response
        else:
            timeOut += 1
        p1.game_Coloring()

#enumeration of message types
class Mess_Type(enum.Enum):
    GUESS = 0
    HIT = 1
    MISS = 2
    END = 3
    READY = 4

XOff = 1  # amount of tiles apart are the left and right grids
YOff = 1  # amount of tiles apart are the top and bottom grids

BLUE = (135, 206, 250)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WINDOW_X = 400
WINDOW_Y = 400
square_size = 14
MARGIN = 1
AMOUNT = WINDOW_Y // (square_size + MARGIN)
WINDOW_X = WINDOW_Y * 2 + 50

while True:
    socClient = client.Client()
    PLAYER1 = player.Player(1)
    PLAYER1.gameID = 1
    PLAYER1.firstTurn = True

    

    PLAYER1.make_grid(AMOUNT)  # creates grid for player1(top)
    
    p1 = BoardGame(WINDOW_X, WINDOW_Y * 2, square_size, MARGIN, AMOUNT)
    p1.make_window()

    main_LOOP(p1)
    pygame.quit()
    # only player1's staus is brodcasted
    if PLAYER1.win == True:
        print("you won!")
    else:
        print("you lost")

    # do thy want to play again
    x = input("Want to play again:(y/n)")
    if x.capitalize() != "Y":
        print("Byyyeeeee")
        socClient.end()
        break