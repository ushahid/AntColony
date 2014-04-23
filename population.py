from chromosome import Chromosome
from ants import *
class Population():
	def __init__(self):
		self.populationSize=12
		self.generationGap=5
		self.chromosomes=[]



	def run(self,ants):

	 	#create chromosome
	 	#//add to list with 0
	 	#//three functions
	 	#//then move best
	 	chromosome = Chromosome()
	 	chromosome.create(ants)
	 	self.chromosomes.append([0,chromosome])
	 	
	 	
	 	#// loop if 0.1 seconds remaining else stop
	 	print (ants.time_remaining())

	 	while ants.time_remaining() >= 200:
	 		self.generateOffsprings(ants)
	 		self.calculateFitness(ants)
	 		self.selectBest(ants)

	 	return self.chromosomes[0]





	def generateOffsprings(self,ants):
	 		#if (len(self.chromosomes[0][1])==1):
	 		#	return
	 		return







	def calculateFitness(self,ants):

	 	return


	def selectBest(self,ants):
	 	#sore according to priority
	 	#selects n best
	 	self.sort()
	 	counter=0
	 	if (self.populationSize>=len(self.chromosomes)):
	 		counter=len(self.chromosomes)
	 	else:
	 		counter=self.populationSize
	 	self.chromosomes = self.chromosomes[:counter]




	def sort(self):
		



		key=0
		i=0
		a1 = self.chromosomes
		for j in range(1,len(a1)):
			key=a1[j];
			i=j-1;
			
			while(a1[i][0]>key[0] and i>=0):
			
				a1[i+1]=a1[i];
				i=i-1;
			
			a1[i+1]=key;
		

















