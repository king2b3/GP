#   Genetic Programming Framework
#   Python 3.8.6
#   Bayley King

import random
#from tabulate import tabulate      # used just for testing, remove upon completion
import itertools
import operations as op


#ops = ['or','and','not','nand']
#binOps = ['or','and','nand']
#soloOps = ['not']
#ops = binOps+soloOps

def mutate(ast,ins):
    ''' Returns one of each of the mutations
    '''
    return [m for m in [doNothing(ast,ins),randomMutate(ast,ins),crossover(ast,ins),addNode(ast,ins),removeNode(ast,ins)]]

def randomMutation(ast,ins):
    ''' Basic random mutation on random node returned
    '''
    num = random.randint(1,3)

    if num == 1:
        return randomMutate(ast,ins)
    elif num == 2:
        return addNode(ast,ins)
    elif num == 3:
        return removeNode(ast,ins)

######### Mutations #########

def randomMutate(ast,ins):
    ''' Randomly mutates the AST by changing a single node value
    '''
    #selects a node in the AST
    gate = random.randint(0,len(ast)-1)
    tempAST = ast.copy()
    if ast[gate] in op.binary_operators :
        ranIn = op.randomGate()
        while ranIn == ast[gate] or ranIn not in op.binary_operators:
            ranIn = op.randomGate()
        tempAST[gate] = ranIn
    elif ast[gate] in ins:
        ranIn = random.randint(0,len(ins)-1)
        while ins[ranIn] == ast[gate]:
            ranIn = random.randint(0,len(ins)-1)
        tempAST[gate] = ins[ranIn]
    elif ast[gate] in op.solo_operators:
        ''' This will eventually change the Solo gates, but since the only
            one the network currently uses is NOT, there isn't a point in
            doing anything with it yet. 
        '''
        pass
    return tempAST       


def crossover(ast,ins):
    ''' The bane of my existence, this needs fixing BIG time
    '''
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
    ''' Returns every possible variation of the current ast from adding new nodes
            every possbile node, each possible node value and possible child configuration
    '''
    for comb in itertools.product(
            *[
                list(range(len(ast))), # nodes in ast
                list(op.operators.keys()), # node value
                ins, # first child in tree
                ins # second child in tree
                ]
        ):

        temp_ast = ast.copy()
        # if current node in AST is an operator
        if ast[comb[0]] in op.operators:
            continue
        else:
            temp_gate = comb[0] # node value in current AST
            gate = comb[1] # new node value 
            temp_ast = ast.copy()
            # split AST at the current node value in current AST
            tempStart = temp_ast[:temp_gate]
            tempEnd = temp_ast[temp_gate+1:]
            # create new subtree of new node value
            newNode = []
            newNode.append(gate)

            # add children to new subtree
            if gate in op.solo_operators:
                newNode.append(comb[2]) 
            else:
                newNode.append(comb[2])
                newNode.append(comb[3])

            # insert new subtree in middle of split tree
            temp = tempStart+newNode+tempEnd
            # append the new variant ast to return list
            muts_list.append(temp)
    return muts_list


def addNode(ast,ins):
    ''' Returns AST with randomly inserted gate

        ** Needs to be checked to work for standard GA **
    '''
    len_ins = len(ins)-1
    len_ast = len(ast)-1
    # select a random node in the tree
    gate = random.randint(0,len_ast)
    # make sure the node in an input, not an operator
    while ast[gate] in op.operators:
        gate = random.randint(0,len_ast)
    tempAST = ast.copy()
    tempStart = tempAST[:gate]
    tempEnd = tempAST[gate+1:]

    newNode = []
    gate = op.randomGate()
    newNode.append(gate)

    if gate in op.solo_operators:
        # create one random child 
        child = random.randint(0,len_ins)
        newNode.append(ins[child]) 
    else:
        # create two random children
        child1 = random.randint(0,len_ins)
        child2 = random.randint(0,len_ins)
        newNode.append(ins[child1])
        newNode.append(ins[child2])

    # recombine AST and return it
    return tempStart+newNode+tempEnd


def check_every_remove_node(ast,ins,muts_list=[]):
    ''' Returns a list with every possible variant of the current AST by
          removing nodes
    '''
    for comb in itertools.product(
            *[
                list(range(len(ast))), # nodes in the AST
                ins # list of inputs to be inserted in place of removed node
            ]):
        
        # if the AST is larger than 3, and the current node is removable 
        if len(ast) > 3 and hasChildren(ast,comb[0],ins):
            gate = comb[0]
            if gate in op.solo_operators:
                tree = ast.copy()
                # splits the AST removing the gate
                start = tree[:gate]
                end = tree[gate+1:]
                temp = start+end
                muts_list.append(temp)
                
            elif gate in op.binary_operators:
                tree = ast.copy()
                # splits the ast by removing the subtree
                start = tree[:gate]
                # every possible input in place of the tree
                middle = [comb[1]]
                end = tree[gate+3:]
                temp = start+middle+end
                muts_list.append(temp)
            
            else:
                pass
        
    return muts_list


def removeNode(ast,ins):
    ''' Returns a variant with a randomly removed node

        ** Need to check before use in standard GA **
    '''
    if len(ast) > 5:
        # selects random node in the current ast
        gate = random.randint(0,len(ast)-1)
        # makes sure the node is a removable node
        while not hasChildren(ast,gate,ins):
            gate = random.randint(0,len(ast)-1)

        if ast[gate] in op.solo_operators:
            tree = ast.copy()
            start = tree[:gate]
            end = tree[gate+1:]
            # leaves child of the op, maybe insert a random input in the future?
            return start+end
        
        elif ast[gate] in op.binary_operators:
            tree = ast.copy()
            start = tree[:gate]
            # make this into a function?
            new_input = random.randint(0,len(ins)-1)
            middle = [ins[new_input]]
            end = tree[gate+3:]
            # returns reconstructed variant
            return start+middle+end
        
        else:
            return ast
    
    else:
        return ast


def doNothing(ast,ins):
    ''' Returns nothing, needed for chance that nothing happens.
          Can probably replace with pass in other code
    '''
    return ast

######### Functions #########    

def hasChildren(tree,gate,ins):
    ''' Checks if node has children
        Returns Boolean. True if the next node(s) are children of the node
            tree: the current AST : list
            gate: location of node in AST : int
            ins: list of inputs
    '''
    try:
        # pulls next nodes in the tree
        children = tree[gate+1:gate+3]
        if tree[gate] in ins:
            # Node is an input 
            return False
        elif children[0] not in op.operators and 
             children[1] not in op.operators and 
             tree[gate] in op.binary_operators:
            # Node is an end leaf, it could be removed
            return True
        elif children[0] not in op.operators and 
             tree[gate] in op.solo_operators:
            # Node is an end leaf, it could be removed
            return True            
        else:
            return False
    except:
        # might be able to remove this, broken case was when it was the end nodes in the AST
        return False


def main():
    # assuming the code works after OOP and operators changes. Might need to check with main again 
    original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel']
    ins = ['I0','I1','Sel']
    current_ast = original_ast.copy()
    #ins = ['I0','I1']    

    print(original_ast)
    for gate in range(len(original_ast)):
        print(hasChildren(original_ast,gate,ins))
    #print(tabulate(check_every_remove_node(current_ast,ins)))
    #print(tabulate(check_every_add_node(current_ast,ins)))


if __name__ == '__main__':
    main()