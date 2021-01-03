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
from levenshteinDistance import levenshtein
import mutations as m
import pickle as pkl
from treePrint import treePrint
#from params import *
import time
import random
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
        super().__init__(inputs,max_epochs)
        self.original_ast = ast.copy()
        self.current_ast = ast.copy()
        self.min_struc_fit = struc_fit
        self.starting_struc_fit = 1 - struc_fit      
        self.strucFit = 1 - struc_fit
        self.logFit = struc_fit
        self.orig_log = self.exhaustiveTest(ast)
        self.check_ast(self.current_ast)
        '''
            If these inits are the same as whats needed in the other file,
            inheritance would work very nicely.

            Lets keep everything local to this class, and let the other classes
            be the data handeling classes.
        '''

    def checkFitness(
        self, epochs,
        ast = None,
        returnCheck=True,
        print_bool=False
    ):
        ''' Can either return if exit conditions are met or current numerical fitness

        This function first gets the current weights for each fitness function
        (structural and logical) before calculating the overall fitness.
        '''                
        if ast == None:
            ast = self.current_ast
        logical_result = self.exhaustiveTest(ast)
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
            if logical_fitness+structural_fitness >= 1 and logical_fitness / self.logFit == 1:
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
        '''
        temp = self.starting_struc_fit*math.exp(-epochs/self.max_epochs)
        if temp <= self.min_struc_fit:
            self.strucFit = self.min_struc_fit
            self.logFit = 1-self.min_struc_fit
        else:
            self.strucFit = temp
            self.logFit = 1-temp
        if printBool:
            print('Structural Fitness: {:0.4f} and logical fitness: {:0.4f}'.format(
                    self.strucFit,self.logFit))

    
    def hereBoy(
        self, epochs
    ):
        ''' Closer approximation to the HereBOY algorithm

            Returns nothing
            Will either mutate AST or leave AST alone
        '''

        cur_fit = self.checkFitness(epochs)
        mut_ast = m.randomMutation(self.current_ast,self.ins)
        mut_fit = self.checkFitness(epochs,mut_ast)

        if mut_fit > cur_fit:
            self.current_ast = mut_ast
    
    def exhaustiveCheck(
        self, epochs,
        circuit_test=None
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
        if circuit_test == None:
            circuit_test = [self.current_ast]
        circuit_test += m.exhaustiveMutationsCheck(self.current_ast,self.ins)
        circuit_test += m.check_every_add_node(self.current_ast,self.ins)
        circuit_test += m.check_every_remove_node(self.current_ast,self.ins)
        # shuffles the mutation list, as to not 
        random.shuffle(circuit_test)
        fit_check = []
        # checks for best mutated AST from exhaustive add/remove nodes and best mutated node AST
        for circuit in circuit_test:
            fit_check.append(self.checkFitness(epochs,circuit,False))
        max_fit_loc = fit_check.index(max(fit_check))
        self.current_ast = circuit_test[max_fit_loc]


    def randomExhaustive(
        self, 
        print_bool=False
    ):
        ''' Returns a stochastically selected mutated AST

        See issue #6
        '''
        num_mut = random.randint(0,1000)
        if num_mut < 800: # 80%
            if print_bool: print('\nexhaustive mut check')
            self.current_ast = m.exhaustiveMutationsCheck(self.current_ast,self.ins)
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

    @staticmethod
    def params_test(
        total_success = 0,
        num_runs = 0,
        max_epochs = 100,
        #original_ast = ['or','I0','I1'],
        original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],
        ins = ['I0','I1','Sel']
    ):

        for rand in range(0,20):
            lev_total = []
            average_epochs = []
            total_success = 0
            num_runs = 0
            for _ in range(5):
                
                variant = HereBoy(original_ast,ins,max_epochs,.3)
                variant.current_ast = variant.addRandomness(rand)

                epochs = 0

                while epochs < variant.max_epochs and variant.checkFitness(epochs):
                    variant.exhaustiveCheck(epochs) 
                    variant.updateFitness(epochs)
                    epochs +=1

                logic2 = variant.exhaustiveTest(variant.current_ast)
                num_runs += 1
                if variant.orig_log == logic2:
                    total_success += 1
                
                average_epochs.append(epochs)
                lev_total.append(levenshtein(variant.original_ast,variant.current_ast))

            print('\nAverage lev distance for {} initial randoms muts: {}'.format(
                sum(lev_total)/len(lev_total),rand))
            print('Number of hits: {}'.format(total_success/num_runs))
            print('Average number of epochs needed: {}'.format(
                sum(average_epochs)/len(average_epochs)))


    @staticmethod
    def normal_dv(
        original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],
        #original_ast = ['or','I0','I1'],
        #ins = ['I0','I1']
        ins = ['I0','I1','Sel']
    ):
        
        variant = HereBoy(original_ast,ins,100,.3)
        #variant.current_ast = variant.createRandomAST()

        treePrint(variant.original_ast,'temp/Original_AST.gv')
        treePrint(variant.current_ast,'temp/Starting_AST.gv')

        epochs = 0
        same_count = 0
        same_count_max = 3

        start = time.time()
        while epochs < variant.max_epochs and variant.checkFitness(epochs):
            print('\nEpoch: {} Current Fitness: {:0.4f}'.format(epochs,
                variant.checkFitness(epochs,variant.current_ast,False)))
            print('Current AST is: ',variant.current_ast)
            past_ast = variant.current_ast.copy()
            variant.exhaustiveCheck(epochs) 
            variant.updateFitness(epochs)
            
            if past_ast == variant.current_ast:
                same_count += 1
            else:
                same_count = 0
            
            if same_count > same_count_max:
                print('Adding diversity, circuit been way to stable son')
                variant.current_ast = m.randomMutation(variant.current_ast,variant.ins)
                same_count = 0
            

            print('Mutated AST is: ',variant.current_ast)
            epochs +=1
        end = time.time()
        
        logic2 = variant.exhaustiveTest(variant.current_ast)
        

        print('\nOriginal AST: ',variant.original_ast)
        print('Final AST is: ',variant.current_ast)
        print('\nNumber of epochs ran {}'.format(epochs))
        print('Final fitness: {:0.4f}'.format(
                variant.checkFitness(epochs,variant.current_ast,False)))
        print('Run time: {:0.4f}\n'.format(end-start))
        print(list(zip(variant.orig_log,logic2)))
        treePrint(variant.current_ast,'temp/Final_AST.gv')


def main():
    test1 = HereBoy(['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],['I0','I1','Sel'],100,0.3)
    test1.normal_dv()


if __name__ == "__main__":
    main()
