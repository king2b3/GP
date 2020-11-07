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


def checkFitness(current_ast,original_ast,ins,epochs):
    struc_fit,log_fit = returnFitness(epochs)
    with open('outputs/Logical_Fitness.pkl','rb') as f:
        orig_log = pkl.load(f)
    #print(current_ast)
    logical_result = exhaustiveTest(current_ast,ins)
    score = 0
    for t in range(len(logical_result)):
        if logical_result[t] == orig_log[t]:
            score += 1
    logical_fitness = log_fit*(score/len(logical_result)) 

    structural_fitness = levenshtein(current_ast,original_ast)
    if structural_fitness > 1:
        structural_fitness = 1
    structural_fitness = struc_fit*structural_fitness


    return logical_fitness+structural_fitness
    #return score/len(logical_result)


def returnFitness(epochs,printBool=False):
    '''
        Returns the new weights for each part of the fitness function
        Need to set up better system for inputting set values.
          Use second file? I like using that at least.
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
    #print('Changing Fitness')
    if printBool:
        print('Structural Fitness:',strucFit,' and logical fitness:',logFit)
    return strucFit,logFit


def exhaustiveTest(input_ast,ins):

    args = []
    test = []
    args = [[False,True] for i in range(len(ins)) ]
    for comb in itertools.product(*args):
        ast = input_ast.copy()
        ins_counter = 0
        for inputs in ins:
            for gate in range(len(ast)):
                if inputs == ast[gate]:
                    ast[gate] = comb[ins_counter]
            ins_counter += 1
        test.append(returnLogic(ast,ins)) 

    return test


def checkFinished(ast,ins,epochs):
    with open('outputs/Logical_Fitness.pkl','rb') as f:
        orig_log = pkl.load(f)
    logical_result = exhaustiveTest(ast,ins)
    score = 0
    for t in range(len(logical_result)):
        if logical_result[t] == orig_log[t]:
            score += 1
    logical_fitness = (score/len(logical_result))
    print(logical_fitness)
    if logical_fitness >= 1 and epochs != 0:
        print('here')
        return False
    else:
        return True


def loadAST(file='verilogInput.v'):
    print('LoadingAST')
    #return ast, inputs


def exhaustiveMutationsCheck(ast,ins,original_ast,epochs):
    circuit_test = [ast]
    orig_ast = tuple(ast)
    for gate in range(len(ast)):
        ast = list(orig_ast)
        if ast[gate] in ins:
            for new_gate in ins:
                ast = list(orig_ast)
                if new_gate == ast[gate]:
                    pass
                else:
                    ast[gate] = new_gate
                    circuit_test.append(ast)
        elif ast[gate] in bin_ops:
            for new_gate in bin_ops:
                ast = list(orig_ast)
                if new_gate == ast[gate]:
                    pass
                else:
                    ast[gate] = new_gate
                    circuit_test.append(ast)
        elif ast[gate] in solo_ops:
            for new_gate in solo_ops:
                ast = list(orig_ast)
                if new_gate == ast[gate]:
                    pass
                else:
                    ast[gate] = new_gate
                    circuit_test.append(ast)
        else:
            raise Exception

    fit_check = []
    for circuit in circuit_test:
        fit_check.append(checkFitness(circuit,original_ast,ins,epochs))
    max_fit_loc = fit_check.index(max(fit_check))
    return circuit_test[max_fit_loc]

'''
def exhaustiveCheck(ast,ins,original_ast,epochs):
    circuit_test.append(exhaustiveMutationsCheck(ast,ins,original_ast,epochs))
    for node in range(len(ast)):
        try:
            circuit_test.append(m.addNode(ast,ins))
        except:
            
    fit_check = []
    for circuit in circuit_test:
        fit_check.append(checkFitness(circuit,original_ast,ins,epochs))
    max_fit_loc = fit_check.index(max(fit_check))
    return circuit_test[max_fit_loc]
'''


def returnLogic(tempAST,ins):
    currentAST = tempAST
    while len(currentAST) > 1:
        currentAST = tempAST
        temp_len = len(currentAST)
        for node in range(temp_len):
            if currentAST[node] in binOps:
                children = currentAST[node+1:node+3]
                if type(children[0]) == bool and type(children[1]) == bool:
                    tempStart = currentAST[:node+1]
                    tempEnd = currentAST[node+3:]
                    tempResult = BinOps(children,currentAST[node])
                    tempAST = tempStart  + tempEnd
                    tempAST[node] = tempResult                    
                    break
            elif currentAST[node] in soloOps:
                child = currentAST[node+1]
                if type(child) == bool:
                    tempStart = currentAST[:node+1]
                    tempEnd = currentAST[node+2:]
                    tempResult = SoloOps(child,currentAST[node])
                    tempAST = tempStart  + tempEnd
                    tempAST[node] = tempResult
                    break
    return currentAST


def randomExhaustive(current_ast,ins,original_ast,epochs):
    num_mut = random.randint(0,1000)
    if num_mut < 800: # 80%
        current_ast = exhaustiveMutationsCheck(current_ast,ins,original_ast,epochs)
    elif num_mut < 900: # 10%
        current_ast = m.randomMutate(current_ast,ins)
    elif num_mut < 910: # 1%
        current_ast = m.addNode(current_ast,ins)
    elif num_mut < 920: # 1%
        current_ast = m.removeNode(current_ast,ins)
    elif num_mut < 970: # 5%
        current_ast = m.crossover(current_ast,ins)
    else: # 3%
        pass
    return current_ast

'''
def bestOfSetMutations(current_ast,ins):
    results = m.mutate(current_ast,ins)
    fit_check = []
    for current_ast in results:
        fit_check.append(checkFitness(current_ast,original_ast,ins,epochs))
    max_fit_loc = fit_check.index(max(fit_check))
    return results[max_fit_loc]
