#   Test file not to be pushed
from mutations import *
'''
def testFitness():
    
    score = 0
    a = ['in1','in2','in3','in4']
    b = [0,1]
    fit = p.loadFit("setFitness.txt")
    counter = 0
    b = [0,1]

    for in1 in b:
        for in2 in b:
            a = ( Or(And(in1,Not(in2)),And(in2,Not(in1))) )
            print(int(a))

testFitness()

'''


def visit_Import(self, node):
    for alias in node.names:
        self.stats["import"].append(alias.name)
    self.generic_visit(node)

def visit_ImportFrom(self, node):
    for alias in node.names:
        self.stats["from"].append(alias.name)
    self.generic_visit(node)

import ast
from pprint import pprint


def main():
    with open("ast_example.py", "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()


class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {"import": [], "from": []}

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["import"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["from"].append(alias.name)
        self.generic_visit(node)

    def report(self):
        pprint(self.stats)


if __name__ == "__main__":
    main()

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

tree = Node('A')
tree.children.append(Node('B'))
tree.children.append(Node('C'))

visit(tree, print_node_value)

#analyzer = Analyzer()
#analyzer.visit(tree)