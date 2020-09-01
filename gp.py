#   Genetic Programming Framework
#   Python 3.7
#   Bayley King

from lexerTry import AST
import random

ops = ['or','and','not']

class hereBoy(object):
    def __init__(self,ogAST,inputs):
        self.originalAST = ogAST
        self.currentAST = ogAST
        self.numGens = self.numMutations = 0
        self.ast = AST(ogAST,inputs)
        self.inputs = inputs
        #self.bestFitness = self.currentFitness = self.funcTest(self.currentAST[0],0)

    def mutate(self):
        results = []
        for m in [self.randomMutate(),self.crossover(),self.addNode(),self.removeNode()]:
            results.append([m,str(m)])
        return results

    ######### Mutations #########

    def randomMutate(self):
        gate = random.randint(0,len(self.currentAST)-1)
        tempAST = list(self.currentAST)
        if self.currentAST[gate] == 'or':
            tempAST[gate] = 'and'
        elif self.currentAST[gate] == 'and':
            tempAST[gate] = 'or'
        elif self.currentAST[gate] in self.inputs:
            ranIn = random.randint(0,1)
            while self.inputs[ranIn] == self.currentAST[gate]:
                ranIn = random.randint(0,1)
            tempAST[gate] = self.inputs[ranIn]
        return tempAST       


    def crossover(self):
        tempAST = list(self.currentAST)
        gate = random.randint(0,len(self.currentAST)-1)
        gateCross = random.randint(0,len(self.currentAST)-1)
        while self.currentAST[gate] in self.inputs or self.hasChildren(self.currentAST,gate):
            gate = random.randint(0,len(self.currentAST)-1)
        while self.currentAST[gateCross] in self.inputs or gateCross == gate or self.hasChildren(self.currentAST,gateCross):
            gateCross = random.randint(0,len(self.currentAST)-1)
        #print('First Gate is:',gateCross,'Second Gate is:',gate)

        if gate > gateCross:
            g1 = gateCross
            g2 = gate
        else:
            g1 = gate
            g2 = gateCross

        start = tempAST[:g1]
        cross1 = tempAST[g1:g1+3]
        middle = tempAST[g1+3:g2]
        cross2 = tempAST[g2:g2+3]
        end = tempAST[g2+3:]

        tree = start+cross2+middle+cross1+end
        return tree

    def addNode(self):
        gate = random.randint(0,len(self.currentAST)-1)
        while self.currentAST[gate] in ops or self.isLeaf(self.currentAST,gate):
            gate = random.randint(0,len(self.currentAST)-1)
        tempAST = list(self.currentAST)
        tempStart = tempAST[:gate]
        tempEnd = tempAST[gate+1:]

        newNode = []
        gate = random.randint(0,len(ops)-1)
        if gate == 0:
            newNode.append('and')
        else:
            newNode.append('or')
        
        gate1 = random.randint(0,len(self.inputs)-1)
        gate2 = random.randint(0,len(self.inputs)-1)
        while gate1 == gate2:
            gate2 = random.randint(0,len(self.inputs)-1)
        newNode.append(self.inputs[gate1])
        newNode.append(self.inputs[gate2])

        return tempStart+newNode+tempEnd


    def removeNode(self):
        gate = random.randint(0,len(self.currentAST)-1)
        while self.currentAST[gate] in self.inputs or self.isLeaf(self.currentAST,gate):
            gate = random.randint(0,len(self.currentAST)-1)
        
        tree = list(self.currentAST)
        start = tree[:gate]
        middle = tree[gate:gate+3]
        end = tree[gate+3:]

        return start+end


    def hasChildren(self,tree,gate):
        try:
            children = tree[gate+1:gate+3]
            if children[0] in ops or children[1] in ops:
                return True
            else:
                return False
        except:
            return False
    
    def isLeaf(self,tree,gate):
        if tree[gate-1] in ops and tree[gate+1] in self.inputs:
            return False
        else:
            return True
    
    
    def error(self):
        raise Exception('Invalid operator in AST')

    def __str__(self):
        return self.currentAST


def main():
    ast = ('or','and','A','B','and','B','A')
    Ins = ['A','B']
    test = hereBoy(ast,Ins)
    results = test.mutate()
    print(ast)
    #print(results)
    for r in results:
        print(r[0])

if __name__ == '__main__':
    main()