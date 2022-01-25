import math
from levenshteinDistance import levenshtein
import mutations as m
import math
from treePrint import treePrint
#from params import *
import time
import random
from os import system
from GP import GP
import operations as op
import datetime


class Individual:
    def __init__(self, val):
        self.val = val
        self.fit = 0

class Population(GP):
    def __init__(self, size, mut_rate, cross_rate):
        self.population = []
        self.size = size
        self.original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel']
        self.ins = ['I0','I1','Sel']
        self.len_ins = len(self.ins)
        self.mut_rate = mut_rate
        self.cross_rate = cross_rate
        self.fit_calc = 0

        super().__init__(self.ins, 1000, self.len_ins)
        self.orig_log = self.exhaustiveTest(self.original_ast)

        # Inits the population with random individuals
        for _ in range(size):
            temp_ckt = self.createRandomAST()
            self.population.append(Individual(temp_ckt))
    
    def calcFitness(self) -> None:
        """ Calculates the fitness of each individual in the population """
        for circuit in self.population:
            self.fit_calc += 1
            logical_result = self.exhaustiveTest(circuit.val)
            score = 0
            for t in range(len(logical_result)):
                if logical_result[t] == self.orig_log[t]:
                    score += 1
            circuit.fit = score/len(logical_result)
    
    def parentSelection(self, X) -> None:
        """ Over selection method where the top X% makes up 80% of the next population
              and (100-X)% makes up 20% of the population

            X is a value between 0-100

            All variation and parent selection is performed here.
            A tournament selection is used to decide who the parents are
        """
        # normalize X into a float (called x), so that pop[:x] pulls the (100 - X)%
        # this is done because the sorted function returns a list from lowest to highest
        x = 1 - (X / 100)
        # sorts the population
        self.population = sorted((ind for ind in self.population), key=lambda ind: ind.fit)
        size = round(self.size*x)
        # this is here just to help fight python mutability
        temp_pop = self.population.copy()
        # lower performing
        temp_pop1 = temp_pop[:size]
        # higher performing
        temp_pop2 = temp_pop[size:]

        count = 0
        new_pop = []
        while len(new_pop) < self.size:
            if count <= X:
                circuit = self.tournament(temp_pop2)
                new_pop += self.variation(circuit, temp_pop2)
            else:
                circuit = self.tournament(temp_pop1)
                new_pop += self.variation(circuit, temp_pop1)
            count += 1
        # repopulate the new generation
        self.population = new_pop.copy()
    
    def variation(self, circuit, pop) -> list:
        """ Function to perform mutation or crossover on an individual"""
        r = random.random()
        if r <= self.mut_rate:
            """ Every individual has an mut_rate chance to mutate any given node 
        
                Mutations can be found in the mutations.py file.
                A circuit that is selected for mutation has equal chances to either have a 
                  Node (operator or leaf) mutated to a different value
                  Have a new randomly generated node inserted in place of a leaf
                  Have a random leaf node removed, putting a random leaf in its place
            """
            circuit.val = m.randomMutate(circuit.val, self.ins)
            return [circuit]
            '''
        elif r <= self.mut_rate + self.cross_rate:
            """ Every individual has an cross_rate chance to mutate any given node.
                This is done with replacement, so an individual could crossover with itself

                This was QUITE a challenge to code correctly, if the crossover function in the
                mutations.py file can't find a valid node to crossover, it will just return
                a copy of the original circuit.

                Instead of using a tournament selection for the second parent, a random parent is chosen
            """
            circuit2 = random.choice(pop)
            circuit.val, circuit2.val = m.crossover(circuit.val, circuit2.val, self.ins)
            return [circuit, circuit2]
            '''
        else:
            # chance for circuit to not undergo variation, and just survives into next generation
           return [circuit]

    def __str__(self) -> str:
        temp = ""
        for i in self.population:
            temp += f"{i.val} fit:{i.fit}\n"
        return temp

    def exitConditions(self) -> bool:
        """ Checks if any member of the population is a valid solution
              If so, return true. else return false
        """
        #print('in the exit cases')
        self.calcFitness()
        for c in self.population:
            if c.fit == 1:
                #print(f"this circuit passes {c.val}")
                treePrint(c.val)
                return False
        #print('returning true')
        return True

    @staticmethod
    def tournament(pop, k=30) -> None:
        """ A tournament selection is run with k participants. """
        tournament = random.choices(pop, k=k)
        return max(tournament, key=lambda i: i.fit)
    
    def similar(self) -> float:
        """ returns how many similar circuits are in the population 

            Create a dictionary where each key is every unique individual in the population
            The number of each individuals are counted.
            % unique = Total number with count > 2 / total individuals 

            Returns
                % unique individuals in the population
        """
        # allows a default key in the dictionary with a default value of 0. 
        from collections import defaultdict 
        num_stats = defaultdict(lambda: 0)
        # counts each unique individuals 
        for ind in self.population:
            num_stats[str(ind.val)] += 1
        # Sum the count of individuals whose count is higher than 1. Divide that by the pop size to get % of unique individuals
        return 100*sum(filter(lambda i: i > 1, num_stats.values())) / self.size


def utility():
    results = []
    mr_range = []
    x_range = []
    
    for x in range(10,90,10):
        for mr in range(1,20):
            mr = mr *0.01
            success = []
            print(f"Test mr:{mr} and x:{x}")
            for _ in range(1):
                p = Population(1000,mr,0.3)
                p.calcFitness()
                #print(p)
                gens = 0
                works = True
                
                while gens < 100 and (works := p.exitConditions()):
                    #print("entering")
                    p.parentSelection(x)
                    gens += 1
                
                success.append(p.fit_calc)
            results.append(sum(success)/len(success))
            mr_range.append(mr)
            x_range.append(x)

    #################################################

    from mpl_toolkits import mplot3d
    import numpy as np
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    X, Y = np.meshgrid(mr_range, x_range)
    Z = np.array([results])

    ax.plot_wireframe(X, Y, Z, color='green')
    ax.set_xlabel('Mutation Rate (mr)')
    ax.set_ylabel('Over Selection Size (x)')
    ax.set_zlabel('Success Rate')
    ax.set_title("Genetic Programming 2-1 Multiplexer Circuit Generation")

    fig.savefig('outputs/sga_3d.jpeg')

    #################################################


def normal():

    
    
    results_num_same = []
    for _ in range(10):
        p = Population(1000,0.1,0.3)
        p.calcFitness()
        #print(p)
        gens = 0
        gens_range = []
        num_same = []
        works = True
        
        while gens < 500:
            p.parentSelection(60)
            num_same.append(p.similar())
            gens_range.append(gens)
            gens += 1
        results_num_same.append(num_same)
    
    from statistics import mean

    results_num_same = list(map(mean, zip(*results_num_same)))
    
    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(gens_range,results_num_same,'k*-',label="GP")
    plt.xlabel('Generations')
    plt.ylabel('% Similar')
    plt.title('Convergence Time for GP Systems for 2-1 MUX Generation')
    plt.legend()
    plt.savefig('outputs/time_plot.jpeg')

def main():
    utility()
    #normal()

if __name__ == '__main__':
    main()