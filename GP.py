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
        
    def exhaustiveTest(self):
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
            ast = self.current_ast.copy()
            ins_counter = 0
            for inputs in self.ins:
                for gate in range(len(ast)):
                    if inputs == ast[gate]:
                        # Inserts either True or False into proper input
                        ast[gate] = comb[ins_counter]
                ins_counter += 1
            test.append(returnLogic(ast,self.ins)) 

        return test

