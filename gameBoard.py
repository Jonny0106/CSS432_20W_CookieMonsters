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
        # font = pygame.font.Font('freesansbold.ttf', 32) 
        # text = font.render('GeeksForGeeks', True, green, blue) 
        # textRect = text.get_rect()  
  
        # set the center of the rectangular object. 
        # textRect.center = (X // 2, Y // 2) 

    def make_window(self):
        self.WINDOW_SIZE = [self.WINDOW_X, self.WINDOW_Y + 20]
        pygame.init()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption(socClient.player_id + " game")
        self.clock = pygame.time.Clock()
        self.done = False
        self.textChange("Set your ships")

    def textChange(self, textStr):
        self.dispayText = textStr
        self.font = pygame.font.Font(pygame.font.get_default_font(), 20)
        self.text = self.font.render(self.dispayText, True, BLACK, BLUE)
        self.textRect = self.text.get_rect()
        self.textRect.left = TEXT_X
        self.textRect.top = TEXT_Y


    def game_Event(self, updates=False):
        guessRequest = ""  # guess request for player1
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
                # this is where either hits are rejected or not

                # next lines check what grid was clicked. Amount is the length in row and column direction

                # top grids
                if column < AMOUNT and row < AMOUNT and PLAYER1.isTurn and not updates:  # left
                    if PLAYER1.grid[row][column] == 0:
                        guessRequest = self.createGuessMsg(row, column)
                        PLAYER1.changeTurn()
                        self.textChange("Waiting on opponent")

                elif column > AMOUNT and row < AMOUNT and PLAYER1.buildTime and not updates:  # right
                    column = column - AMOUNT - XOff
                    # checks the column is in range
                    if column < AMOUNT and column >= 0:
                        PLAYER1.creatingBoat(row, column)
                        if not PLAYER1.buildTime:
                            self.sendStartGame()
        return guessRequest

    def game_Coloring(self):
        # Set the screen background
        self.screen.fill(WHITE)
        self.screen.blit(self.text, self.textRect) 
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

    # reads the message passed through the socket (that will be passed)
    # at this moment no socket so all done locally
    def sendMessage(self, request):
        response = socClient.sendMessage(request)
        return response

    # reads response message and updates board
    def readRespMessage(self, response):
        split = response.split(' ')

        if split[0] == "GUESS":
            row = int(split[3])
            column = int(split[4])
            # If hit, create HIT message
            if PLAYER1.hitsBoats(row, column):
                PLAYER1.grid2[row][column] = 3
                if len(PLAYER1.BoatDict) == 0:
                    self.endGameBoard()    
                else:
                    socClient.sendMessageResponse(self.createHitMsg(row, column))
            # Else create MISS message
            else:
                PLAYER1.grid2[row][column] = 2
                socClient.sendMessageResponse(self.createMissMsg(row, column))
        elif split[0] == "HIT":
            row = int(split[3])
            column = int(split[4])
            PLAYER1.grid[row][column] = 2
        elif split[0] == "MISS":
            row = int(split[3])
            column = int(split[4])
            PLAYER1.grid[row][column] = 1
        elif split[0] == "READY":
            PLAYER1.startGuessing()
        elif split[0] == "END":
            if split[1] != socClient.player_id:
                PLAYER1.win = True
                PLAYER1.grid = [[2 for i in range(self.AMOUNT)] for j in range(self.AMOUNT)]
                # when end the screen turns red
            self.done = True

    def createGuessMsg(self, row, column):
        # format: GUESS player_id game_id row, column
        return "GUESS" + " " + str(PLAYER1.playerID) + " " + str(socClient.game_id) + " " + str(row) + " " + str(column)

    def createHitMsg(self, row, column):
        # format: HIT player_id game_id row, column
        return "HIT" + " " + str(PLAYER1.playerID) + " " + str(socClient.game_id) + " " + str(row) + " " + str(column)

    def createMissMsg(self, row, column):
        # format: MISS player_id game_id row, column
        return "MISS" + " " + str(PLAYER1.playerID) + " " + str(socClient.game_id) + " " + str(row) + " " + str(column)

    def createReadyMsg(self):
        # format: READY player_id game_id
        return "READY" + " " + str(PLAYER1.playerID) + " " + str(socClient.game_id)

    def createEndMsg(self, message):
        # format: END player_id game_id message
        return "END" + " " + str(PLAYER1.playerID) + " " + str(socClient.game_id) + " " + message

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
    # draws the one that shows hits right side
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

    # this makes makes the game go from setting up to actually guessing
    def sendStartGame(self):
        self.textChange("waiting on opponent")
        self.game_Coloring()
        self.game_Event(updates=True)
        PLAYER1.startGuessing()  # player is ready
        readyMsg = self.createReadyMsg()  # creates ready message
        response = socClient.sendMessage(readyMsg)  # sends ready message to other player
        self.readRespMessage(response)  # make sure it is a ready/ could be an end message
        if PLAYER1.isTurn:
            self.textChange("your turn")
            self.game_Coloring()
            self.game_Event(updates=True)
    

    def endGameBoard(self):
        endMsg = self.createEndMsg("Loss")  # create end message
        while not self.done:  # makes sure that server is on track with exit
            response = socClient.sendMessage(endMsg)  # send end message
            self.readRespMessage(response)  # make sure it is a ready/ could be an end message
            # self.done = True    will be called in readMessage      # Flag that we are done so we exit this loop


def main_LOOP(p1):
    timeOut = 0
    while not p1.done and timeOut < 2:
        if not p1.done:
            hitMessage = p1.game_Event()
            p1.game_Coloring()
            if hitMessage != "":
                p1.game_Event(updates=True)
                response = p1.sendMessage(hitMessage)  # send p1.message across
                p1.readRespMessage(response)  # send p1.response 
            elif (not PLAYER1.isTurn) and PLAYER1.tickerStart == 2:
                p1.game_Event(updates=True)
                resp = socClient.receiveMessage()
                p1.readRespMessage(resp) 
                PLAYER1.changeTurn()
                p1.textChange("Your turn!")
               
        else:
            timeOut += 1
        p1.game_Coloring()
        


XOff = 1  # amount of tiles apart are the left and right grids
YOff = 1  # amount of tiles apart are the top and bottom grids

BLUE = (135, 206, 250)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WINDOW_X = 350
WINDOW_Y = 350
square_size = 24
MARGIN = 1
AMOUNT = WINDOW_Y // (square_size + MARGIN)
WINDOW_X = WINDOW_Y * 2 + 50
SIZE_OF_UNDER = 100 
TEXT_X = 10
WINDOW_Y = WINDOW_Y + SIZE_OF_UNDER
TEXT_Y = WINDOW_Y - SIZE_OF_UNDER

while True:
    socClient = client.Client()
    PLAYER1 = player.Player(socClient.player_id)
    PLAYER1.gameID = socClient.game_id
    PLAYER1.firstTurn = socClient.goFirst

    PLAYER1.make_grid(AMOUNT)  # creates grid for player1(top)

    p1 = BoardGame(WINDOW_X, WINDOW_Y, square_size, MARGIN, AMOUNT)
    p1.make_window()

    main_LOOP(p1)
    # only player1's status is broadcasted
    if PLAYER1.win == True:
        p1.textChange("you won! check terminal")
    else:
        p1.textChange("you lost, check terminal")
    p1.game_Coloring()
    p1.game_Event(updates=True)
    x = input("Want to play again:(y/n)")
    pygame.quit()
    # do thy want to play again
    if x.capitalize() != "Y":
        print("Byyyeeeee")
        socClient.end()
        break
