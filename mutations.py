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

def mutate(
    ast,ins
):
    ''' Returns one of each of the mutations
    '''
    return [m for m in [doNothing(ast,ins),randomMutate(ast,ins),addNode(ast,ins),removeNode(ast,ins)]]

def randomMutation(
    ast,ins
):
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

def randomMutate(
    ast,ins
):
    ''' Randomly mutates the AST by changing a single node value
    '''
    #selects a node in the AST
    gate = random.randint(0,len(ast)-1)
    len_ins = len(ins)
    tempAST = ast.copy()
    if op.checkBinaryGate(ast[gate]) :
        ranGate = op.randomGate()
        while ranGate == ast[gate] or not op.checkBinaryGate(ranGate):
            ranGate = op.randomGate()
        tempAST[gate] = ranGate
    elif ast[gate] in ins:
        ranIn = random.randint(1,len_ins-1)
        while ins[ranIn] == ast[gate]:
            ranIn = random.randint(1,len_ins-1)
        tempAST[gate] = ins[ranIn]
    elif op.checkSoloGate(ast[gate]):
        ''' This will eventually change the Solo gates, but since the only
            one the network currently uses is NOT, there isn't a point in
            doing anything with it yet. 
        '''
        pass
    return tempAST       


def exhaustiveMutationsCheck(
    ast, ins
):
    ''' Function that checks all possible mutations to a single node

    goes through full AST
      Checks if current node is an input, or binary gate or a solo gate
      Append the full possibility of new node values
    '''
    circuit_test = [ast]
    orig_ast = ast.copy()
    for gate in range(len(ast)):
        ast = orig_ast.copy() # is this line needed?
        if ast[gate] in ins:
            for new_gate in ins:
                # step through all inputs
                ast = orig_ast.copy()
                if new_gate == ast[gate]:
                    # current AST (no change) already appended to the list
                    pass
                else:
                    # append AST with input mutation
                    ast[gate] = new_gate
                    circuit_test.append(ast)
        elif op.checkBinaryGate(ast[gate]):
            for new_gate in op.binary_operators.keys():
                # step through all binary operators
                ast = orig_ast.copy()
                if new_gate == ast[gate]:
                    # current AST (no change) already appended to the list
                    pass
                else:
                    # append AST with gate mutation
                    ast[gate] = new_gate
                    circuit_test.append(ast)
        elif op.checkSoloGate(ast[gate]):
            for new_gate in op.solo_operators.keys():
                # step through all solo operators
                ast = orig_ast.copy()
                if new_gate == ast[gate]:
                    # current AST (no change) already appended to the list
                    pass
                else:
                    # append AST with gate mutation
                    ast[gate] = new_gate
                    circuit_test.append(ast)
        else:
            raise Exception
    # checks for best mutated AST. See issue #9
    return circuit_test


def crossover(
    ast_1, ast_2, ins
):
    ''' The bane of my existence, this needs fixing BIG time

        Look into crossover for ordered lists here https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)
    '''
    len_ast_1 = len(ast_1)
    len_ast_2 = len(ast_2)
    gate_ast_1 = random.randint(1,len_ast_1-1)
    gate_ast_2 = random.randint(1,len_ast_2-1)
    
    # makes sure node selected in ast_1 is an operator
    while ast_1[gate_ast_1] not in op.operators:
        gate_ast_1 = random.randint(1,len_ast_1-1)
    # makes sure node selected in ast_2 is an operator
    while ast_2[gate_ast_2] not in op.operators or gate_ast_1 == gate_ast_2:
        gate_ast_2 = random.randint(1,len_ast_2-1)

    #print(ast_1)
    #print(gate_ast_1)
    #print(ast_2)
    #print(gate_ast_2)
    ast_1_first = ast_1[:gate_ast_1]
    ast_1_middle, ast_1_end = findRoots(ast_1, gate_ast_1,ins)
    ast_2_first = ast_2[:gate_ast_2]
    ast_2_middle, ast_2_end = findRoots(ast_2, gate_ast_2,ins)

    new_ast_1 = ast_1_first + ast_2_middle + ast_1_end
    new_ast_2 = ast_2_first + ast_1_middle + ast_2_end

    return new_ast_1, new_ast_2

    
