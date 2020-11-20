#   Python 3.7.3
#   Bayley King
#   University of Cincinnati MIND Lab
'''
    General container file for GP system using here boy algorithm.
    Takes in from mutations.py, lexer.py, stringComp.py and exhaustiveTest.py.
    
'''
binOps = ['or','and','nand']
soloOps = ['not']

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

def clear():
    _ = system("clear")


class HereBoy:
    def __init__(self,ast,inputs):
        self.origAST = self.currentAST = ast
        self.inputs = inputs
        
        #self.m = mutations.mutations()
        #self.strCmp = StringComp.StringComp() # outdated, see levenshteinDistance.py 
        '''
            If these inits are the same as whats needed in the other file,
            inheritance would work very nicely.

            Lets keep everything local to this class, and let the other classes
            be the data handeling classes.
        '''
    def outputResults(self):
        print('saving results')


    def returnLogic(self,l,loc):
        if l in binOps:
            children = self.currentAST[loc+1:loc+3]
            #print('\tBin Op:',l,'with children:',children)
            for c in range(len(children)):
                if children[c] in binOps or children[c] in soloOps:
                    #print('CHILD CHANGED, ORIGINAL',children)
                    #print(self.currentAST,loc+3,self.currentAST[loc+3],len(children),c)
                    children[c] = self.returnLogic(children[c],loc+1)
                    try:
                        children[c+1] = self.currentAST[loc+3]
                    except:
                        pass
                    #print('CHILD CHANGED, NEW',children)
                loc += 1
            #print('\t\tBinops results',children,BinOps(children,l))
            return BinOps(children,l)
                
        elif l in soloOps:
            child = self.currentAST[loc+1]
            #print('\tSolo Op:',l,'with child:',child)
            if child in binOps or child in soloOps:
                self.returnLogic(child,loc+1)
            else:
                #print('\t\tSolo Results',SoloOps(child,l))
                return SoloOps(child,l)

        elif type(l) == bool:
            pass
        
        else:
            self.error()
        

    def error(self):
        raise Exception('Invalid operator in AST')


def checkFitness(current_ast,original_ast,
                ins,epochs,
                orig_log,returnCheck=True,
                print_bool=False):
    ''' Can either return if exit conditions are met or current numerical fitness

    This function first gets the current weights for each fitness function
      (structural and logical) before calculating the overall fitness.
    '''                
    struc_fit,log_fit = returnFitness(epochs)
    logical_result = exhaustiveTest(current_ast,ins)
    if print_bool:
        print('\nEpoch {}'.format(epochs))
        print('Orig logic:    {}'.format(orig_log))
        print('Current logic: {}'.format(logical_result))
    score = 0
    # logical fitness check
    for t in range(len(logical_result)):
        if logical_result[t] == orig_log[t]:
            score += 1
    logical_fitness = log_fit*(score/len(logical_result)) 
    #structural fitness check
    structural_fitness = levenshtein(current_ast,original_ast)
    if structural_fitness > 1:
        structural_fitness = 1
    structural_fitness = struc_fit*structural_fitness

    if returnCheck:
        # By default True. Returns if exit conditions are met or not
        if logical_fitness+structural_fitness >= 1 and logical_fitness / log_fit == 1:
            return False
        else:
            return True
    else:
        # Returns the actual numerical fitness value of the circuit
        return logical_fitness+structural_fitness


def returnFitness(epochs,printBool=False):
    '''
        Returns the new weights for each part of the fitness function
        
    See issue #8
    '''
    startSim = .7
    minSim = .3
    maxEpochs = 1000

    temp = startSim*math.exp(-epochs/maxEpochs)
    if temp <= minSim:
        strucFit = minSim
        logFit = 1-minSim
    else:
        strucFit = temp
        logFit = 1-temp
    if printBool:
        print('Structural Fitness:',strucFit,' and logical fitness:',logFit)
    return strucFit,logFit


