import logging
import sys
from optparse import OptionParser
from logutils import initLogging,getLogger
from collector import CollectorAnt
from scout import ScoutAnt


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

        #Check in scouts
        for scout in self.scouts:
            if scout.getPosition() == ant:
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

        toRemove = []

        #Get moves from collectors
        for i in range (0, len(self.collectors)):
            direction = self.collectors[i].suggestMove(ants, self)
            if direction == '#':
                self.scouts.append(ScoutAnt(self.collectors[i].getPosition()))
                toRemove.append(self.collectors[i])
            else:
                getLogger().debug("Moving collector: " + str(self.collectors[i].getPosition()) + " to " + direction)
                self.collectors[i].executeMove(ants, direction, self)

        for i in range(0, len(toRemove)):
            self.collectors.remove(toRemove[i])


    def moveScouts(self, ants):
        getLogger().debug("Moving scouts: " + str(len(self.scouts)))
        toRemove = []

        food = ants.food()
        targetedFood = [self.collectors[i].target for i in range(0, len(self.collectors))]
        foodNotTargeted =  len(food) - len(targetedFood)

        #Get moves from scouts
        for i in range (0, len(self.scouts)):
            direction = self.scouts[i].suggestMove(ants, self)
            if foodNotTargeted > 5:
                self.collectors.append(CollectorAnt(self.scouts[i].getPosition()))
                self.collectors.append
                toRemove.append(self.scouts[i])
                foodNotTargeted = foodNotTargeted - 1
            else:
                getLogger().debug("Moving scout: " + str(self.scouts[i].getPosition()) + " to " + direction)
                self.scouts[i].executeMove(ants, direction, self)

        for i in range(0, len(toRemove)):
            self.scouts.remove(toRemove[i])



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

        #check scouts
        for scout in self.scouts:
            if not(scout.getPosition() in ants):
                self.scouts.remove(scout)


    def move(self, ants):
        self.deleteDead(ants)
        self.newRecruits(ants)
        getLogger().debug("Moving colony")
        self.setOccupied()
        getLogger().debug(str(self.occupied))
        self.moveCollectors(ants)
        self.moveScouts(ants)
