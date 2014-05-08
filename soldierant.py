import logging
import sys
from optparse import OptionParser
from logutils import initLogging,getLogger
from ant import Ant
from ants import FOOD

class SoldierAnt(Ant):
    def __init__(self, position):
        Ant.__init__(self, position)

    def suggestMove(self, ants, target):
        if target is None:
            return '#'
        
        direction = ants.get_direction(self.getPosition(), target)
        return direction[0]