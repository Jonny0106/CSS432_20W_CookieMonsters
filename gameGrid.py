import pygame
# will chang
# Define colors


#each player gets a board
class BoardGame:
    def __init__(self, WINDOW_X, WINDOW_Y, square_size, margin, AMOUNT):
        self.WINDOW_X = WINDOW_X
        self.square_size = square_size
        self.margin = margin
        self.AMOUNT = AMOUNT
        self.WINDOW_Y = WINDOW_Y
    
    def make_grid(self, x, y):
        self.grid = []
        self.grid2 = []

        for row in range(self.AMOUNT):
            self.grid.append([])
            self.grid2.append([])
            for column in range(self.AMOUNT):
                self.grid[row].append(0) 
                self.grid2[row].append(0)
        self.WINDOW_SIZE = [self.WINDOW_X, self.WINDOW_Y + 20]
        

    def make_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Array Backed Grid")
        self.clock = pygame.time.Clock()
        self.done = False

    def game_logic(self):    
        hitRequest = ""
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
                
                if column < AMOUNT and row < AMOUNT:
                    hitRequest = "HIT [" + str(row) + "," + str(column) + "] GM1\r\nEND"
                    print(hitRequest)
                else:
                    self.grid2[row][column - AMOUNT - 1] = 1
            
                
        # Set the screen background
        self.screen.fill(WHITE)

        # Draw the grid
        for row in range(self.AMOUNT):
            for column in range(self.AMOUNT):
                color = BLUE
                if self.grid[row][column] == 1:
                    color = RED
                pygame.draw.rect(self.screen,
                         color,
                         [(MARGIN + self.square_size) * column + MARGIN,
                          (MARGIN + self.square_size) * row + MARGIN,
                          self.square_size,
                          self.square_size])
                color2 = BLUE
                if self.grid2[row][column] == 1:
                    color2 = BLACK
                elif self.grid2[row][column] == 2:
                    color2 = RED

                pygame.draw.rect(self.screen,
                         color2,
                         [((MARGIN + self.square_size) * column + MARGIN ) + self.WINDOW_X // 2,
                          (MARGIN + self.square_size) * row + MARGIN,
                          self.square_size,
                          self.square_size])
        # Limit to 60 frames per second
        self.clock.tick(60)
        pygame.display.flip()
        return hitRequest

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
            


            
        


 
            # Go ahead and update the screen with what we've drawn.
        
    # Be IDLE friendly. If you forget t
    # his line, the program will 'hang'
    # on exit.

def main_LOOP(p1):
    while not p1.done:
        if not p1.done:
            hitMessage = p1.game_logic()
            if hitMessage is "":
                continue

            #send p1.message across
            p1.readMessege(hitMessage)
            #send p1.response

        


BLUE = (135,206,250)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WINDOW_X= 418
WINDOW_Y= 418
square_size = 20

MARGIN = 2
AMOUNT = WINDOW_Y//(square_size + MARGIN)
WINDOW_X = WINDOW_Y * 2 + 50
p1 = BoardGame(WINDOW_X, WINDOW_Y, square_size, MARGIN, AMOUNT)
p1.make_grid(1,1)
p1.make_window()

main_LOOP(p1)
pygame.quit()