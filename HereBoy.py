#   Python 3.7.3
#   Bayley King
#   University of Cincinnati MIND Lab
'''
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
#import StringComp 
from levenshteinDistance import levenshtein
import mutations as m
import pickle as pkl
from treePrint import treePrint
from params import *
import time
import random
import itertools
import sys
from os import system
from GP import GP
import operations as op

def clear():
    _ = system("clear")


class HereBoy(GP):
    ''' Child class of GP class
    '''
    def __init__(
        self, ast, inputs, 
        max_epochs, struc_fit
    ):
        super().__init__(self,ast,inputs,max_epochs)
        self.start_struc_fit, self.strucFit = struc_fit
        self.start_log_fit, self.logFit = 1 - struc_fit
        #self.strucFit = struc_fit
        #self.logFit = = 1 - struc_fit
        '''
            If these inits are the same as whats needed in the other file,
            inheritance would work very nicely.

            Lets keep everything local to this class, and let the other classes
            be the data handeling classes.
        '''

    def checkFitness(
        self, epochs,
        ast = self.current_ast,
        returnCheck=True,
        print_bool=False
    ):
        ''' Can either return if exit conditions are met or current numerical fitness

        This function first gets the current weights for each fitness function
        (structural and logical) before calculating the overall fitness.
        '''                
        logical_result = exhaustiveTest(ast)
        if print_bool:
            print('\nEpoch {}'.format(epochs))
            print('Orig logic:    {}'.format(self.orig_log))
            print('Current logic: {}'.format(logical_result))
        score = 0
        # logical fitness check
        for t in range(len(logical_result)):
            if logical_result[t] == self.orig_log[t]:
                score += 1
        logical_fitness = self.logFit*(score/len(logical_result)) 
        #structural fitness check
        structural_fitness = levenshtein(ast,self.original_ast)
        if structural_fitness > 1:
            structural_fitness = 1
        structural_fitness = self.strucFit*structural_fitness

        if returnCheck:
            # By default True. Returns if exit conditions are met or not
            if logical_fitness+structural_fitness >= 1 and logical_fitness / log_fit == 1:
                return False
            else:
                return True
        else:
            # Returns the actual numerical fitness value of the circuit
            return logical_fitness+structural_fitness


    def updateFitness(
        self, epochs, 
        printBool=False
    ):
        '''
            Returns the new weights for each part of the fitness function
            
        See issue #8
        '''
        startSim = .7
        minSim = .3
        maxEpochs = 1000

        temp = self.start_struc_fit*math.exp(-epochs/self.maxEpochs)
        if temp <= self.start_struc_fit:
            self.strucFit = self.start_struc_fit
            self.logFit = 1-self.start_struc_fit
        else:
            self.strucFit = temp
            self.logFit = 1-temp
        if printBool:
            print('Structural Fitness:',self.strucFit,' and logical fitness:',self.logFit)
        #return strucFit,logFit


    def exhaustiveCheck(
        self, epochs,
        circuit_test=[]
    ):
        ''' HereBOY exhaustive mutation check
        
        This function will check for EVERY possbile:
            Mutation on every node
            Every possbile added node
            Every possbile removed node
        and will return which mutation gives the highest overall fitness

        Returns best mutated AST. If best scores are the same across multiple
            variants, the best first option is returned. The exhaustive mutations
            should be checked first, which doesn't change the size of the AST.  
        '''
        circuit_test += m.exhaustiveMutationsCheck(self.current_ast,self.ins)
        circuit_test += m.check_every_add_node(self.current_ast,self.ins)
        circuit_test += m.check_every_remove_node(self.current_ast,self.ins)
        # checks for best mutated AST from exhaustive add/remove nodes and best mutated node AST
        fit_check = []
        for circuit in circuit_test:
            fit_check.append(checkFitness(epochs,circuit,False))
        max_fit_loc = fit_check.index(max(fit_check))
        return circuit_test[max_fit_loc]


    def randomExhaustive(
        self, print_bool=False
    ):
        ''' Returns a stochastically selected mutated AST

        See issue #6
        '''
        num_mut = random.randint(0,1000)
        if num_mut < 800: # 80%
            if print_bool: print('\nexhaustive mut check')
            self.current_ast = exhaustiveMutationsCheck(self.current_ast,self.ins)
        elif num_mut < 900: # 10%
            if print_bool: print('\nRandom Mutation')
            self.current_ast = m.randomMutate(self.current_ast,self.ins)
        elif num_mut < 910: # 1%
            if print_bool: print('\nAdd a randoom node')
            self.current_ast = m.addNode(self.current_ast,self.ins)
        elif num_mut < 920: # 1%
            if print_bool: print('\nRemove a random node')
            self.current_ast = m.removeNode(self.current_ast,self.ins)
        #elif num_mut < 970: # 5%
        #    if print_bool: print('\nCrossover a random node')
        #    current_ast = m.crossover(current_ast,ins)
        else: # 3%
            pass


############# Test Functions  #############

def params_test(
    total_success = 0,
    num_runs = 0,
    max_epochs = 1000,
    original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],
    ins = ['I0','I1','Sel']
):

    for rand in range(1,20):
        lev_total = []
        average_epochs = []
        total_success = 0
        num_runs = 0
        for _ in range(100):
            
            variant = HereBoy(original_ast,ins,max_epochs,.7)
            variant.addRandomness(current_ast,ins,rand)

            epochs = 0

            while epochs < max_epochs and variant.checkFitness(epochs):
                variant.randomExhaustive()
                epochs +=1

            logic2 = exhaustiveTest(variant.current_ast)
            num_runs += 1
            if orig_logic == logic2:
                total_success += 1
            
            average_epochs.append(epochs)
            lev_total.append(levenshtein(variant.original_ast,variant.current_ast))

        print('\nAverage lev distance for {} initial randoms muts: {}'.format(
            sum(lev_total)/len(lev_total),rand))
        print('Number of hits: {}'.format(total_success/num_runs))
        print('Average number of epochs needed: {}'.format(
            sum(average_epochs)/len(average_epochs)))


def normal_dv(
    original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],
    ins = ['I0','I1','Sel']
):
    
    variant = HereBoy(original_ast,ins,1000,.7)
    
    variant.addRandomness()
    print(variant.original_ast)
    print(variant.current_ast)
    treePrint(variant.original_ast,'temp/Original_AST.gv')
    treePrint(variant.current_ast,'temp/Starting_AST.gv')

    epochs = 0
    same_count = 0
    same_count_max = 3

    start = time.time()
    while epochs < variant.max_epochs and variant.checkFitness(epochs):
        '''
        if epochs % 50 == 0:
            print('Epoch:',epochs,' Current Fitness:',fit)
            print('Current AST is: ',current_ast)
        '''
        print('Epoch: {} Current Fitness: {}'.format(epochs,
            checkFitness(epochs,variant.current_ast,False)))
        print('Current AST is: ',variant.current_ast)
        past_ast = variant.current_ast.copy()
        variant.exhaustiveCheck(epochs) 
        
        if past_ast == variant.current_ast:
            same_count += 1
        else:
            same_count = 0
        
        if same_count > same_count_max:
            variant.current_ast = m.randomMutation(variant.current_ast,variant.ins)
            same_count = 0
        

        print('Mutated AST is: ',variant.current_ast)
        epochs +=1
    end = time.time()
    
    logic2 = variant.exhaustiveTest()
    

    print('\nOriginal AST: ',variant.original_ast)
    print('Final AST is: ',variant.current_ast)
    print('\nNumber of epochs ran {}'.format(epochs))
    print('Final fitness: {:0.4f}'.format(
            variant.checkFitness(epochs,variant.current_ast,False)))
    print('Run time: {:0.4f}\n'.format(end-start))
    print(list(zip(variant.orig_logic,logic2)))
    treePrint(variant.current_ast,'temp/Final_AST.gv')


def main():
    normal_dv()


if __name__ == "__main__":
    main()