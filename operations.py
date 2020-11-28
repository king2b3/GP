#   Python 3.8.6
#   Bayley King
''' All possible operations from parsing along with some functions
      that utilize their logic. Functions also here to return the logic
      of AST, along with returning gates
'''

import random
import sys

######  Gate Operations  ######

def and_op(args):
    return all(args)

def or_op(args):
    return any(args)

def nand_op(args):
    return not all(args)

def nor_op(args):
    return not any(args)

def not_op(args):
    return not args

######  Functions  ######

binary_operators = {
    'and': and_op,
    'or': or_op,
    'nand': nand_op,
    'nor': nor_op
}

solo_operators = {
    'not': not_op
}

operators = {**binary_operators,**solo_operators}

def randomGate():
    return random.choice(list(operators.keys()))      


def returnGate(
    op, args
):
    '''Returns the results of the operation
    '''
    return(operators[op](args))


def returnLogic(
    tempAST, ins
):
    ''' Returns the logical function of an AST

    Requires that boolean values are substituted into the AST in place of inputs

    Will search for first two node tree, and will simplify down to single value
    IE, for the following AST
        ['or','and',True,False,False]
              'and',True,False
      will be selected and simplified into False. The AST will now read
        ['or',False,False]
      which can be simplified into a single value. This value is then returned.
    '''
    currentAST = tempAST
    while len(currentAST) > 1:
        currentAST = tempAST
        temp_len = len(currentAST)
        for node in range(temp_len):
            if checkBinaryGate(node):
                # guesses that the next two nodes in the AST list are the node's children
                children = currentAST[node+1:node+3]
                try:
                    # if children are not gates
                    if type(children[0]) == bool and type(children[1]) == bool:
                        # splits small tree from AST
                        tempStart = currentAST[:node+1]
                        tempEnd = currentAST[node+3:]
                        # preforms logical operation on children
                        tempResult = returnGate(currentAST[node],children)
                        # combines logical result of the tree with old AST
                        tempAST = tempStart  + tempEnd
                        tempAST[node] = tempResult                    
                        break
                except:
                    # error check
                    sys.exit()

            elif checkSoloGate(node):
                child = currentAST[node+1]
                # if child is not a gate
                if type(child) == bool:
                    tempStart = currentAST[:node+1]
                    tempEnd = currentAST[node+2:]
                    # preforms logical operation
                    tempResult = returnGate(currentAST[node],children)
                    # combines logical result with AST
                    tempAST = tempStart  + tempEnd
                    tempAST[node] = tempResult
                    break
    return currentAST


def main():
    for _ in range(10):
        print(randomGate())

if __name__ == "__main__":
    main()