'''

def insertRandomOp(depth,ins,gates,ast=[]):
    '''
        Recursive function which adds new gates to AST.
        depth: set number of layers in the AST
        gates: list containing possible gates, both binary and singular ops
        current_depth: current depth of AST creation
        ast: list of nodes resembled as strings
        current_loc: current location in the ast
    '''
    random_gate = gates[random.randint(0,len(gates)-1)]
    if random_gate in solo_ops:
        ast.append(random_gate)
        ast.append(ins[random.randint(0,len(ins)-1)])
    else:
        ast.append(random_gate)
        ast.append(ins[random.randint(0,len(ins)-1)])
        ast.append(ins[random.randint(0,len(ins)-1)])
    for _ in range(depth):
        ast = m.addNode(ast,ins)
    return ast


def createRandomAST(ins,min_ast_depth=3,max_ast_depth=6):
    '''
        calls insertRandomOp function, which will return a randomly generated AST
        ins: list of inputs
        min_ast_depth: min number of layers in new AST. default 3
        max_ast_depth: max number of layers in new AST default 6
    '''
    return insertRandomOp(random.randint(min_ast_depth,max_ast_depth),ins,bin_ops + solo_ops)

def addRandomness(ast,ins,num_muts=10):
    '''
        Takes an AST and preforms num_muts number of mutations, to try and 
        add initial randomness to the AST.
    '''
    for _ in range(num_muts):
        num_mut = random.randint(0,2)
        if num_mut == 0:
            ast = m.addNode(ast,ins)
        elif num_mut == 1:
            ast = m.randomMutate(ast,ins)
        elif num_mut == 2:
            ast = m.crossover(ast,ins)
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

def main():

    '''
    #original_ast = ('or','and','A','B','and','B','A')
    original_ast = ('or','A','B')
    current_ast = list(original_ast)
    ins = ['A','B']
    '''
    
    # Mux
    
    original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel']
    current_ast = original_ast.copy()
    ins = ['I0','I1','Sel']
    
    logic = exhaustiveTest(original_ast,ins)
    #print(logic)
    with open('outputs/Logical_Fitness.pkl','wb') as f:
        pkl.dump(logic,f)
    #print('Base logic',logic)
    
    #current_ast = createRandomAST(ins)
    current_ast = addRandomness(current_ast,ins)
    treePrint(current_ast,binOps,soloOps,'Original_AST.gv')
    print('original ast',original_ast)
    print('starting ast',current_ast)
    fit = 0
    max_epochs = 100
    epochs = 0
    mutations_time = []
    fitness_time = []
    start = time.time()
    while epochs < max_epochs and (fit != 1) and checkFinished(current_ast,ins,epochs):
        '''
        if epochs % 50 == 0:
            print('Epoch:',epochs,' Current Fitness:',fit)
            print('Current AST is: ',current_ast)
        '''
        print('\nEpoch:',epochs,' Current Fitness:',fit)
        print('Current AST is: ',current_ast)
        
        # Exhaustive Mutation checking
        #for gate in current_ast:

        mutation_start = time.time()
        current_ast = exhaustiveMutationsCheck(current_ast,ins,original_ast,epochs)
        mutation_end = time.time()
        print('Mutated AST is: ',current_ast)

        fitness_start = time.time()
        fit = checkFitness(current_ast,original_ast,ins,epochs)
        fitness_end = time.time()

        mutations_time.append(mutation_end - mutation_start)
        fitness_time.append(fitness_end - fitness_start)

        epochs +=1
    end = time.time()
    logic2 = exhaustiveTest(current_ast,ins)
    print('Final AST is: ',current_ast)
    print('Original AST  : ',original_ast)
    print('Time for mutations to run: ',end-start)
    print('Final fitness: ',fit)
    print(list(zip(logic,logic2)))
    treePrint(current_ast,binOps,soloOps,'Final_AST.gv')
    #treePrint(current_ast,binOps,soloOps)
    with open('outputs/mutations_time.pkl','wb') as f:
        pkl.dump(mutations_time,f)
    with open('outputs/fitness_time.pkl','wb') as f:
        pkl.dump(fitness_time,f)

if __name__ == "__main__":
    main()