def exhaustiveTest(input_ast,ins):
    ''' Returns the exhaustive tested of the AST

    Dynamically tests the AST on its full range of input values
    Returns list of boolean results.
    For a set of inputs like
        ['in1','in2',.....]
      the dynamic testing works like this
        for [False,True] in input_1:
            for [False,True] in input_2:
                ......
      itertools offers a dynamic approach instead of hardcoding like above.
    The input list will change from left to right with all inputs starting
      at False. EX.
        [False,False,....,False]
        [True,False,.....,False]
        [False,True,.....,False]
        [True,True,......,False]
        .....
        [True,True,........True]
    '''

    args = []
    test = []
    # creates list of [False,True] the length of number of inputs
    args = [[False,True] for i in range(len(ins)) ]
    for comb in itertools.product(*args):
        ast = input_ast.copy()
        ins_counter = 0
        for inputs in ins:
            for gate in range(len(ast)):
                if inputs == ast[gate]:
                    # Inserts either True or False into proper input
                    ast[gate] = comb[ins_counter]
            ins_counter += 1
        test.append(returnLogic(ast,ins)) 

    return test


def loadAST(file='verilogInput.v'):
    print('LoadingAST')
    #return ast, inputs


def exhaustiveMutationsCheck(ast,ins,
                            original_ast,epochs,
                            orig_logic):
    ''' Function that checks all possible mutations to a single node

    The highest performing mutation is returned 
    See issue #9

    goes through full AST
      Checks if current node is an input, or binary gate or a solo gate
      Append the full possibility of new node values
    '''
    circuit_test = [ast]
    orig_ast = ast.copy()
    for gate in range(len(ast)):
        ast = orig_ast.copy() # is this line needed?
        if ast[gate] in ins:
            for new_gate in ins:
                # step through all inputs
                ast = orig_ast.copy()
                if new_gate == ast[gate]:
                    # current AST (no change) already appended to the list
                    pass
                else:
                    # append AST with input mutation
                    ast[gate] = new_gate
                    circuit_test.append(ast)
        elif ast[gate] in bin_ops:
            for new_gate in bin_ops:
                # step through all binary operators
                ast = orig_ast.copy()
                if new_gate == ast[gate]:
                    # current AST (no change) already appended to the list
                    pass
                else:
                    # append AST with gate mutation
                    ast[gate] = new_gate
                    circuit_test.append(ast)
        elif ast[gate] in solo_ops:
            for new_gate in solo_ops:
                # step through all solo operators
                ast = orig_ast.copy()
                if new_gate == ast[gate]:
                    # current AST (no change) already appended to the list
                    pass
                else:
                    # append AST with gate mutation
                    ast[gate] = new_gate
                    circuit_test.append(ast)
        else:
            raise Exception
    # checks for best mutated AST. See issue #9
    fit_check = []
    for circuit in circuit_test:
        fit_check.append(checkFitness(circuit,original_ast,ins,epochs,orig_logic,False))
    max_fit_loc = fit_check.index(max(fit_check))
    return circuit_test[max_fit_loc]


def exhaustiveCheck(current_ast,ins,
                    original_ast,epochs,
                    orig_logic,circuit_test=[]):
    ''' HereBOY exhaustive mutation check
    
    This function will check for EVERY possbile:
        Mutation on every node
        Every possbile added node
        Every possbile removed node
      and will return which mutation gives the highest overall fitness

      Returns best mutated AST
    '''
    circuit_test.append(exhaustiveMutationsCheck(current_ast,ins,original_ast,epochs,orig_logic))
    circuit_test += m.check_every_add_node(current_ast,ins)
    circuit_test += m.check_every_remove_node(current_ast,ins)
    # checks for best mutated AST from exhaustive add/remove nodes and best mutated node AST
    fit_check = []
    for circuit in circuit_test:
        fit_check.append(checkFitness(circuit,original_ast,ins,epochs,orig_logic,False))
    max_fit_loc = fit_check.index(max(fit_check))
    return circuit_test[max_fit_loc]


