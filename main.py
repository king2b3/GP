import numpy as numpy
from mutations import *

class dTree:

    def __init__(self):
        self.ast = "Or(And(self.ins[0],Not(self.ins[1])),And(self.ins[1],Not(self.ins[0])))"
        self.gates = ['or','and','in1','not','in2','and','in2','not','in1']
        self.ins = ['in1','in2']
        self.outs = ['ou1']

class Node:
    def __init__(self,val):
        self.value = val
        self.children = []
'''    
def print_node_value(value):
    print(value)

def visit(node, handle_node):
    handle_node(node.value)
    for child in node.children:
        visit(child, handle_node)

def addNode(tree,node):
    tree.children.append(Node(node))
'''
def thing(val,counter = True):
    if counter:
        print(val.value)
        counter = False
    func = getattr(val, "children", None)
    if func:
        for node in val.children:
            if node.children != []:
                thing(node)
            else:
                print(node.value)

def genAST(ASTlist,counter = 0,layer = 0,nodeC = 0):
    for A in ASTlist:
        if layer == 0:                    # init 
            tree = Node(A)
            layer += 1

        elif layer == 1:  # 2nd layer
            tab = '\t'
            tree.children.append(Node(tab+A))
            tab += '\t'
            layer += 1
            counter += 1
            c = 0

        elif layer == 2:
            if c > 1:
                nodeC = 1
            tree.children[nodeC].children.append(Node(tab+A))
            if A == 'not':
                layer += 1
            c += 1

        elif layer == 3:
            tree.children[nodeC].children[1].children.append(Node('\t'+tab+A))
            layer -= 2

    return tree


def addLayer(layer,val):
    print()

#set way for 3 layers, init, middle, end layer

AST = ['or','and','in1','not','in2','and','in2','not','in1']

tree = genAST(AST)

thing(tree)