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
import math
from treePrint import treePrint
#from params import *
import time
import random
from os import system
from GP import GP
import operations as op
import datetime
import argparse
import os

def clear():
    _ = system("clear")


class HereBoy(GP):
    ''' Child class of GP class
    '''
    def __init__(
        self, ast, inputs, 
        max_epochs, struc_fit, 
        test_cases = None, rand =.1
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
        self.mutation_fraction = rand
        self.max_score = 1
        '''
            If these inits are the same as whats needed in the other file,
            inheritance would work very nicely.

            Lets keep everything local to this class, and let the other classes
            be the data handeling classes.
        '''

    
    def logicalFitness(
        self, current_ast,
        test_cases = None,
        test_case_per = 0.8,
        print_bool = False
    ):
        ''' Container function which can be called in place of hardcoding
              which testing function is used.
            Returns % of test cases passed. 
        '''
        logical_result = self.exhaustiveTest(current_ast)
        orig_log = self.orig_log.copy()
        if test_cases != None:
            logical_result = logical_result[:math.floor(len(logical_results)*test_case_per)]
            orig_log = self.orig_log[:math.floor(len(logical_results)*test_case_per)]
        score = 0
        # logical fitness check
        for t in range(len(logical_result)):
            if logical_result[t] == orig_log[t]:
                score += 1
        return score/len(logical_result)
        
        ''' Need to reposition
        if print_bool:
            print('\nEpoch {}'.format(epochs))
            print('Orig logic:    {}'.format(self.orig_log))
            print('Current logic: {}'.format(logical_result))
        '''  
    
    def init_ffs(
        self
    ):
        ''' Defines the initial states of each flip flop in the original ast
        '''
        count = 0
        for g in self.original_ast:
            if g == 'ff':
                temp = 'ff_'+str(count)
                op.ff_statements[temp] = False
                count += 1


    def insertCombTrojan(
        self
    ):
        ''' This function will insert a random combinational trojan on some node of the AST

            The trojan is a fault injecting combinatonal trojan, that looks for a specific
              input pattern to inject a fault onto a wire.

            A random wire is selected to be fed into an xor gate. The other input to the xor gate
              is an combination of AND gates that take [2,N] inputs for N number of inputs. The 
              number of inputs used are randomly selected.

            Nothing is returned, but the function calls self and replaces the current AST
              to insert the trojan. 
        '''
        # len calcs 
        len_ast = len(self.current_ast)-1
        len_ins = len(self.ins)-1
        # creates a copy of the current ast
        temp_ast = self.current_ast.copy()
        # picks what wire the trojan will be added on
        wire = random.randint(0,len_ast)
        # selects a random number of inputs in the comb logic
        num_combs = random.randint(2,len_ins+1)
        # breaks the temp ast into pieces to add the trojan
        temp_start = temp_ast[:wire]
        temp_end = temp_ast[wire+1:]
        # adds the torjan to newNode
        new_node = []
        new_node.append('xor')
        for n in range(1,num_combs):
            new_node.append('and')
            new_node.append(self.ins[random.randint(0,len_ins)])
        new_node.append(self.ins[random.randint(0,len_ins)])
        new_node.append(temp_ast[wire])
        # recombine the temp_ast and save it to self.current_ast
        #print('trojan inserted)')
        self.current_ast = temp_start+new_node+temp_end
        
    def __del__(
        self
    ):
        ''' deconstructor 
        '''
        pass

    
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
            ast = self.current_ast.copy()
        logical_fitness = self.logicalFitness(ast)
        logical_fitness = self.logFit*logical_fitness
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
            sets the new weights for each part of the fitness function
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


    def updateHereBoy(
        self, cur_fit
    ):
        '''
            Mutation Bits = αβ 
            α = MaxMutationRate = UserFraction*ChromosomeBits
            β = (MaxScore – MaxCurrentScore)/MaxScore (4)
        '''
        alpha = self.mutation_fraction*len(self.current_ast)
        beta = (self.max_score - cur_fit) / self.max_score
        return math.ceil(alpha*beta)

    
    def hereBoy(
        self, epochs
    ):
        ''' Closer approximation to the HereBOY algorithm

            Returns nothing
            Will either mutate AST or leave AST alone
        '''

        # figures out how many mutations can happen 
        cur_fit = self.checkFitness(epochs,self.current_ast,False)
        num_muts = self.updateHereBoy(cur_fit)
        mut_ast = self.current_ast.copy()
        for _ in range(num_muts):
            mut_ast = m.randomMutation(mut_ast,self.ins)
        mut_fit = self.checkFitness(epochs,mut_ast,False)

        if mut_fit > cur_fit:
            self.current_ast = mut_ast
            #print('current fitness {:0.3f} and mutated fitness {:0.3f} with {} mutations'.format(
            #    cur_fit,mut_fit,num_muts))

    
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
        self, epochs,
        print_bool=False
    ):
        ''' Returns a stochastically selected mutated AST

        See issue #6
        '''
        num_mut = random.randint(0,1000)
        if num_mut < 800: # 80%
            if print_bool: print('\nexhaustive mut check')
            circuit_test = m.exhaustiveMutationsCheck(self.current_ast,self.ins)
            random.shuffle(circuit_test)
            fit_check = []
            # checks for best mutated AST from exhaustive add/remove nodes and best mutated node AST
            for circuit in circuit_test:
                fit_check.append(self.checkFitness(epochs,circuit,False))
            max_fit_loc = fit_check.index(max(fit_check))
            self.current_ast = circuit_test[max_fit_loc]
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
        mutation_mode, test_mode, number_of_runs,
        total_success = 0,
        max_epochs = 8000,
        #original_ast = ['or','I0','I1'],
        original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],
        ins = ['I0','I1','Sel']
    ):

        f = open("paramsOutput.txt","a")
        now = datetime.datetime.now()
        new_str = "\nNew test at: " + now.strftime("%Y-%m-%d %H:%M:%S")+ "\n"
        f.write(new_str)
        if test_mode == 1:
            f.write('Random AST with ')
        elif test_mode == 2:
            f.write('Combination Trojan inserted into AST with ')
        else:
            f.write('Diverse variant AST with ')
        if mutation_mode == 1:
            f.write('software HereBOY\n')
        elif mutation_mode == 2:
            f.write('exhaustive mutations checking\n')
        else:
            f.write('stochastic mutations\n')
        f.close()
        lev_total = []
        average_epochs = []
        total_success = 0
        num_runs = 0
        #rand = rand / 100
        for _ in range(int(number_of_runs)):
            
            variant = HereBoy(original_ast,ins,max_epochs,.3)
            
            # determine testing type from args parse
            if test_mode == 1:
                variant.current_ast = variant.createRandomAST()
            elif test_mode == 2:
                variant.insertCombTrojan()
            else:
                pass
            
            epochs = 0

            start = time.time()
            while epochs < variant.max_epochs and variant.checkFitness(epochs):
                
                if mutation_mode == 1:
                    variant.hereBoy(epochs)
                elif mutation_mode == 2:
                    variant.exhaustiveCheck(epochs)
                else:
                    variant.randomExhaustive(epochs) 
                
                variant.updateFitness(epochs)
                epochs +=1
            end = time.time()

            logic2 = variant.exhaustiveTest(variant.current_ast)
            num_runs += 1
            if variant.orig_log == logic2:
                total_success += 1
            
            average_epochs.append(epochs)
            lev_total.append(levenshtein(variant.original_ast,variant.current_ast))
            
        f = open("paramsOutput.txt","a")
        str1 = "Average lev distance for {:0.4f}\n".format(
            sum(lev_total)/len(lev_total))
        str2 = "Number of hits: {}\n".format(total_success/num_runs)
        str3 = "Average number of epochs needed: {}\n".format(
            sum(average_epochs)/len(average_epochs))
        f.write(str1)
        f.write(str2)
        f.write(str3)
        f.close()
        #print('past')



    @staticmethod
    def normal_dv(
        original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],
        #original_ast = ['or','I0','I1'],
        #ins = ['I0','I1']
        ins = ['I0','I1','Sel'],
        max_epochs = 8000

    ):
        
        variant = HereBoy(original_ast,ins,max_epochs,.3)
        #variant.current_ast = variant.createRandomAST()

        treePrint(variant.original_ast,'temp/Original_AST.gv')
        treePrint(variant.current_ast,'temp/Starting_AST.gv')

        epochs = 0

        start = time.time()
        while epochs < variant.max_epochs and variant.checkFitness(epochs):
            #print('\nEpoch: {} Current Fitness: {:0.4f}'.format(epochs,
                #variant.checkFitness(epochs,variant.current_ast,False)))
            #print('Current AST is: ',variant.current_ast)
            #past_ast = variant.current_ast.copy()
            variant.randomExhaustive(epochs) 
            variant.updateFitness(epochs)
            
            #print('Mutated AST is: ',variant.current_ast)
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


