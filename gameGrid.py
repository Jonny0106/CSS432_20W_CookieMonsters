import pygame
import battleship
import player
import enum

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
        hitRequest2 = ""  # hit request for player2
        # for loop  records the mouse clicks
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                self.done = True  # Flag that we are done so we exit this loop 
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


                # bottom grids
                elif column < AMOUNT and row > AMOUNT and PLAYER2.isTurn:  # left
                    row = row - AMOUNT - YOff  # taking acount offset created by space between grids and -Amount so it is in graph bounds
                    if row < AMOUNT and row >= 0 and PLAYER2.grid[row][column] == 0:  # sanity check and chking if clicked area was a border not an actual grid
                        hitRequest2 = self.makeRequestMssg(row, column)
                        PLAYER2.changeTurn()

                elif column > AMOUNT and row > AMOUNT and PLAYER2.buildTime:  # right
                    row = row - AMOUNT - YOff
                    column = column - AMOUNT - XOff
                    if row < AMOUNT and row >= 0 and column < AMOUNT and column >= 0:
                        PLAYER2.creatingBoat(row, column)
                        if not PLAYER2.buildTime:
                            self.sendStartGame2()
        return hitRequest, hitRequest2  # tupple of request
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
                # bottom grids are built
                color = self.color_single_grid(PLAYER2.grid, row, column)  # left bottom
                self.draw_grid_1st(row, column, YOff, color)  # left bottom

                color2 = self.color_2nd(PLAYER2.grid2, row, column)  # right bottom
                self.draw_2nd(row, column, YOff, color2)  # right bottom
        # Limit to 60 frames per second
        self.clock.tick(60)
        pygame.display.flip()

    #reads the message passed through the socket(that will be passed)
    # at this moment no socket so all done localy
    def readMessege(self, request, isTop):
        sendMessage = ""
        split = request.split(' ')
        is_hit_message = False
        if split[0] == "GUESS":
            cord = (split[1])[1:-1].split(",")
            row = int(cord[0])
            column = int(cord[1])
            if isTop:
                if PLAYER2.hitsBoats(row, column):
                    PLAYER2.grid2[row][column] = 3
                    if len(PLAYER2.BoatDict) == 0:
                        sendMessage = "END [" + str(1) + "," + str(0) + "] GM1\r\nEND"
                    else:
                        sendMessage = "HIT [" + str(row) + "," + str(column) + "] "+ str(PLAYER2.gameID) + "\r\nEND"
                else:
                    PLAYER2.grid2[row][column] = 2
                    sendMessage = "MISS [" + str(row) + "," + str(column) + "] GM1\r\nEND"
                PLAYER2.changeTurn()      
            else:
                if PLAYER1.hitsBoats(row, column):
                    PLAYER1.grid2[row][column] = 3
                    if len(PLAYER1.BoatDict) == 0:
                        sendMessage = "END [" + str(1) + "," + str(0) + "] GM1\r\nEND"
                    else:
                        sendMessage = "HIT [" + str(row) + "," + str(column) + "] GM1\r\nEND"
                else:
                    PLAYER1.grid2[row][column] = 2
                    sendMessage = "MISS [" + str(row) + "," + str(column) + "] GM1\r\nEND"
                PLAYER1.changeTurn()
        return sendMessage

    # reads response message and updates board    
    def readRespMessege(self, response, isTop):
        split = response.split(' ')
        is_hit_message = False
        cord = (split[1])[1:-1].split(",")
        row = int(cord[0])
        column = int(cord[1])
        if isTop:
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
        else:
            if split[0] == "HIT":
                PLAYER2.grid[row][column] = 2
            elif split[0] == "MISS":
                PLAYER2.grid[row][column] = 1
            elif split[0] == "END":
                if row == 1:
                    PLAYER2.win = True
                    PLAYER2.grid = [[2 for i in range(self.AMOUNT)] for j in range(self.AMOUNT)]
                    # when end the screen turns red 
                self.done = True
                
    
    # request sent to server
    def makeRequestMssg(self, row, column):
        return "GUESS [" + str(row) + "," + str(column) + "] GM1\r\nEND"

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


    def sendStartGame(self):
        PLAYER1.startGussing()
        PLAYER2.startGussing()

    def sendStartGame2(self):
        PLAYER1.startGussing()
        PLAYER2.startGussing()


def main_LOOP(p1):
    timeOut = 0
    while not p1.done and timeOut < 2:
        if not p1.done:
            hitMessage = p1.game_Event()
            if hitMessage[0] is not "":

                # send p1.message across
                response = p1.readMessege(hitMessage[0], True)
                # send p1.response
                p1.readRespMessege(response, True)
            elif hitMessage[1] is not "":
                # send p1.message across
                response = p1.readMessege(hitMessage[1], False)
                p1.readRespMessege(response, False)
                # send p1.response
        else:
            timeOut += 1
        p1.game_Coloring()

#enumeration of message types
class Mess_Type(enum.Enum):
    GUESS = 0
    HIT = 1
    MISS = 2
    END = 3
    START = 4
    STARTGUESS = 5



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
    PLAYER1 = player.Player(1)
    PLAYER1.gameID = 1
    PLAYER1.firstTurn = True

    PLAYER2 = player.Player(2)
    PLAYER2.gameID = 2
    PLAYER2.firstTurn = False

    PLAYER1.make_grid(AMOUNT)  # creates grid for player1(top)
    PLAYER2.make_grid(AMOUNT)  # creates grid for player2(bottom)

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
        print("OK have it your way. Bye...")
        break