import battleship


class Player:

    # player is initialiezed by the server
    def __init__(self, playerID):
        self.gameID = "0-0"
        # users game id recieved from server
        self.playerID = playerID
        # users own player ID
        self.isTurn = False
        # who will go
        self.BoatDict = {}
        # ships in a dict easy acces
        self.firstTurn = False
        # who goes first
        self.buildTime = True
        self.boatBuildingNum = 2
        self.chosenBuild = []
        self.maxBoatSize = 7
        self.tickerStart = 0
        self.win = False

    def make_grid(self, AMOUNT):
        self.AMOUNT = AMOUNT
        self.grid = []
        self.grid2 = []
        
        for row in range(self.AMOUNT):
            self.grid.append([])
            self.grid2.append([])
            for column in range(self.AMOUNT):
                self.grid[row].append(0)
                self.grid2[row].append(0)     

    # changes turn once done
    def changeTurn(self):
        self.isTurn = not self.isTurn

    def startGussing(self):
        self.tickerStart += 1
        if self.tickerStart == 2:
            self.isTurn = self.firstTurn
        # game can only start if called twice
        # one from being ready and one for the opponent being readdy

    def creatingBoat(self, row, column):
        if(len(self.chosenBuild) == 0):
            if self.grid2[row][column] != 0:
                return
            self.chosenBuild.append((row, column))
            self.grid2[row][column] = 1
        else:
            if not self.checkInput(row, column):
                self.grid2[self.chosenBuild[0][0]][self.chosenBuild[0][1]] = 0
            self.chosenBuild.clear()
        if self.maxBoatSize <= self.boatBuildingNum:
            self.buildTime = not self.buildTime

    def checkInput(self, row, column):
        locationList = []
        isblank = False
        firstsq = self.chosenBuild[0]
        # where the firt click was set
        newRow = firstsq[0]
        # newRow will be the last row block
        newCol = firstsq[1]
        locationList.append((firstsq[0], firstsq[1]))
        # where the last column will be 
        direction = 1
        # what direction with the blocks go relative to first block
        # bottom if statment checks if the second click create a vertical boat 
        if row != firstsq[0] and column == firstsq[1]:
            if row - firstsq[0] < 1:        # changes direction if new click is above
                direction = -1
            maxRow = firstsq[0] + (self.boatBuildingNum * direction)    #location of furthest block
            
            if maxRow > self.AMOUNT or maxRow < -1:         #check if in bound of grid
                return False
            
            newRow = firstsq[0] + direction
            isblank =  (self.grid2[newRow][column] == 0)         
            # finally add to grid
            while True:
                # if the grid squeare is 0 then no ship 
                if isblank:
                    self.grid2[newRow][column] = 1
                    locationList.append((newRow, column))
                    newRow += direction
                    if newRow == maxRow:                        # end while loop if reached end
                        break
                    isblank = (self.grid2[newRow][column] == 0) # check incoming square
                else:
                    if newRow == firstsq[0]:
                        break
                    newRow -= direction
                    self.grid2[newRow][column] = 0

           
        # second click creates a horizontal boat  
        elif row == firstsq[0] and column != firstsq[1]:
            # changes direction if second click is to the left
            if column - firstsq[1]  < 1:
                direction = -1

            # furthes block loaction
            maxCol = firstsq[1] + (self.boatBuildingNum * direction)
            if maxCol > self.AMOUNT or maxCol < -1:     #check if out of bound
                return False
            newCol = firstsq[1] + direction
            isblank = (self.grid2[row][newCol] == 0)
            # finally add t grid
            while True:
                if isblank:
                    self.grid2[row][newCol] = 1
                    locationList.append((row, newCol))
                    newCol += direction
                    if newCol == maxCol:
                        break
                    isblank = (self.grid2[row][newCol] == 0)
                else:
                    if newCol == firstsq[1]:
                        break
                    newCol -= direction
                    self.grid2[row][newCol] = 0
                
        if not isblank:
            return False
        #send out to bee added to dict and initialized
        if direction == -1:
            self.addBoat((firstsq[0], firstsq[1]), ( newRow, newCol), locationList) 
        else:
            self.addBoat((newRow, newCol), (firstsq[0], firstsq[1]), locationList)  
        return True

    #adds boat by first checking size then adding to to dict
    def addBoat(self, start, end, locationList):
        size = start[0] - end[0]
        #row offset how long
        if size == 0:
            size = start[1] - end[1]
            #column offset how tall
        self.BoatDict[size] = battleship.Battleship(size, start, end, locationList)
        self.boatBuildingNum += 1


    # colision check
    def hitsBoats(self, row, column):
        
        for boat in self.BoatDict.keys():
            i = -1
            for square in self.BoatDict[boat].locations:
                i += 1
                if row == square[0] and column == square[1]:
                    if self.BoatDict[boat].hit(i) and self.BoatDict[boat].isSunk():
                        self.BoatDict.pop(boat)

                    return True
        
        return False
            
