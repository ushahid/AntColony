import logging
import sys
from optparse import OptionParser
from logutils import initLogging,getLogger

class Ant:
    def __init__(self, position):
        self.position = position
        self.noob = True
        
    def getPosition(self):
        return self.position

    def isOccupied(self, pos, occupied):
        return occupied.get(pos, False)

    def executeMove(self, ants, direction, colony):
        if direction != '#':
            newPos = ants.destination(self.position, direction)
            if (not self.isOccupied(newPos, colony.occupied)) and ants.passable(newPos):
                ants.issue_order((self.position, direction))
                colony.occupied[newPos] = True
                self.position = newPos
                return True
            elif ants.passable(newPos):
                getLogger().debug("Moved randomly: " +  str(newPos) + " is occupied.")
                directions = ['n', 's','e', 'w']
                for direction in directions:
                    newPos = ants.destination(self.position, direction)
                    if (not self.isOccupied(newPos, colony.occupied)) and ants.passable(newPos):
                        ants.issue_order((self.position, direction))
                        colony.occupied[newPos] = True
                        self.position = newPos
                        return True
        elif self.noob:
            directions = ['n', 's','e', 'w']
            for direction in directions:
                newPos = ants.destination(self.position, direction)
                if (not self.isOccupied(newPos, colony.occupied)) and ants.passable(newPos):
                    ants.issue_order((self.position, direction))
                    colony.occupied[newPos] = True
                    self.position = newPos
                    return True
            self.noob = False
        else:

            getLogger().debug("Failed to execute move: Direction is #")

        return False