def check_every_add_node(
    ast, ins,
    muts_list=[]
):
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
        if op.checkGate(ast[comb[0]]):
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


def addNode(
    ast, ins
):
    ''' Returns AST with randomly inserted gate

        ** Needs to be checked to work for standard GA **
    '''
    len_ins = len(ins)-1
    len_ast = len(ast)-1
    # select a random node in the tree
    gate = random.randint(0,len_ast)
    # make sure the node is an input, not an operator
    while op.checkGate(ast[gate]):
        gate = random.randint(0,len_ast)
    tempAST = ast.copy()
    tempStart = tempAST[:gate]
    tempEnd = tempAST[gate+1:]

    newNode = []
    gate = op.randomGate()
    newNode.append(gate)

    if op.checkSoloGate(gate):
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


def check_every_remove_node(
    ast, ins,
    muts_list=[]
):
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
            if op.checkSoloGate(gate):
                tree = ast.copy()
                # splits the AST removing the gate
                start = tree[:gate]
                end = tree[gate+1:]
                temp = start+end
                muts_list.append(temp)
                
            elif op.checkBinaryGate(gate):
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


def removeNode(
    ast, ins
):
    ''' Returns a variant with a randomly removed node

        ** Need to check before use in standard GA **
    '''
    if (len_ast := len(ast)) > 5:
        # selects random node in the current ast
        gate = random.randint(0,len_ast-1)
        # makes sure the node is a removable node
        while not hasChildren(ast,gate,ins):
            gate = random.randint(0,len_ast-1)

        if op.checkSoloGate(ast[gate]):
            tree = ast.copy()
            start = tree[:gate]
            end = tree[gate+1:]
            # leaves child of the op, maybe insert a random input in the future?
            return start+end
        
        elif op.checkBinaryGate(ast[gate]):
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


def doNothing(
    ast, ins
):
    ''' Returns nothing, needed for chance that nothing happens.
          Can probably replace with pass in other code
    '''
    return ast

######### Functions #########    

def hasChildren(
    tree, gate, ins
):
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
        elif not op.checkGate(children[0]) and \
             not op.checkGate(children[1]) and \
             op.checkBinaryGate(tree[gate]):
            # Node is an end leaf, it could be removed
            return True
        elif not op.checkGate(children[0]) and \
             op.checkSoloGate(tree[gate]):
            # Node is an end leaf, it could be removed
            return True            
        else:
            return False
    except:
        # might be able to remove this, broken case was when it was the end nodes in the AST
        return False


def findRoots(
    tree, gate, ins
):
    ''' This function will return the crossover portion of a circuit 

        Returns:
        middle: list of strings
            The middle portion of AST that will be used in crossover
        end: list of strings
            The remaining portion of the AST that won't be used in the crossover
    '''
    middle = []
    end = []
    new_tree = tree[gate:]
    for node in range(len(new_tree)):
        if hasChildren(new_tree,node,ins):
            gate2 = node + 3
            break
    middle = new_tree[:gate2]
    end = new_tree[gate2:]

    return middle, end



def main():
    # assuming the code works after OOP and operators changes. Might need to check with main again 
    original_ast = ['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel']
    ast = ['or','nand','I1','nand','Sel','Sel','I0']
    ins = ['I0','I1','Sel']
    #current_ast = original_ast.copy()
    #ins = ['I0','I1']   
    ast1, ast2 = crossover(original_ast,ast,ins)
    print(ast)
    print(ast2)
    print(original_ast)
    print(ast1)


if __name__ == '__main__':
    main()