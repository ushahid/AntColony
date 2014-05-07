import logging
import sys
from optparse import OptionParser
from logutils import initLogging,getLogger
from ant import Ant
from ants import FOOD

class CollectorAnt(Ant):
    def __init__(self, position):
        Ant.__init__(self, position)
        self.path = []
        self.index = 0

    def suggestMove(self, ants, colony):
        if(len(self.path) == 0):
            self.path = ants.get_nearest_food(self.position, colony.collectors)
            self.index = 0

        if(len(self.path) != 0):
            direction = self.path[self.index][1]
            self.index = self.index + 1
            if(self.index == len(self.path)):
                self.path = []
            return direction
        else:
            return '#'


