#!/usr/bin/env python
import logging
import sys
from optparse import OptionParser
from logutils import initLogging,getLogger
from colony import Colony
from ants import *



turn_number = 1
bot_version = 'v0.1'
initLogging()

class LogFilter(logging.Filter):
  """
  This is a filter that injects stuff like TurnNumber into the log
  """
  def filter(self,record):
    global turn_number,bot_version
    record.turn_number = turn_number
    record.version = bot_version
    return True

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    def __init__(self):
        """Add our log filter so that botversion and turn number are output correctly"""        
        log_filter  = LogFilter()
        getLogger().addFilter(log_filter)
    
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        self.initialized = False
    
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):
        global turn_number
        if not self.initialized:
            self.colony = Colony(ants)
            self.initialized = True
        else:
            self.colony.move(ants)
        turn_number = turn_number + 1
        
        """    
        i =0
        for ant_loc in ants.my_ants():
            # try all directions in given order

            i=i+1
            directions = ('n','e','s','w')
            for direction in directions:
                # the destination method will wrap around the map properly
                # and give us a new (row, col) tuple
                new_loc = ants.destination(ant_loc, direction)
                # passable returns true if the location is land
                if (ants.passable(new_loc)):
                    # an order is the location of a current ant and a direction
                    ants.issue_order((ant_loc, direction))
                    # stop now, don't give 1 ant multiple orders
                    break
            # check if we still have time left to calculate more orders
            if ants.time_remaining() < 10:
                break
           """
           
if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
