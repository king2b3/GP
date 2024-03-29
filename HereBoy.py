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

def clear():
    _ = system("clear")


class HereBoy(GP):
    ''' Child class of GP class
    '''
    def __init__(self, ast, inputs, max_epochs, struc_fit, 
        in_num,test_cases = None, rand =.1, cir_depth=5,
        brute_force_test=(True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True)):
        super().__init__(inputs,max_epochs,in_num)
        if ast == None:
            #print(f"Creating an AST {cir_depth=}")
            self.original_ast = self.createRandomAST(cir_depth-1,cir_depth+1)
        else:
            self.original_ast = ast.copy()
        self.current_ast = self.original_ast.copy()
        self.min_struc_fit = struc_fit
        self.starting_struc_fit = 1 - struc_fit      
        self.strucFit = 1 - struc_fit
        self.logFit = struc_fit
        self.orig_log = self.exhaustiveTest(self.original_ast)
        self.check_ast(self.current_ast)
        self.mutation_fraction = rand
        self.max_score = 1
        self.num_muts = 0
        self.brute_force_test = gen_brute()
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
            orig_log = self.orig_log[:math.floor(len(logical_result)*test_case_per)]
            logical_result = logical_result[:math.floor(len(logical_result)*test_case_per)]
        score = 0
        # logical fitness check
        #print(len(logical_result))
        #print(len(orig_log))
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
    
    def bruteLogicalFitness(self, current_ast):
        ''' Container function which can be called in place of hardcoding
              which testing function is used.
            Returns % of test cases passed. 
        '''
        logical_result = self.exhaustiveTest(current_ast)
        orig_log = self.orig_log.copy()
        score = 0
        temp_score = 0
        # EX [True, False, None, None, False, None False, True]
        for t in range(len(logical_result)):
            if self.brute_force_test[t]:
                temp_score += 1
                if logical_result[t] == orig_log[t]:
                    score += 1
        if temp_score == 0:
            return 0
        return score/temp_score
        

    def init_ffs(self):
        ''' Defines the initial states of each flip flop in the original ast
        '''
        count = 0
        for g in self.original_ast:
            if g == 'ff':
                temp = 'ff_'+str(count)
                op.ff_statements[temp] = False
                count += 1


    def insertCombTrojan(self):
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
        
    def __del__(self):
        ''' deconstructor 
        '''
        ...

    
    def checkFitness(
        self, epochs,
        ast = None,
        returnCheck=True,
        print_bool=False,
        log_fit_bool=None
    ):
        ''' Can either return if exit conditions are met or current numerical fitness

        This function first gets the current weights for each fitness function
        (structural and logical) before calculating the overall fitness.
        '''                
        if ast == None:
            ast = self.current_ast.copy()
        logical_fitness = self.bruteLogicalFitness(ast)
        #logical_fitness = self.logicalFitness(ast,log_fit_bool)
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
            Mutation Bits = alpha * beta 
            alpha = MaxMutationRate = UserFraction*ChromosomeBits
            beta = (MaxScore – MaxCurrentScore)/MaxScore (4)
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
        ''' Sets a stochastically selected mutated AST as the current AST

        See issue #6
        '''
        self.num_muts += 1
        num_mut = random.randint(0,1000)
        if num_mut < 500: # 50%
            if print_bool: print('\nexhaustive mut check')
            circuit_test = m.exhaustiveMutationsCheck(self.current_ast,self.ins)
            random.shuffle(circuit_test)
            fit_check = []
            # checks for best mutated AST from exhaustive add/remove nodes and best mutated node AST
            for circuit in circuit_test:
                fit_check.append(self.checkFitness(epochs,circuit,False,log_fit_bool=True))
            max_fit_loc = fit_check.index(max(fit_check))
            self.current_ast = circuit_test[max_fit_loc]
        elif num_mut < 800: # 30%
            if print_bool: print('\nRandom Mutation')
            self.current_ast = m.randomMutate(self.current_ast,self.ins)
        elif num_mut < 900: # 10%
            if print_bool: print('\nAdd a randoom node')
            self.current_ast = m.addNode(self.current_ast,self.ins)
        else: # 10%
            if print_bool: print('\nRemove a random node')
            self.current_ast = m.removeNode(self.current_ast,self.ins)

    
    @staticmethod
    def scalabilityTest(
            mutation_mode, test_mode, number_of_runs,
            nums_ins=3,
            total_success = 0,
            max_epochs = 4000,
            #original_ast = None,
            original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],
            #ins = ['I0','I1','Sel']
            ins = None

        ):

            f = open("paramsOutput.txt","a")
            now = datetime.datetime.now()
            new_str = "\nNew test at: " + now.strftime("%Y-%m-%d %H:%M:%S")+ "\n"
            max_depth = nums_ins*2
            f.write(new_str)
            f.write('Scalability Test with {} inputs '.format(max_depth))

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
            for _ in range(int(number_of_runs)):
                print('gets inside of loop')
                
                variant = HereBoy(original_ast,ins,max_epochs,.3,nums_ins)
                
                # determine testing type from args parse
                # variant.original_ast = variant.createRandomAST(max_depth-1,max_depth+1)
                print('got here')
                variant.current_ast = variant.original_ast.copy()
                variant.orig_log = variant.exhaustiveTest(variant.current_ast)
                
                if test_mode == 1:
                    variant.current_ast = variant.createRandomAST(29,31)
                elif test_mode == 2:
                    variant.insertCombTrojan()
                else:
                    pass
                
                
                epochs = 0

                start = time.time()
                while epochs < variant.max_epochs and variant.checkFitness(epochs):
                    print('here')
                    
                    if mutation_mode == 1:
                        variant.hereBoy(epochs)
                    #elif mutation_mode == 2:
                    #    variant.exhaustiveCheck(epochs)
                    else:
                        variant.randomExhaustive(epochs) 
                    
                    variant.updateFitness(epochs)
                    #print('Curret epoch {}\nCurrent AST {}'.format(epochs,variant.current_ast))
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
    def params_test(
        mutation_mode, test_mode, number_of_runs,
        total_success = 0,
        max_epochs = 8000,
        #original_ast = ['or','I0','I1'],
        #original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],
        #ins = ['I0','I1','Sel']
        #original_ast = ['nand','nand','N1','N3','nand','N2','nand','N3','N6'],
        #ins = ['N1','N2','N3','N6']
        original_ast = ['nor','and','PB1','GB1','nor','and','GB0','and','not','CN','GB1','and','GB1','and','PBO','GB0'],
        ins = ['PB0','PB1','GB0','GB1','CN']

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

    def size(self) -> int:
        return len(self.current_ast) - len(self.original_ast)


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

def mainTest(
    mutation_mode, test_mode, number_of_runs,
    nums_ins = 3,
    total_success = 0,
    max_epochs = 1000,
    original_ast = None, # comb logic
    ins = ['A','B','C','D'] #comb logic
    #original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'], # 2-1
    #ins = ['I0','I1','Sel'] # 2-1
    #original_ast = ['or','or','and','and','not','s1','not','s2','d0','and','and','not','s1','s0','d1','or','and','and','s1','not','s0','d0','and','and','s1','s0','d3'],
    #ins = ['s0','s1','s2','d1','d2','d3']
    #original_ast = ['or','and','A','B','and','Cin','xor','A','B'], # carry out
    #ins = ['A','B','Cin'] # carry out
):
    from timer import Timer
    f = open("paramsOutput.txt","a")
    now = datetime.datetime.now()
    new_str = "\nNew test at: " + now.strftime("%Y-%m-%d %H:%M:%S")+ "\n"
    max_depth = nums_ins*2
    f.write(new_str)
    f.write('Scalability Test with {} depth '.format(max_depth))

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

    import os
    results = []
    t = Timer()
    a = 3
    b = 31
    #for loop for inputs
    for i in range(a,b):
        t.start_timer()
        for _ in range(int(number_of_runs)):

            print("Number of Inputs: " + str(i))
            
            output_folder = 'temp/temp/'

            #path = output_folder+str(time.time())
            #os.mkdir(path)
            #print(f"{i=}")
            variant = HereBoy(original_ast,ins,max_epochs,.3,i)

            # determine testing type from args parse
            #variant.original_ast = variant.createRandomAST(max_depth-1,max_depth+1)
            #variant.current_ast = variant.original_ast.copy()
            #variant.orig_log = variant.exhaustiveTest(variant.current_ast)
            #treePrint(variant.current_ast, "temp/original")
            if test_mode == 1:
                variant.current_ast = variant.createRandomAST(4,6)
                #print("random ast created")
            elif test_mode == 2:
                variant.insertCombTrojan()
                #print("trojan inserted")
            else:
                #print("variant used")
                pass
            
            
            epochs = 0
            #treePrint(variant.current_ast, "temp/original")

            start = time.time()
            while epochs < variant.max_epochs and variant.checkFitness(epochs,log_fit_bool=None):
                
                variant.randomExhaustive(epochs) 
                
                variant.updateFitness(epochs)
                #print('Curret epoch {}\nCurrent AST {}'.format(epochs,variant.current_ast))
                epochs +=1
                #treePrint(variant.current_ast, path+'/'+str(epochs))
            end = time.time()

            #print(variant.exhaustiveTest(variant.current_ast))
            #print(variant.exhaustiveTest(variant.original_ast))

            logic1 = variant.exhaustiveTest(variant.current_ast)
            logic2 = variant.exhaustiveTest(variant.original_ast)
            num_runs += 1
            if logic1 == logic2:
                total_success += 1
            
            average_epochs.append(epochs)
            lev_total.append(levenshtein(variant.original_ast,variant.current_ast))
            #treePrint(variant.current_ast, "temp/final")
            
            '''
            # creates the gif 
            command1 = "ffmpeg -framerate 1 -f image2 -i "+path+"/%d.png "+path+"/video.avi"
            command2 = "ffmpeg -i "+path+"/video.avi temp/temp"+str(".gif")
            os.system(command1)
            os.system(command2)
            '''
        t.end_timer()
        results.append(float(str(t))/float(number_of_runs))

    #print(f"{num_runs=}")
    #print(f"{total_success=}")
    print(f"{results}")

    import matplotlib.pyplot as plt

    plt.style.use('seaborn-whitegrid')

    inputs = list(range(a,b))
    plt.plot(inputs,results, 'o', color='black')
    plt.title("Scalability of ES")
    plt.xlabel("Number of Inputs")
    plt.ylabel("Average Time to Completion (Seconds)")
    
    plt.show()
    
    f = open("paramsOutput.txt","a")
    str1 = "Average lev distance for {:0.4f}\n".format(
        sum(lev_total)/len(lev_total))
    str2 = "Number of hits: {}\n".format(total_success/num_runs)
    str3 = "Average number of epochs needed: {}\n".format(
        sum(average_epochs)/len(average_epochs))
    str4 = f"Time simulation was run {f}"
    f.write(str1)
    f.write(str2)
    f.write(str3)
    #f.write(str4)
    f.close()
    #print('past')

def bruteForceTest(number_of_runs) -> None:
    nums_ins = 3
    total_success = 0
    max_epochs = 1000
    original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'] # 2-1
    ins = ['I0','I1','Sel'] # 2-1

    def clear():
        _ = system("clear")

    from timer import Timer
    from itertools import product
    f = open("paramsOutput.txt","a")
    now = datetime.datetime.now()
    new_str = "\nRunning Brute Force Partial Test Cases " + now.strftime("%Y-%m-%d %H:%M:%S")+ "\n"
    f.write(new_str)

    f.write('stochastic mutations\n')
    f.close()


    total_success = 0
    num_runs = 0

    import os
    #t = Timer()

    #used to store results. test_mode is the key
    #gen_results = {0:[], 1:[], 2:[]}
    #lev_results = {0:[], 1:[], 2:[]}
    #time_results = {0:[], 1:[], 2:[]}
    #mut_results = {0:[], 1:[], 2:[]}
    #size_results = {0:[], 1:[], 2:[]}
    #succ_results = {0:[], 1:[], 2:[]}
    #lev_total = []
    #average_epochs = []
    for test_mode in range(3):
        '''
        0: variant
        1: comb trojan
        2: random
        '''
        f = open("brute_paramsOutput.txt","a")
        temp_str = "start type: " + str(test_mode) + "\n"
        f.write(temp_str)
        #print("########")
        #print("Test " + str(test_mode))
        #print("########")
        f.close()
        args = [[False,True] for i in range(8) ]
        for comb in product(*args):
	        #print(comb)
            ave_lev = 0
            ave_gens = 0
            ave_muts = 0
            ave_size = 0
            ave_succ = 0
            #t.start_timer()
            #print(f"Comb logic: {comb}")
            for run in range(int(number_of_runs)):
                #clear()
                #print("test " + str(run) + " out of " + str(int(number_of_runs) - 1))
                #init the class
                variant = HereBoy(original_ast,ins,max_epochs,.3,3,brute_force_test=comb)

                if test_mode == 0:
                    variant.current_ast = variant.createRandomAST(4,6)
                    #print("random ast created")
                elif test_mode == 1:
                    variant.insertCombTrojan()
                    #print("trojan inserted")
                else:
                    #print("variant used")
                    pass 
                
                epochs = 0
                start = time.time()
                while epochs < variant.max_epochs and variant.checkFitness(epochs,log_fit_bool=None):
                    variant.randomExhaustive(epochs) 
                    variant.updateFitness(epochs)
                    epochs +=1
                end = time.time()

                logic1 = variant.exhaustiveTest(variant.current_ast)
                logic2 = variant.exhaustiveTest(variant.original_ast)
                num_runs += 1
                if logic1 == logic2:
                    total_success += 1
                    ave_succ += 1
                
                '''
                average_epochs.append(epochs)
                temp_lev = levenshtein(variant.original_ast,variant.current_ast)
                lev_total.append(temp_lev)
                ave_gens += epochs
                ave_lev += temp_lev
                ave_muts += variant.num_muts
                ave_size += variant.size()            
                '''
            if ave_succ/int(number_of_runs) > 0.5:
                f = open("brute_paramsOutput.txt","a")
                f.write(f"Test patterns allowed: {comb}")
                f.write(f'  Success rate: {ave_succ/int(number_of_runs)}\n')
                f.close()

            #t.end_timer()
            '''
            gen_results[test_mode].append(float(ave_gens)/float(number_of_runs))
            time_results[test_mode].append(float(str(t))/float(number_of_runs))
            lev_results[test_mode].append(float(ave_lev)/float(number_of_runs))
            mut_results[test_mode].append(float(ave_muts)/float(number_of_runs))
            size_results[test_mode].append(float(ave_size)/float(number_of_runs))
            succ_results[test_mode].append(float(ave_succ)/float(number_of_runs))
            '''
    #writes the testing scheme to the file
    f = open("brute_paramsOutput.txt","a")
    f.write(f"Original Logic: {variant.orig_log}\n")
    f.close()



def scalabilityTest(number_of_runs) -> None:
    nums_ins = 3
    total_success = 0
    max_epochs = 1000
    original_ast = None # comb logic
    ins = ['A','B','C','D'] #comb logic

    def clear():
        _ = system("clear")

    from timer import Timer
    f = open("paramsOutput.txt","a")
    now = datetime.datetime.now()
    new_str = "\nGenerating Scalability Plots: " + now.strftime("%Y-%m-%d %H:%M:%S")+ "\n"
    f.write(new_str)

    f.write('stochastic mutations\n')
    f.close()


    total_success = 0
    num_runs = 0

    import os
    t = Timer()
    a = 3   #start input range
    b = 31  #end input range

    #used to store results. test_mode is the key
    gen_results = {0:[], 1:[], 2:[]}
    lev_results = {0:[], 1:[], 2:[]}
    time_results = {0:[], 1:[], 2:[]}
    mut_results = {0:[], 1:[], 2:[]}
    size_results = {0:[], 1:[], 2:[]}
    succ_results = {0:[], 1:[], 2:[]}
    lev_total = []
    average_epochs = []
    for test_mode in range(3):
        '''
        0: variant
        1: comb trojan
        2: random
        '''
        f = open("paramsOutput.txt","a")
        temp_str = "start type: " + str(test_mode) + "\n"
        f.write(temp_str)
        print("########")
        print("Test " + str(test_mode))
        print("########")
        for i in range(a,b):
            ave_lev = 0
            ave_gens = 0
            ave_muts = 0
            ave_size = 0
            ave_succ = 0
            t.start_timer()
            print("Number of Inputs: " + str(i))
            for run in range(int(number_of_runs)):
                #clear()
                print("test " + str(run) + " out of " + str(int(number_of_runs) - 1))
                #init the class
                variant = HereBoy(original_ast,ins,max_epochs,.3,i)

                if test_mode == 0:
                    variant.current_ast = variant.createRandomAST(4,6)
                    #print("random ast created")
                elif test_mode == 1:
                    variant.insertCombTrojan()
                    #print("trojan inserted")
                else:
                    #print("variant used")
                    pass 
                
                epochs = 0
                start = time.time()
                while epochs < variant.max_epochs and variant.checkFitness(epochs,log_fit_bool=None):
                    variant.randomExhaustive(epochs) 
                    variant.updateFitness(epochs)
                    epochs +=1
                end = time.time()

                logic1 = variant.exhaustiveTest(variant.current_ast)
                logic2 = variant.exhaustiveTest(variant.original_ast)
                num_runs += 1
                if logic1 == logic2:
                    total_success += 1
                    ave_succ += 1
                
                average_epochs.append(epochs)
                temp_lev = levenshtein(variant.original_ast,variant.current_ast)
                lev_total.append(temp_lev)
                ave_gens += epochs
                ave_lev += temp_lev
                ave_muts += variant.num_muts
                ave_size += variant.size()

            t.end_timer()
            gen_results[test_mode].append(float(ave_gens)/float(number_of_runs))
            time_results[test_mode].append(float(str(t))/float(number_of_runs))
            lev_results[test_mode].append(float(ave_lev)/float(number_of_runs))
            mut_results[test_mode].append(float(ave_muts)/float(number_of_runs))
            size_results[test_mode].append(float(ave_size)/float(number_of_runs))
            succ_results[test_mode].append(float(ave_succ)/float(number_of_runs))


    import pickle

    pickle.dump(gen_results, open( "p/gen_results.p", "wb" ) )
    pickle.dump(time_results, open( "p/time_results.p", "wb" ) )
    pickle.dump(lev_results, open( "p/lev_results.p", "wb" ) )
    pickle.dump(mut_results, open( "p/mut_results.p", "wb" ) )
    pickle.dump(size_results, open( "p/size_results.p", "wb" ) )
    pickle.dump(succ_results, open( "p/succ_results.p", "wb" ) )

    #############################################################################################
    
    #plot the final results
    import matplotlib.pyplot as plt
    inputs = list(range(a,b))

    plt.style.use('seaborn-whitegrid')
    plt.plot(inputs,gen_results[0], 'o', color='black', label="Random Start")
    plt.plot(inputs,gen_results[1], 'o', color='blue', label="Combinational Trojan Inserted")
    plt.plot(inputs,gen_results[2], 'o', color='red', label="Variant Generation")
    plt.legend()
    plt.title("Scalability of ES Across Averaged over " + str(number_of_runs) + " Runs")
    plt.xlabel("Number of Inputs")
    plt.ylabel("Average Generations to Completion")
    #plt.show()
    plt.savefig("gen_results_scal.png")

    plt.figure()
    plt.style.use('seaborn-whitegrid')
    plt.plot(inputs,time_results[0], 'o', color='black', label="Random Start")
    plt.plot(inputs,time_results[1], 'o', color='blue', label="Combinational Trojan Inserted")
    plt.plot(inputs,time_results[2], 'o', color='red', label="Variant Generation")
    plt.legend()
    plt.title("Scalability of ES Across Averaged over " + str(number_of_runs) + " Runs")
    plt.xlabel("Number of Inputs")
    plt.ylabel("Average Time to Completion (Seconds)")
    #plt.show()
    plt.savefig("time_results_scal.png")

    plt.figure()
    plt.style.use('seaborn-whitegrid')
    plt.plot(inputs,lev_results[0], 'o', color='black', label="Random Start")
    plt.plot(inputs,lev_results[1], 'o', color='blue', label="Combinational Trojan Inserted")
    plt.plot(inputs,lev_results[2], 'o', color='red', label="Variant Generation")
    plt.legend()
    plt.title("Scalability of ES Across Averaged over " + str(number_of_runs) + " Runs")
    plt.xlabel("Number of Inputs")
    plt.ylabel("Average Levenshtien Distance")
    #plt.show()
    plt.savefig("lev_results_scal.png")

    plt.figure()
    plt.style.use('seaborn-whitegrid')
    plt.plot(inputs,mut_results[0], 'o', color='black', label="Random Start")
    plt.plot(inputs,mut_results[1], 'o', color='blue', label="Combinational Trojan Inserted")
    plt.plot(inputs,mut_results[2], 'o', color='red', label="Variant Generation")
    plt.legend()
    plt.title("Scalability of ES Across Averaged over " + str(number_of_runs) + " Runs")
    plt.xlabel("Number of Inputs")
    plt.ylabel("Average Number of Mutations Needed")
    #plt.show()
    plt.savefig("mut_results_scal.png")

    plt.figure()
    plt.style.use('seaborn-whitegrid')
    plt.plot(inputs,size_results[0], 'o', color='black', label="Random Start")
    plt.plot(inputs,size_results[1], 'o', color='blue', label="Combinational Trojan Inserted")
    plt.plot(inputs,size_results[2], 'o', color='red', label="Variant Generation")
    plt.legend()
    plt.title("Scalability of ES Across Averaged over " + str(number_of_runs) + " Runs")
    plt.xlabel("Number of Inputs")
    plt.ylabel("Average Size of Final Circuit (Nodes)")
    #plt.show()
    plt.savefig("size_results_scal.png")

    plt.figure()
    plt.style.use('seaborn-whitegrid')
    plt.plot(inputs,succ_results[0], 'o', color='black', label="Random Start")
    plt.plot(inputs,succ_results[1], 'o', color='blue', label="Combinational Trojan Inserted")
    plt.plot(inputs,succ_results[2], 'o', color='red', label="Variant Generation")
    plt.legend()
    plt.title("Scalability of ES Across Averaged over " + str(number_of_runs) + " Runs")
    plt.xlabel("Number of Inputs")
    plt.ylabel("Average Number of Successful Evolutions")
    #plt.show()
    plt.savefig("succ_results_scal.png")


    #############################################################################################


    #open the file back up for debug
    f = open("paramsOutput.txt","a")    
    #if num_runs != total_successes:
    #    temp_str = "CAUTION! NOT ALL SIMS PASSED:" + str(total_successes) + \
    #        " out of " + str(num_runs)
    #    f.write(temp_str)

    str1 = "Average lev distance for {:0.4f}\n".format(
        sum(lev_total)/len(lev_total))
    str2 = "Number of hits: {}\n".format(total_success/num_runs)
    str3 = "Average number of epochs needed: {}\n".format(
        sum(average_epochs)/len(average_epochs))
    str4 = f"Time simulation was run {f}"
    f.write(str1)
    f.write(str2)
    f.write(str3)
    #f.write(str4)
    f.close()
    #print('past')



def params_test(
        mutation_mode, test_mode, number_of_runs,
        total_success = 0,
        max_epochs = 8000,
        #original_ast = ['or','I0','I1'],
        #original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],
        #ins = ['I0','I1','Sel']
        #original_ast = ['nand','nand','N1','N3','nand','N2','nand','N3','N6'],
        #ins = ['N1','N2','N3','N6']
        original_ast = ['nor','and','PB1','GB1','nor','and','GB0','and','not','CN','GB1','and','GB1','and','PB0','GB0'],
        ins = ['PB0','PB1','GB0','GB1','CN']

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
            
            variant = HereBoy(original_ast,ins,max_epochs,.3,5)
            
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


def gen_brute():
    in_size = 5
    cases = math.floor(2**in_size*.8)
    temp = []
    for _ in range(cases):
        temp.append(True)
    for _ in range(2**in_size - cases):
        temp.append(False)
    random.shuffle(temp)
    temp = tuple(temp)
    return temp

def gen_best():
    in_size = 5
    cases = 2**in_size
    temp = []
    for _ in range(cases):
        temp.append(True)
    return temp

def main():
    gen_brute()


if __name__ == "__main__":
    main()
