#   Python 3.8.6
#   Bayley King
#   University of Cincinnati MIND Lab
'''
    ** UPDATE THIS **
    
    Child class of GP, the HereBoy algorithm is a form of a genetic algorithm (GA)
      where instead of having a population of individual circuits, one circuit
      in evolved by optimizing a similar fitness function.
    
    In a true HereBoy implementation, a mutation is selected by looking at all 
      possible mutations to the circuit, and performing which one will create the
      highest overall fitness. Although this takes much longer than doing a random
      mutation on a random node, less mutations are usually needed compared
      to a standard GA.

    In this code, we consider that use case where the user would want to evolve a
      piece of code into a variant of itself. 

'''

import math
from levenshteinDistance import levenshtein
import mutations as m
import pickle as pkl
from treePrint import treePrint
#from params import *
import time
import random
from GP import GP
import operations as op


class GA(GP):
    ''' Child class of GP class
    '''
    def __init__(
        self, inputs, 
        max_epochs, 
        pop_size = 1000,
        selection_size = 100
    ):
        super().__init__(inputs,max_epochs)
        # test numpy to see if memory management is better
        self.pop_size = pop_size
        self.selection_size = selection_size
        self.population = [ self.createRandomAST() for x in range(pop_size) ]
        '''
            If these inits are the same as whats needed in the other file,
            inheritance would work very nicely.

            Lets keep everything local to this class, and let the other classes
            be the data handeling classes.
        '''

    def tournamentSelection(
        self, k
    ):
        next_gen = []
        for _ in range(self.selection_size):
            tournament_population = self.population.copy()
            random.shuffle(tournament_population)
            tournament_population = tournament_population[:k]
            fit_check = []
            # checks for best mutated AST from exhaustive add/remove nodes and best mutated node AST
            for circuit in tournament_population:
                fit_check.append(self.checkFitness(circuit))
            max_fit_loc = fit_check.index(max(fit_check))
            next_gen += tournament_population[max_fit_loc]
        self.population = self.fillPopulation(next_gen)

    def fillPopulation(
        self, next_gen
    ):
        for _ in range(self.pop_size - self.selection_size):
            # either mutate member of next_gen or crossover two members of next_gen
            pass
        return None

    def checkFitness(
        self, circuit
    ):
        pass



############# Test Functions  #############



def main():
    pass


if __name__ == "__main__":
    main()