def returnLogic(tempAST,ins):
    ''' Returns the logical function of an AST

    Requires that boolean values are substituted into the AST in place of inputs

    Will search for first two node tree, and will simplify down to single value
    IE, for the following AST
        ['or','and',True,False,False]
              'and',True,False
      will be selected and simplified into False. The AST will now read
        ['or',False,False]
      which can be simplified into a single value. This value is then returned.
    '''
    currentAST = tempAST
    while len(currentAST) > 1:
        currentAST = tempAST
        temp_len = len(currentAST)
        for node in range(temp_len):
            if currentAST[node] in binOps:
                # guesses that the next two nodes in the AST list are the node's children
                children = currentAST[node+1:node+3]
                try:
                    # if children are not gates
                    if type(children[0]) == bool and type(children[1]) == bool:
                        # splits small tree from AST
                        tempStart = currentAST[:node+1]
                        tempEnd = currentAST[node+3:]
                        # preforms logical operation on children
                        tempResult = BinOps(children,currentAST[node])
                        # combines logical result of the tree with old AST
                        tempAST = tempStart  + tempEnd
                        tempAST[node] = tempResult                    
                        break
                except:
                    # error check
                    sys.exit()

            elif currentAST[node] in soloOps:
                child = currentAST[node+1]
                # if child is not a gate
                if type(child) == bool:
                    tempStart = currentAST[:node+1]
                    tempEnd = currentAST[node+2:]
                    # preforms logical operation
                    tempResult = SoloOps(child,currentAST[node])
                    # combines logical result with AST
                    tempAST = tempStart  + tempEnd
                    tempAST[node] = tempResult
                    break
    return currentAST


def randomExhaustive(current_ast,ins,
                    original_ast,epochs,
                    orig_logic,print_bool=False):
    ''' Returns a stochastically selected mutated AST

    See issue #6
    '''
    num_mut = random.randint(0,1000)
    if num_mut < 800: # 80%
        if print_bool: print('\nexhaustive mut check')
        current_ast = exhaustiveMutationsCheck(current_ast,ins,original_ast,epochs,orig_logic)
    elif num_mut < 900: # 10%
        if print_bool: print('\nRandom Mutation')
        current_ast = m.randomMutate(current_ast,ins)
    elif num_mut < 910: # 1%
        if print_bool: print('\nAdd a randoom node')
        current_ast = m.addNode(current_ast,ins)
    elif num_mut < 920: # 1%
        if print_bool: print('\nRemove a random node')
        current_ast = m.removeNode(current_ast,ins)
    #elif num_mut < 970: # 5%
    #    if print_bool: print('\nCrossover a random node')
    #    current_ast = m.crossover(current_ast,ins)
    else: # 3%
        pass
    return current_ast


def createRandomAST(ins, min_ast_depth=3,
                    max_ast_depth=6, ast=None,
                    gates=bin_ops + solo_ops):
    '''
        Recursive function which adds new gates to AST.
        depth: set number of layers in the AST
        gates: list containing possible gates, both binary and singular ops
        current_depth: current depth of AST creation
        ast: list of nodes resembled as strings
        current_loc: current location in the ast
    '''
    if ast == None:
        # creates a randomly ast od depth 1
        random_gate = gates[random.randint(0,len(gates)-1)]
        if random_gate in solo_ops:
            ast.append(random_gate)
            ast.append(ins[random.randint(0,len(ins)-1)])
        else:
            ast.append(random_gate)
            ast.append(ins[random.randint(0,len(ins)-1)])
            ast.append(ins[random.randint(0,len(ins)-1)])
    # adds depth to the tree
    depth = random.randint(min_ast_depth,max_ast_depth)
    for _ in range(depth):
        ast = m.addNode(ast,ins)
    return ast


def addRandomness(ast,ins,num_muts=10):
    ''' Takes an AST and preforms num_muts number of mutations, to try and 
        add initial randomness to the AST.

    See issue #11
    
    Returns AST with random mutation 
    '''
    for _ in range(num_muts):
        # 50/50 chance it adds nodes or mutates nodes
        num_mut = random.randint(0,1)
        if num_mut == 0:
            ast = m.addNode(ast,ins)
        elif num_mut == 1:
            ast = m.randomMutate(ast,ins)
    return ast

