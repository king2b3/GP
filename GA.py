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
from tabulate import tabulate


class GA(GP):
    ''' Child class of GP class
    '''
    def __init__(
        self, inputs, 
        max_epochs,
        orig_ast, 
        pop_size = 1000,
        selection_size = 100
    ):
        super().__init__(inputs,max_epochs)
        # test numpy to see if memory management is better
        self.orig_logic = self.exhaustiveTest(orig_ast)
        self.pop_size = pop_size
        self.selection_size = selection_size
        self.population = [ self.createRandomAST() for x in range(pop_size) ]
        self.fit_check = []
        self.current_epoch = 0
        '''
            If these inits are the same as whats needed in the other file,
            inheritance would work very nicely.

            Lets keep everything local to this class, and let the other classes
            be the data handeling classes.
        '''

    def tournamentSelection(
        self, k
    ):
        ''' Standard k-tournament selector

            k members of the population are seeded in a tournament, the best 
              individual is selected for the next generation.
            After selection_size individuals have been selected, then the next population
              is generated using the tournament winners
        '''
        next_gen = []
        for _ in range(self.selection_size):
            tournament_population = self.population.copy()
            random.shuffle(tournament_population)
            tournament_population = tournament_population[:k]
            #print('tournament selection ',tabulate(tournament_population))
            fit_check = []
            for circuit in tournament_population:
                fit_check.append(self.checkFitness(circuit))
            max_fit_loc = fit_check.index(max(fit_check))
            next_gen += [tournament_population[max_fit_loc]]
            #print('next gen',tabulate(next_gen))
        self.population = self.fillPopulation(next_gen)

    def fillPopulation(
        self, next_gen
    ):
        ''' Fills the next population from the winners selected in tournamentSelection

            Returns: new_gen -> List
                List of list of strings. The list is thenew poulation of individuals
                  and each individual list is a single individual.
        '''
        new_gen = next_gen.copy()
        while len(new_gen) < self.pop_size:
            mut_type = random.randint(0,1)
            random.shuffle(next_gen)
            if mut_type == 0:
                new_gen += [m.addNode(next_gen[0],self.ins)]
            #elif mut_type == 1:
            else:
                new_gen += [m.removeNode(next_gen[0],self.ins)]
            #else:
            #    new_gen += m.crossover(next_gen[0],next_gen[1],self.ins)
            pass
        return new_gen

    def checkFitness(
        self, circuit
    ):
        ''' Returns the logical fitness of the circuit from exhaustive testing
        '''
        logical_result = self.exhaustiveTest(circuit)
        score = 0
        for t in range(len(logical_result)):
            if logical_result[t] == self.orig_logic[t]:
                score += 1
        return score/len(logical_result)

    def printStats(
        self
    ):
        ''' Prints out the stats of the current generation
        '''
        fit_check = []
        num_circuit = 0
        for circuit in self.population:
            fit_check.append(self.checkFitness(circuit))
            num_circuit += 1
        table = [ [self.current_epoch, min(fit_check), sum(fit_check)/len(fit_check), max(fit_check)] ]
        print(tabulate(table,headers=["Epoch", "Min", "Average", "Max"]))


def normalTest(
    original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],
    ins = ['I0','I1','Sel'],
    max_epochs = 1000
):
    ''' Normal test of the GA system
    '''
    test = GA(ins,max_epochs,original_ast)
    test.printStats()

    while test.current_epoch < test.max_epochs:
        test.tournamentSelection(10)
        test.current_epoch += 1
        test.printStats()

############# Test Functions  #############

def main():
    normalTest()


if __name__ == "__main__":
    main()
