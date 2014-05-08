import logging
import sys
from optparse import OptionParser
from logutils import initLogging,getLogger
from ant import Ant
from soldierant import SoldierAnt

class Battalion:
    def __init__(self, s):
        self.target = None
        self.soldiers = []
        for sldr in s:
            self.soldiers.append(SoldierAnt(sldr))

    def updateTarget(self, ants):
        if len(self.soldiers) == 0:
            return False
        self.target = ants.get_nearest_target(self.soldiers[0].getPosition())

        if self.target is None:
            self.target = self.soldiers[0]

        return True

    def getSize(self):
        return len(self.soldiers)


    def addSoldier(self, soldier):
        self.soldiers.append(soldier)


    def disperse(self, type):
        units = []
        if type == "scouts":
            for soldier in soldiers:
                units.append(ScoutAnt(soldier.getPosition()))

        elif type == "collectors":
            for soldier in soldiers:
                units.append(CollectorAnt(soldier.getPosition()))

        return units

    def battalionStrength(self, ants):
        totalDistance = 1
        for soldier in self.soldiers:
            soldierDistance = 0
            for isoldier in self.soldiers:
                soldierDistance = soldierDistance + ants.distance(soldier.getPosition(), isoldier.getPosition())
            totalDistance = totalDistance + soldierDistance
        return 1/totalDistance