def parse_arguments(
    args=None
) -> None:
    """Returns the parsed arguments.

    Parameters
    ----------
    args: List of strings to be parsed by argparse.
        The default None results in argparse using the values passed into
        sys.args.
    """
    parser = argparse.ArgumentParser(
            description="Argument parsing for genetic programming system",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #parser.add_argument("input_file", help="Path to the input file.")
    parser.add_argument("runs", help="Sets the number of runs to be averaged and saved",
            default=1)
    parser.add_argument("-hb", "--hboy", help="Chooses the hereBOY mutation system",
            default=False, action="store_true")
    parser.add_argument("-s", "--stochastic", help="Chooses the stochastic mutation system",
            default=False, action="store_true")
    parser.add_argument("-e", "--exhaustive", help="Chooses the exhaustive mutation approach",
            default=False, action="store_true")
    parser.add_argument("-r", "--random", help="Sets the number of runs to be averaged and saved",
            default=False, action="store_true")
    parser.add_argument("-ct", "--combinational_trojan", help="Sets the number of runs to be averaged and saved",
            default=False, action="store_true")
    parser.add_argument("-v", "--variant", help="Sets the number of runs to be averaged and saved",
            default=False, action="store_true")

    args = parser.parse_args(args=args)
    return args

def main(
    runs=1,
    hboy=False, 
    stochastic=False,
    exhaustive=False,
    random=False, 
    combinational_trojan=False,
    variant=False
) -> None:
    """ Main function.

    Parameters
    ----------
    runs: int
        Number of runs to average for testing. Default is 1 test
    here_boy: bool
        Mutation type is the software HereBOY approach. 
    stochastic: bool
        Mutation type is a stoachatic mutations check
    exhaustive: bool
        Mutation type is exhaustive mutation checking
    random: bool
        Starting circuit is randomly generated
    combinational_trojan: bool
        Random combinational trojan is inserted
    variant: bool
        A varint is created from the original ast
    ------
    FileNotFoundError
        Means that the input file was not found.
    """   
    # Error check if the file even exists
    #if not os.path.isfile(input_file):
    #    raise FileNotFoundError("File not found: {}".format(input_file))
    
    test1 = HereBoy(
        ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'], # ast
        ['I0','I1','Sel'], # ins
        40000, # num epochs
        0.3 # init struct fit
    )

    if hboy:
        mutation_mode = 1
    elif exhaustive:
        mutation_mode = 2
    else:
        mutation_mode = 3

    if random:
        test_mode = 1
    elif combinational_trojan:
        test_mode = 2
    else:
        test_mode = 3

    test1.params_test(
        mutation_mode,
        test_mode,
        runs
    )


if __name__ == "__main__":
    import sys
    args = parse_arguments()
    try:
        main(**vars(args))
    except FileNotFoundError as exp:
        print(exp, file=sys.stderr)
        exit(-1)