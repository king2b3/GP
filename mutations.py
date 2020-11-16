#   Genetic Programming Framework
#   Python 3.7
#   Bayley King

import random
from tabulate import tabulate
import itertools

#ops = ['or','and','not','nand']
binOps = ['or','and','nand']
soloOps = ['not']
ops = binOps+soloOps

def mutate(ast,ins):
    '''
    results = []
    for m in [doNothing(ast,ins),randomMutate(ast,ins),crossover(ast,ins),addNode(ast,ins),removeNode(ast,ins)]:
    #for m in [doNothing(ast,ins),randomMutate(ast,ins),crossover(ast,ins),addNode(ast,ins)]:
    #for m in [doNothing(ast,ins),randomMutate(ast,ins),crossover(ast,ins)]:
        results.append(m)
    return results
    '''
    return [m for m in [doNothing(ast,ins),randomMutate(ast,ins),crossover(ast,ins),addNode(ast,ins),removeNode(ast,ins)]]

def randomMutation(ast,ins):
    #mutations = [doNothing(ast,ins),randomMutate(ast,ins),crossover(ast,ins),addNode(ast,ins),removeNode(ast,ins)]
    #mutations = [doNothing(ast,ins),randomMutate(ast,ins),addNode(ast,ins)]#,removeNode(ast,ins)]
    #num = random.randint(0,len(mutations)-1)
    num = random.randint(0,2)

    if num == 0:
        return doNothing(ast,ins)
    elif num == 1:
        return randomMutate(ast,ins)
    elif num == 2:
        return addNode(ast,ins)
    elif num == 3:
        return removeNode(ast,ins)
    elif num == 4:
        return crossover(ast,ins)
    #return mutations[num]

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
    if (len_ast := len(ast)) > 5:
        #len_ast = len(ast)-1
        tempAST = ast.copy()
        gate = random.randint(0,len_ast-1)
        gateCross = random.randint(0,len_ast-1)
        while hasChildren(ast,gate,ins) or ast[gate] in ins:
            gate = random.randint(0,len_ast-1)
        while gateCross == gate or hasChildren(ast,gateCross,ins) or ast[gateCross] in ins :
            gateCross = random.randint(0,len_ast-1)
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


def check_every_add_node(ast,ins,muts_list=[]):
    for comb in itertools.product(*[list(range(len(ast))),list(range(len(ops))),ins,ins]):

        temp_ast = ast.copy()
        if ast[comb[0]] in ops:
            continue
        else:
            temp_gate = comb[0]
            gate = comb[1]
            temp_ast = ast.copy()
            tempStart = temp_ast[:temp_gate]
            tempEnd = temp_ast[temp_gate+1:]
            newNode = []
            newNode.append(ops[gate])

            if ops[gate] == 'not':
                newNode.append(comb[2]) 
            else:
                newNode.append(comb[2])
                newNode.append(comb[3])

            temp = tempStart+newNode+tempEnd
            muts_list.append(temp)
    return muts_list


def addNode(ast,ins):
    len_ins = len(ins)-1
    len_ast = len(ast)-1
    gate = random.randint(0,len_ast)
    while ast[gate] in ops:
        gate = random.randint(0,len_ast)
    tempAST = ast.copy()
    tempStart = tempAST[:gate]
    tempEnd = tempAST[gate+1:]

    newNode = []
    gate = random.randint(0,len(ops)-1)
    newNode.append(ops[gate])

    if ops[gate] == 'not':
        gate1 = random.randint(0,len_ins)
        newNode.append(ins[gate1]) 
    else:
        gate1 = random.randint(0,len_ins)
        gate2 = random.randint(0,len_ins)
        while gate1 == gate2:
            gate2 = random.randint(0,len_ins)
        newNode.append(ins[gate1])
        newNode.append(ins[gate2])

    return tempStart+newNode+tempEnd

def check_every_remove_node(ast,ins,muts_list=[]):
    for comb in itertools.product(*[list(range(len(ast))),ins]):
        if len(ast) > 3 and hasChildren(ast,comb[0],ins):
            gate = comb[0]
            if ast[gate] in soloOps:
                tree = ast.copy()
                start = tree[:gate]
                end = tree[gate+1:]
                temp = start+end
                muts_list.append(temp)
                
            
            elif ast[gate] in binOps:
                tree = ast.copy()
                start = tree[:gate]
                middle = [comb[1]]
                end = tree[gate+3:]
                temp = start+middle+end
                muts_list.append(temp)
            
            else:
                pass
        
    return muts_list


def removeNode(ast,ins):
    if len(ast) > 5:
        gate = random.randint(0,len(ast)-1)
        #print(gate)
        while hasChildren(ast,gate,ins):
            gate = random.randint(0,len(ast)-1)
            #print(gate)

        if ast[gate] in soloOps:
            tree = ast.copy()
            start = tree[:gate]
            end = tree[gate+1:]
            return start+end
        
        elif ast[gate] in binOps:
            tree = ast.copy()
            start = tree[:gate]
            gate1 = random.randint(0,len(ins)-1)
            middle = [ins[gate1]]
            end = tree[gate+3:]
            return start+middle+end
        
        else:
            return ast
    
    else:
        return ast


def doNothing(ast,ins):
    return ast

######### Functions #########    

def hasChildren(tree,gate,ins):
    try:
        children = tree[gate+1:gate+3]
        if tree[gate] in ins:
            return False
        elif children[0] not in ops and children[1] not in ops and tree[gate] in binOps:
            return True
        elif children[0] not in ops and tree[gate] in soloOps:
            return True            
        else:
            return False
    except:
        return False


def main():
    
    original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel']
    ins = ['I0','I1','Sel']
    current_ast = original_ast.copy()
    #ins = ['I0','I1']    

    print(original_ast)
    print(tabulate(check_every_remove_node(current_ast,ins)))
    print(tabulate(check_every_add_node(current_ast,ins)))



if __name__ == '__main__':
    main()