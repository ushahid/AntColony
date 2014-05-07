import logging
import sys
from optparse import OptionParser
from logutils import initLogging,getLogger
from collector import CollectorAnt


class Colony:
    def __init__(self, ants):
        self.collectors = []
        self.scouts = []
        self.occupied = {}
        self.newRecruits(ants)

    def isRegistered(self, ant):
        #Check in collectors
        for collector in self.collectors:
            if collector.getPosition() == ant:
                return True

        return False


    def newRecruits(self, ants):
        recruits = []
        for ant in ants.my_ants():
            if not self.isRegistered(ant):
                getLogger().debug("Found an ant: " + str(ant))
                self.collectors.append(CollectorAnt(ant))


    def moveCollectors(self, ants):
        getLogger().debug("Moving collectors: " + str(len(self.collectors)))
        #Get moves from collectors
        for i in range (0, len(self.collectors)):
            direction = self.collectors[i].suggestMove(ants, self)
            getLogger().debug("Moving collector: " + str(self.collectors[i].getPosition()) + " to " + direction)
            self.collectors[i].executeMove(ants, direction, self)


    def setOccupied(self):
        self.occupied = {}

        #Add collectors
        for collector in self.collectors:
            self.occupied[collector.getPosition()] = True


    def deleteDead(self, ants):
        ants = ants.my_ants()
        
        #check collectors
        for collector in self.collectors:
            if not(collector.getPosition() in ants):
                self.collectors.remove(collector)


    def move(self, ants):
        self.deleteDead(ants)
        self.newRecruits(ants)
        getLogger().debug("Moving colony")
        self.setOccupied()
        getLogger().debug(str(self.occupied))
        self.moveCollectors(ants)

