import pygame
# will chang
# Define colors


#each player gets a board
class BoardGame:
    def __init__(self, Window, square_size, margin, AMOUNT):
        self.WINDOW = Window
        self.square_size = square_size
        self.margin = margin
        self.AMOUNT = AMOUNT
    
    def make_grid(self, x, y):
        self.grid = []
        for row in range(self.AMOUNT):
            self.grid.append([])
            for column in range(self.AMOUNT):
                self.grid[row].append(0) 
        self.WINDOW_SIZE = [self.WINDOW, self.WINDOW]

    def make_window(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Array Backed Grid")
        self.clock = pygame.time.Clock()
        self.done = False
        while not self.done:
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    self.done = True  # Flag that we are done so we exit this loop
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // ( self.square_size + self.margin)
                    row = pos[1] // (self.square_size + self.margin)
                    # Set that location to one
                    self.grid[row][column] = 1
                    print("Click ", pos, "Grid coordinates: ", row, column)
            # Set the screen background
            self.screen.fill(BLACK)

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
            # Limit to 60 frames per second
            self.clock.tick(60)
 
            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
        pygame.quit()
    # Be IDLE friendly. If you forget t
    # his line, the program will 'hang'
    # on exit.




BLUE = (135,206,250)
RED = (255, 0, 0)
BLACK = (255, 255, 255)

WINDOW = 500
square_size = 23

MARGIN = 2
AMOUNT = WINDOW//(square_size + MARGIN)
p1 = BoardGame(WINDOW, square_size, MARGIN, AMOUNT)
p1.make_grid(1,1)
p1.make_window()


pygame.quit()