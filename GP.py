#   Overall GP container 
#   Bayley King
#   20 November 2020
#   Python 3.8

from itertools import product
from operations import returnLogic
import sys

class GP:
    def __init__(self,ast,inputs,
                 max_epochs):

        self.original_ast = ast.copy()
        self.current_ast = ast.copy()
        self.ins = inputs
        self.max_epochs = max_epochs
        # preform original logic in init
        self.orig_log = self.exhaustiveTest(ast)
        
    def exhaustiveTest(self,current_ast):
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
        args = [[False,True] for i in range(len(self.ins)) ]
        for comb in product(*args):
            ast = current_ast.copy()
            ins_counter = 0
            for inputs in self.ins:
                for gate in range(len(ast)):
                    if inputs == ast[gate]:
                        # Inserts either True or False into proper input
                        ast[gate] = comb[ins_counter]
                ins_counter += 1
            test.append(returnLogic(ast,self.ins)) 

        return test


    def createRandomAST(
        self, min_ast_depth=3,
        max_ast_depth=6, ast=None
    ):
        '''
            Recursive function which adds new gates to AST.
            depth: set number of layers in the AST
            gates: list containing possible gates, both binary and singular ops
            current_depth: current depth of AST creation
            ast: list of nodes resembled as strings
            current_loc: current location in the ast
        '''
        
        # creates a randomly ast of depth 1
        random_gate = op.randomGate()
        ast= []
        if random_gate in op.solo_operators:
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
        self.current_ast = ast


    def addRandomness(
        self,num_muts=10
    ):
        ''' Takes an AST and preforms num_muts number of mutations, to try and 
            add initial randomness to the AST.

        See issue #11
        
        Returns AST with random mutation 
        '''
        for _ in range(num_muts):
            # 50/50 chance it adds nodes or mutates nodes
            num_mut = random.randint(0,1)
            if num_mut == 0:
                self.current_ast = m.addNode(self.current_ast,self.ins)
            elif num_mut == 1:
                self.current_ast = m.randomMutate(self.current_ast,self.ins)