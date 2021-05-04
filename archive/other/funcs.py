from mutations import *
import ast

ast = []

twoTermGate = ['and','or']
oneTermGate = ['not']

def fitness(in1,in2): 
    return ( Or(And(in1,Not(in2)),And(in2,Not(in1))) )

def genFunction(circuit,in1,in2):
    counter = 0
    for gate in circuit:
        if gate in twoTermGate:
            children = circuit[counter+1:counter+2]
        
def printTree(val,counter = True):    
    func = getattr(val, "children", None)
    ast.append(val.value)#,' ',func)
    if func:
        for node in func:
            if node.children != []:
                printTree(node)
            else:
                ast.append(node.value)


def loadFit(File):
    import numpy as np
    import csv
    #path = 'SavedWeights/'+File
    dataFile = open(File)
    lines = dataFile.readlines()
    dataFile.close()
    lines = [int(i) for i in lines]
    return lines

def testFitness():
    score = 0
    a = ['in1','in2','in3','in4']
    b = [0,1]
    fit = loadFit("setFitness.txt")
    counter = 0

    for in1 in b:
        for in2 in b:
            a = fitness(in1,in2)
            if a == fit[counter]:
                score += 1
            counter += 1

    print('Final score is: ',score/counter)

def genAST(ASTlist,Ins,counter = 0,layer = 0,level=0):
    for A in ASTlist:
        #print('Val in AST ',A,' in layer ',layer,' with level ',level)
        
        if level == 0: # Init Layer
            tree = Node(A)
            layer += 1
            level += 1
            c = 0

        elif level == 1: # Middle layers
            tree = addNode(tree,A,layer)
            if A == 'or' or A == 'and':
                layer += 1
                c = 0
            elif A == 'not':
                layer += 1
                level += 1
                c += 1
            else:
                c += 1
                if c > 1:
                    layer -= 1
                    c = 0

        elif level == 2: # Bottom Layer
            tree = addNode(tree,A,layer)
            layer -= 1
            level -= 1


'''
def createRandomTree(size,inputs):
    tree = []
    for layer in range(size):


    

    return tree
'''

#   Test file not to be pushed
from mutations import *
class Node:
    def __init__(self,val):
        self.value = val
        self.children = []

def addNode(var,node,layer):
    #t = tab(layer)
    var.children.append(Node(tab(layer)+node))
    return var

def tab(num):
    t = '\t'
    for i in range(num-1):
        t += '\t'
    return t

AST =    ['or','and','not','in1','in2','and','not','in2','in1','and','and','in1','in2','in1']
Ins = ['in2','in2']
#testFitness()
#tree = genAST(AST,Ins)
printTree(tree)
print(ast)