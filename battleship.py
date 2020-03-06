import pygame


# game initializes a number of Battleships with a determined size and a player-chosen start and end position
class Battleship:
    def __init__(self, size, start, end, locations):
        self.locations = locations
        # size of battleship
        self.size = size
        # array to keep track of hit/not hit
        self.status = [size]
        # start and end position on grid
        self.start = start
        self.end = end

    def hit(self, slot):
        # check if slot has not been hit yet, set to hit
        if self.status[slot] is False:
            self.status[slot] = True
            return self.status[slot]
        # slot has been hit, return false
        else:
            return False
            

    def isSunk(self):
        # iterate through status, check for slot that has not been hit
        for slot in self.status:
            if slot is False:
                # return false if one slot has not been hit yet
                return False
        # otherwise all slots are hit, return true
        return True
