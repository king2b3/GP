#   Genetic Programming Framework
#   Python 3.7
#   Bayley King

import random

ops = ['or','and','not','nand']

def mutate(ast,ins):
    results = []
    for m in [doNothing(ast,ins),randomMutate(ast,ins),crossover(ast,ins),addNode(ast,ins),removeNode(ast,ins)]:
    #for m in [doNothing(ast,ins),randomMutate(ast,ins),crossover(ast,ins),addNode(ast,ins)]:
    #for m in [doNothing(ast,ins),randomMutate(ast,ins),crossover(ast,ins)]:
        results.append(m)
    return results

def randomMutation(ast,ins):
    #mutations = [doNothing(ast,ins),randomMutate(ast,ins),crossover(ast,ins),addNode(ast,ins),removeNode(ast,ins)]
    mutations = [doNothing(ast,ins),randomMutate(ast,ins),addNode(ast,ins),removeNode(ast,ins)]
    num = random.randint(0,len(mutations)-1)
    return mutations[num]

######### Mutations #########

def randomMutate(ast,ins):
    gate = random.randint(0,len(ast)-1)
    tempAST = list(ast)
    binOps = ['or','and','nand']
    if ast[gate] in binOps:
        ranIn = random.randint(0,len(binOps)-1)
        while binOps[ranIn] == ast[gate]:
            ranIn = random.randint(0,len(binOps)-1)
        tempAST[gate] = binOps[ranIn]
    elif ast[gate] in ins:
        ranIn = random.randint(0,len(ins)-1)
        while ins[ranIn] == ast[gate]:
            ranIn = random.randint(0,len(ins)-1)
        tempAST[gate] = ins[ranIn]
    return tempAST       


def crossover(ast,ins):
    if len(ast) > 5:
        tempAST = list(ast)
        gate = random.randint(0,len(ast)-1)
        gateCross = random.randint(0,len(ast)-1)
        while ast[gate] in ins or hasChildren(ast,gate,ins):
            gate = random.randint(0,len(ast)-1)
        while ast[gateCross] in ins or gateCross == gate or hasChildren(ast,gateCross,ins):
            gateCross = random.randint(0,len(ast)-1)
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
    else:
        return ast

def addNode(ast,ins):
    gate = random.randint(0,len(ast)-1)
    while ast[gate] in ops or isLeaf(ast,gate,ins):
        gate = random.randint(0,len(ast)-1)
    tempAST = list(ast)
    tempStart = tempAST[:gate]
    tempEnd = tempAST[gate+1:]

    newNode = []
    gate = random.randint(0,len(ops)-1)
    newNode.append(ops[gate])

    if ops[gate] == 'not':
        gate1 = random.randint(0,len(ins)-1)
        newNode.append(ins[gate1]) 
    else:
        gate1 = random.randint(0,len(ins)-1)
        gate2 = random.randint(0,len(ins)-1)
        while gate1 == gate2:
            gate2 = random.randint(0,len(ins)-1)
        newNode.append(ins[gate1])
        newNode.append(ins[gate2])

    return tempStart+newNode+tempEnd


def removeNode(ast,ins):
    if len(ast) > 5:
        gate = random.randint(0,len(ast)-1)
        while ast[gate] in ins or isLeaf(ast,gate,ins):
            gate = random.randint(0,len(ast)-1)

        if ast[gate] == 'not':
            tree = list(ast)
            start = tree[:gate]
            end = tree[gate+1:]
            return start+end
        else:
        
            tree = list(ast)
            start = tree[:gate]
            gate1 = random.randint(0,len(ins)-1)
            middle = [ins[gate1]]
            end = tree[gate+3:]

            return start+middle+end
    else:
        return ast


def doNothing(ast,ins):
    return ast

######### Functions #########    

def hasChildren(tree,gate,ins):
    try:
        children = tree[gate+1:gate+3]
        if children[0] in ops or children[1] in ops:
            return True
        else:
            return False
    except:
        return False

def isLeaf(tree,gate,ins):
    if tree[gate-1] in ops and tree[gate+1] in ins:
        return False
    else:
        return True




def main():
    ast = ('or','and','A','B','and','B','A')
    test_ast = list(ast)
    ins = ['A','B']
    
    results = mutate(test_ast,ins)
    for r in results:
        print(r)
    
    #print(randomMutation(test_ast,ins))



if __name__ == '__main__':
    main()