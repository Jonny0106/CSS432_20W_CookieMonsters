import battleship

class Player:
    
    #player is initialiezed by the server
    def __init__(self, gameID, playerID, firstTurn):
        self.gameID = gameID
        # users game id recieved from server
        self.playerID = playerID
        # users own player ID
        self.isTurn = firstTurn
        #who will go first
        self.BoatDict = {}

    #adds boat by first checking size
    def addBoat(self, start, end):
        rowOff = start[0] - end[0]
        #row offset how long
        columnOff = start[1] - end[1]
        #column offset how tall
        if rowOff == 0:         #can only be one either tall or long
            return self.addBoatToDict(columnOff, start, end)
        elif columnOff == 0:
            return self.addBoatToDict(rowOff)
        return False
    
    # add boat to dictionary
    def addBoatToDict(self, size, start, end):
        if size in self.BoatDict:
            return False
        self.BoatDict[size] = battleship.Battleship(size,start, end)
        return True

    #changes turn once done
    def changeTurn(self):
        self.isTurn = not self.isTurn

