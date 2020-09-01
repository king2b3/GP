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

AND, OR, NOT, INPUT, OUTPUT, LPAREN, RPAREN, EOF = (
    'AND', 'OR', 'NOT', 'INPUT', 'OUTPUT', '(', ')', 'EOF'
)

class AST(object):
    # container for AST
    pass

class BinOp(AST):
    # Binary OP class
    def __init__(self,val,left,right):
        self.value = val
        self.left = left
        self.right = right

class SoloOp(AST):
    def __init__(self,val,left):
        self.value = val
        self.child = left

class Input(AST):
    def __init__(self,val):
        self.value = val

class Output(AST):
    def __init__(self,val):
        self.value = val


class Parser(object):
    def __init__(self,lexer):
        self.lexer = lexer
        self.originalLexer = lexer
        self.current_token = lexer[0]
        # lexer is the original list of the AST
    
    def error(self):
        raise Exception('Invalid operator in AST')

    def print(self):
        print("Current AST",self.lexer)
        print("Original AST",self.originalLexer)

    def eat(self,token_type):
        if type(self.current_token) == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        token = self.current_token
        if token.type == INPUT:
            self.eat(INPUT)
            return Input(token)

    def expr(self):
        node = self.factor()

        while self.current_token.type in (AND,OR):
            token = self.current_token
            if token.type == AND:
                self.eat(AND)
            elif token.type == OR:
                self.eat(OR)

            node = BinOp(left=node, val=token, right=self.factor())

        while self.current_token.type in (NOT):
            token = self.current_token
            if token.type == NOT:
                self.eat(NOT)
            
            node = SoloOp(left=node, val=token)
        
        return node

########################################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Interpreter(NodeVisitor):
    def __init__(self,parser):
        self.parser = parser
    
    def visitBinOp(self,node):
        if node.op.type == OR:
            return self.visit(node.left) or self.visit(node.right)
        if node.op.type == AND:
            return self.visit(node.left) and self.visit(node.right)

    def visitSoloOP(self,node):
        if node.op.type == NOT:
            return not self.visit(node.left) 

    def visitNum(self,node):
        return node.value


'''
class Interpreter():
    def __init__(self,lex):
        


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

'''

def main():

    a = Op('or','in1','in2')
    if type(a) == Op:
        print(type(a))

if __name__ == '__main__':
    main()