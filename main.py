import numpy as numpy
from mutations import *
'''
class dTree:

    def __init__(self):
        self.ast = "Or(And(self.ins[0],Not(self.ins[1])),And(self.ins[1],Not(self.ins[0])))"
        self.gates = ['or','and','in1','not','in2','and','in2','not','in1']
        self.ins = ['in1','in2']
        self.outs = ['ou1']

#   Test file not to be pushed
'''
from mutations import *
class Node:
    def __init__(self,val):
        self.value = val
        self.children = []


def printTree(tree,counter = True):    
    func = getattr(tree, "children", None)
    print(tree.value)#,' ',func)
    if func:
        for node in func:
            if node.children != []:
                printTree(node)
            else:
                print(node.value)


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

    return tree

def addNode(var,node,layer):
    #t = tab(layer)
    var.children.append(Node(tab(layer)+node))
    return var

def tab(num):
    t = '\t'
    for i in range(num-1):
        t += '\t'
    return t

def printTreeTest(val,ast,counter = True):    
    func = getattr(val, "children", None)
    ast.append(val.value)#,' ',func)
    if func:
        for node in func:
            if node.children != []:
                printTree(node)
            else:
                ast.append(node.value)
    return ast


AST = ['or','and','not','in1','in2','and','not','in2','in1','and','and','in1','in2','in1']
Ins = ['in2','in2']
ast = []
#print(AST)
tree = genAST(AST,Ins)
ast = printTreeTest(tree,ast)
new_ast = []
for gate in ast:
    new_ast.append(gate.strip('\t'))
print(new_ast)
new_ast = tuple(new_ast)


def genFit(ast):
    counter = 0
    for gate in ast:
        children = addGate(ast,gate,counter)
        if children:
            for child in children:
                if child == 'or' or gate == 'and' or 'not':
                    sub_children = addGate(ast,gate,counter)



def addGate(ast,gate,counter):
    if gate == 'or' or gate == 'and':
        return(ast[counter+1:counter+2])
    elif gate == 'not':
        return(ast[counter+1])
    else:
        return False