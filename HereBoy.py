#   Python 3.7.3
#   Bayley King
#   University of Cincinnati MIND Lab
'''
    General container file for GP system using here boy algorithm.
    Takes in from mutations.py, lexer.py, stringComp.py and exhaustiveTest.py.
    
'''
import StringComp 
#from exhaustiveTest import exhaustiveTest
#from mutations import mutations

class HereBoy:
    def __init__(self,ast,inputs):
        self.origAST = self.currentAST = ast
        self.inputs = inputs
        
        #self.m = mutations.mutations()
        self.strCmp = StringComp.StringComp()
        #self.exhTest = exhaustiveTest.exhaustiveTest()
        '''
            If these inits are the same as whats needed in the other file,
            inheritance would work very nicely.

            Lets keep everything local to this class, and let the other classes
            be the data handeling classes.
        '''
    def outputResults(self):
        print('saving results')


def changeFitness(w,epochs):
    '''
        Returns the new weights for each part of the fitness function

    '''
    print('Changing Fitness')


def loadAST(file='verilogInput.v'):
    print('LoadingAST')
    #return ast, inputs



def main():
    print('Hey its the main!')

if __name__ == "__main__":
    main()