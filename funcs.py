from mutations import *


def fitness(in1,in2): 
    return ( Or(And(in1,Not(in2)),And(in2,Not(in1))) )

#print(fitness(True,True,False,True))

#print(And(Or(True,False),False))

def loadFit(File):
    import numpy as np
    import csv
    #path = 'SavedWeights/'+File
    dataFile = open(File)
    lines = dataFile.readlines()
    dataFile.close()
    lines = [int(i) for i in lines]
    return lines

def testFitness():
    score = 0
    a = ['in1','in2','in3','in4']
    b = [0,1]
    fit = loadFit("setFitness.txt")
    counter = 0

    for in1 in b:
        for in2 in b:
            a = fitness(in1,in2)
            if a == fit[counter]:
                score += 1
            counter += 1

    print('Final score is: ',score/counter)
'''
def createRandomTree(size,inputs):
    tree = []
    for layer in range(size):


    

    return tree
'''
testFitness()