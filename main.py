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
    
def print_node_value(value):
    print(value)

def visit(node, handle_node):
    handle_node(node.value)
    for child in node.children:
        visit(child, handle_node)

def addNode(tree,node):
    tree.children.append(Node(node))



in1 = None
in2 = None
'''
AST = ['and',in1,'not',in2,'and',in2,'not',in1]
tree = Node('or')

for a in AST:
    addNode(tree,a)
'''
tree = Node('or')
tree.children.append(Node('\tand'))
tree.children.append(Node('\tand'))
tree.children[0].children.append(Node('\t\tin1'))
tree.children[0].children.append(Node('\t\tnot'))
tree.children[0].children[1].children.append(Node('\t\t\tin2'))
tree.children[1].children.append(Node('\t\tin2'))
tree.children[1].children.append(Node('\t\tnot'))
tree.children[1].children[1].children.append(Node('\t\t\tin1'))

#visit(tree, print_node_value)


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


thing(tree)