############# Data Functions  #############
def BinOps(children,l):
    if l == 'or':
        return children[0] or children[1]
    elif l == 'and':
        return children[0] and children[1]
    elif l == 'nand':
        return not (children[0] and children[1])

def SoloOps(child,l):
    if l == 'not':
        return not child
###########################################

def params_test(
        total_success = 0,
        num_runs = 0,
        max_epochs = 1000,
        original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],
        ins = ['I0','I1','Sel']):

    for rand in range(1,20):
        lev_total = []
        average_epochs = []
        total_success = 0
        num_runs = 0
        for _ in range(100):
            
            current_ast = original_ast.copy()
            orig_logic = exhaustiveTest(original_ast,ins)
            current_ast = addRandomness(current_ast,ins,rand)
            epochs = 0

            while epochs < max_epochs and checkFitness(current_ast,original_ast,ins,epochs,orig_logic):
                current_ast = randomExhaustive(current_ast,ins,original_ast,epochs,orig_logic)
                epochs +=1

            logic2 = exhaustiveTest(current_ast,ins)
            num_runs += 1
            if orig_logic == logic2:
                total_success += 1
            
            average_epochs.append(epochs)
            lev_total.append(levenshtein(original_ast,current_ast))

        print('\nAverage lev distance for {} initial randoms muts: {}'.format(
            sum(lev_total)/len(lev_total),rand))
        print('Number of hits: {}'.format(total_success/num_runs))
        print('Average number of epochs needed: {}'.format(
            sum(average_epochs)/len(average_epochs)))


def normal_dv(
    original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],
    ins = ['I0','I1','Sel']
    ):
    
    orig_logic = exhaustiveTest(original_ast,ins)
    current_ast = original_ast.copy()
    
    #current_ast = createRandomAST(ins)
    current_ast = addRandomness(current_ast,ins)
    print(original_ast)
    print(current_ast)
    treePrint(original_ast,binOps,soloOps,'temp/Original_AST.gv')
    treePrint(current_ast,binOps,soloOps,'temp/Starting_AST.gv')

    max_epochs = 1000
    epochs = 0
    same_count = 0
    same_count_max = 3

    start = time.time()
    while epochs < max_epochs and checkFitness(current_ast,original_ast,ins,epochs,orig_logic):
        '''
        if epochs % 50 == 0:
            print('Epoch:',epochs,' Current Fitness:',fit)
            print('Current AST is: ',current_ast)
        '''
        print('Epoch: {} Current Fitness: {}'.format(epochs,
            checkFitness(current_ast,original_ast,ins,epochs,orig_logic,False)))
        print('Current AST is: ',current_ast)
        past_ast = current_ast.copy()
        current_ast = exhaustiveCheck(current_ast,ins,original_ast,epochs,orig_logic)  #exhaustiveMutationsCheck(current_ast,ins,original_ast,epochs,orig_logic)
        
        if past_ast == current_ast:
            same_count += 1
        else:
            same_count = 0
        
        if same_count > same_count_max:
            current_ast = m.randomMutation(current_ast,ins)
            same_count = 0
        

        print('Mutated AST is: ',current_ast)
        epochs +=1
    end = time.time()
    
    logic2 = exhaustiveTest(current_ast,ins)
    

    print('\nOriginal AST: ',original_ast)
    print('Final AST is: ',current_ast)
    print('\nNumber of epochs ran {}'.format(epochs))
    print('Final fitness: {:0.4f}'.format(
            checkFitness(current_ast,original_ast,ins,epochs,orig_logic,False)))
    print('Run time: {:0.4f}\n'.format(end-start))
    print(list(zip(orig_logic,logic2)))
    treePrint(current_ast,binOps,soloOps,'temp/Final_AST.gv')



def main():
    normal_dv()


if __name__ == "__main__":
    main()