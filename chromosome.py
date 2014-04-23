from ants import *
from random import randint
class Chromosome():
	def __init__(self):
		
		self.genes=[]



	def create(self,ants):
	 	size = len(ants.my_ants())
	 	directions = ['n','s','e','w']
	 	
	 	for i in range (0,size):
	 		
	 		self.genes.append(directions[randint (0,3)])











	

