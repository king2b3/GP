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

def xor_op(args):
    return and_op([or_op(args),nand_op(args)])

def ff_op(args):
    ''' returns saved value from FF, sets new saved value to current 2nd child value
    '''
    temp = ff_statements[args[0]]
    ff_statements[args[0]] = args[1]
    return temp

def if_op(args):
    ''' Returns IF statement operations.
    args is in this format
        if x == 1:
            return True
        else:
            return False

    ['=','x','1',True,False]
                    if
            =             body
        x       1   if_true     if_false

        CURRENTLY UNUSED
    '''
    temp = check_cond(args)
    if temp:
        return args[3]
    else:
        return args[4]
    

def check_cond(args):
    ''' Returns if result from conditions
    '''
    if args[0] == '=':
        return args[1] == args [2]
    elif args[0] == '>':
        return args[1] > args [2]
    elif args[0] == '<':
        return args[1] < args [2]
    elif args[0] == '!=':
        return not (args[1] == args [2])
    elif args[0] == '>=':
        return args[1] >= args [2]
    elif args[0] == '<=':
        return args[1] <= args [2]

######  Functions  ######

ff_statements = {
}

binary_operators = {
    'and': and_op,
    'or': or_op,
    'nand': nand_op,
    'nor': nor_op,
    'xor': xor_op
}

solo_operators = {
    'not': not_op
}

statement_operators = {
    #'if': if_op,
    'ff': ff_op
}

operators = {
    **binary_operators,**solo_operators #,**statement_operators
}


def returnFFLen():
    return len(ff_statements)


def randomGate():
    return random.choice(list(operators.keys()))      


def returnGate(
    op, args
):
    '''Returns the results of the operation
    '''
    return(operators[op](args))


def checkStatementGate(
    node
):
    ''' Checks if the node is a statement operator
    '''
    return node in statement_operators


def checkBinaryGate(
    node
):
    ''' Checks if the node is a binary operator
    '''
    return node in binary_operators


def checkSoloGate(
    node
):
    ''' Checks if the node is a solo operator
    '''
    return node in solo_operators


def checkGate(
    node
):
    ''' Checks if the node is an operator
    '''
    return node in operators


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
    
    currentAST = tempAST.copy()
    while len(currentAST) > 1:
        currentAST = tempAST
        temp_len = len(currentAST)
        for node in range(temp_len):
            if checkBinaryGate(currentAST[node]):
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

            elif checkSoloGate(currentAST[node]):
                child = currentAST[node+1]
                # if child is not a gate
                if type(child) == bool:
                    tempStart = currentAST[:node+1]
                    tempEnd = currentAST[node+2:]
                    # preforms logical operation
                    tempResult = returnGate(currentAST[node],child)
                    # combines logical result with AST
                    tempAST = tempStart  + tempEnd
                    tempAST[node] = tempResult
                    break

            elif checkStatementGate(currentAST[node]):
                children = currentAST[node+1:node+3]
                if type(children[1]) == bool:
                    tempStart = currentAST[:node+1]
                    tempEnd = currentAST[node+3:]
                    # preforms statement operation
                    tempResult = returnGate(currentAST[node],children)
                    # combines logical result with AST
                    tempAST = tempStart  + tempEnd
                    tempAST[node] = tempResult
                    break

    return currentAST


def main():
    #ff_statements['ff_0'] = False
    #t = ['ff_0',False]
    #print(returnGate('ff',t))
    print(xor_op([False,False]))
    print(xor_op([False,True]))
    print(xor_op([True,False]))
    print(xor_op([True,True]))

if __name__ == "__main__":
    main()