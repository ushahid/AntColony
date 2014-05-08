import logging
import sys
from optparse import OptionParser
from logutils import initLogging,getLogger
from collector import CollectorAnt
from scout import ScoutAnt
from battalion import Battalion


class Colony:
    def __init__(self, ants):
        self.collectors = []
        self.scouts = []
        self.battalions = []
        self.collectorsUpperLimit = 5
        self.collectorsLowerLimit = 2
        self.battalionSize = 3
        self.scoutsUpperLimit = 7
        self.scoutsLowerLimit = 3
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

        #Check in battalion
        for battalion in self.battalions:
            for soldier in battalion.soldiers:
                if soldier.getPosition() == ant:
                    return True

        return False


    def newRecruits(self, ants):
        recruits = []
        for ant in ants.my_ants():
            if not self.isRegistered(ant):
                getLogger().debug("Found an ant: " + str(ant))
                self.collectors.append(CollectorAnt(ant))


    def checkBattalion(self):
        getLogger().debug("Checking Battalions")
        pass



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


    def moveBattalions(self, ants):
        getLogger().debug("Moving battalions: " + str(len(self.battalions)))

        toRemove = []

        #Get moves from battalions
        for battalion in self.battalions:
            alive = battalion.updateTarget(ants)
            if alive:
                getLogger().debug("Moving battalion: " + str(battalion.target))
                target = battalion.target
                for soldier in battalion.soldiers:
                    direction = soldier.suggestMove(ants, target)
                    getLogger().debug("Moving soldier: " + str(soldier.getPosition()) + " to " + direction)
                    soldier.executeMove(ants, direction, self)
            else:
                toRemove.append(battalion)

        for battalion in toRemove:
            self.battalions.remove(battalion)


    def setOccupied(self):
        self.occupied = {}

        #Add collectors
        for collector in self.collectors:
            self.occupied[collector.getPosition()] = True

        #Add scouts
        for scout in self.scouts:
            self.occupied[scout.getPosition()] = True

        #Add battalions
        for battalion in self.battalions:
            for soldier in battalion.soldiers:
                self.occupied[soldier.getPosition()] = True




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

        #check battalions
        for battalion in self.battalions:
            for soldier in battalion.soldiers:
                if not(soldier.getPosition() in ants):
                    battalion.soldiers.remove(soldier)


    def checkBattalions(self):
        soldierCount = len(self.collectors) - self.collectorsUpperLimit
        if soldierCount >= self.battalionSize:
            #getLogger().debug("Collectors: " + str(self.collectors))
            soldiers = []
            for i in range(1, soldierCount + 1):
                soldiers.append(self.collectors[-i].getPosition())
            #getLogger().debug("Soldiers: " + str(soldiers))
            self.createBattalions(soldiers)
            self.collectors = self.collectors[0:-soldierCount]
            #getLogger().debug("Collectors left: " + str(self.collectors))

        soldierCount = len(self.scouts) - self.scoutsUpperLimit
        if soldierCount >= self.battalionSize:
            #getLogger().debug("Scouts: " + str(self.scouts))
            soldiers = []
            for i in range(1, soldierCount + 1):
                soldiers.append(self.scouts[-i].getPosition())
            #getLogger().debug("Soldiers: " + str(soldiers))
            self.createBattalions(soldiers)
            self.scouts = self.scouts[0:-soldierCount]
            #getLogger().debug("Scouts left: " + str(self.scouts))


    def createBattalions(self, soldiers):
        getLogger().debug("Creating battalion: " + str(soldiers))
        soldiersCount = len(soldiers)
        while soldiersCount > self.battalionSize:
            self.battalions.append(Battalion(soldiers[0:self.battalionSize - 1]))
            soldiers = soldiers[self.battalionSize]
            soldiersCount -= self.battalionSize



    def move(self, ants):
        self.deleteDead(ants)
        self.newRecruits(ants)

        getLogger().debug("Moving colony")
        self.setOccupied()
        getLogger().debug(str(self.occupied))

        #March forward
        self.moveCollectors(ants)
        self.moveScouts(ants)
        self.moveBattalions(ants)
        self.checkBattalion()
