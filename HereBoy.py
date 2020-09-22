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
    with open('Logical_Fitness.pkl','rb') as f:
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

def exhaustiveTest(astList,ins):
    '''
        Need to set up for dynamic execution
    '''
    test = []
    for in1 in [False,True]:
        for in2 in [False,True]:
            for in3 in [False,True]:
                ast = list(astList)
                for l in range(len(ast)):
                    #print(ast[l])
                    if ast[l] == 'I0':
                        ast[l] = in1
                    elif ast[l] == 'I1':
                        ast[l] = in2
                    elif ast[l] == 'Sel':
                        ast[l] = in3
                #print('Here is the AST',ast)
                tree = HereBoy(ast,ins)
                #test.append(('A:',in1,'B:',in2,'result',tree.returnLogic(ast[0],0)))
                test.append(tree.returnLogic(ast[0],0))
    '''
    for in1 in [False,True]:
        for in2 in [False,True]:
            ast = list(astList)
            for l in range(len(ast)):
                if ast[l] == 'A':
                    ast[l] = in1
                elif ast[l] == 'B':
                    ast[l] = in2
            #print('Here is the AST',ast)
            tree = HereBoy(list(ast),ins)
            #test.append(('A:',in1,'B:',in2,'result',tree.returnLogic(ast[0],0)))
            test.append(tree.returnLogic(ast[0],0))
    '''
    return test


def checkFinished(ast,ins,epochs):
    with open('Logical_Fitness.pkl','rb') as f:
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
    print('Hey its the main!')
    '''
    #original_ast = ('or','and','A','B','and','B','A')
    original_ast = ('or','A','B')
    current_ast = list(original_ast)
    ins = ['A','B']
    
    # Mux
    '''
    original_ast = ('nand','nand','I0','Sel','nand','I1','nand','Sel','Sel')
    current_ast = list(original_ast)
    ins = ['I0','I1','Sel']

    '''
    original_ast = ('or','in1','in2')
    current_ast = list(original_ast)
    ins = ['in1','in2']
    '''

    
    treePrint(current_ast,binOps,soloOps,'Original_AST.gv')
    
    logic = exhaustiveTest(original_ast,ins)
    print(logic)
    with open('Logical_Fitness.pkl','wb') as f:
        pkl.dump(logic,f)
    #print('Base logic',logic)
    
    fit = 0
    max_epochs = 1000
    epochs = 0
    while epochs < max_epochs and (fit != 1 or checkFinished(current_ast,ins,epochs)) :
        #print('Epoch',epochs)
        
        results = m.mutate(current_ast,ins)
        fit_check = []
        for current_ast in results:
            fit_check.append(checkFitness(current_ast,original_ast,ins,epochs))
        max_fit_loc = fit_check.index(max(fit_check))
        current_ast = results[max_fit_loc]
        fit = max(fit_check)
        
        #urrent_ast = m.randomMutation(current_ast,ins)
        #returnFitness(epochs,True)
        print('Current AST is: ',current_ast)
        fit = checkFitness(current_ast,original_ast,ins,epochs)
        print('Epoch:',epochs,' Current Fitness:',fit)
        epochs +=1

    logic2 = exhaustiveTest(current_ast,ins)
    print(list(zip(logic,logic2)))
    treePrint(current_ast,binOps,soloOps)

if __name__ == "__main__":
    main()