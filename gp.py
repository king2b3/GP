#   Genetic Programming Framework
#   Python 3.7
#   Bayley King

from lexerTry import AST

class hereBoy(object):
    def __init__(self,ogAST,inputs):
        self.originalAST = ogAST
        self.currentAST = list(ogAST)
        self.numGens = self.numMutations = 0
        ast = AST(ogAST,inputs)
        self.bestFitness = self.currentFitness = ast.funcTest(self.currentAST[0],0)

    def mutate(self):
        # dirty implemntation 
    
    
    def error(self):
        raise Exception('Invalid operator in AST')

    def __str__(self):
        return self.currentAST


