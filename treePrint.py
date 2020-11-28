#   Bayley King
#   Python 3.7.1
#   AST plotting software

'''
    Library installion as follows
        pip3 install graphviz
'''

import operations as op

def checkDuoGate(
    new_l, ast,
    bin_ops=op.binary_operators.keys(),
    solo_ops=op.solo_operators.keys()
):
    ''' Checks if the current node is a duo gate or not
    '''
    # checks what the current node is
    if ast[new_l] in bin_ops:
        temp_l = checkDuoGate(new_l + 1,ast,bin_ops,solo_ops)
    elif ast[new_l] in solo_ops:
        temp_l = checkSoloGate(new_l + 1,ast,bin_ops,solo_ops)
    else:
        # if not a bin or solo op, then look at the next child
        temp_l = new_l + 1

    if ast[temp_l] in bin_ops:
        temp_l = checkDuoGate(temp_l + 1,ast,bin_ops,solo_ops)   
    elif ast[temp_l] in solo_ops:
        temp_l = checkSoloGate(temp_l + 1,ast,bin_ops,solo_ops)   
    else:
        # check the next node to be a child
        temp_l += 1
    
    return temp_l

def checkSoloGate(
    temp_l, ast,
    bin_ops=op.binary_operators.keys(),
    solo_ops=op.solo_operators.keys()
):
    ''' Checks if the current node is a solo gate
    '''
    if ast[new_l] in bin_ops:
        temp_l = checkDuoGate(temp_l+1,ast,bin_ops,solo_ops)
    elif ast[new_l] in solo_ops:
        temp_l = checkSoloGate(temp_l+1,ast,bin_ops,solo_ops)
    else:
        temp_l += 1
    return temp_l

def treePrint(
    ast,
    file_name='test-output.gv',
    bin_ops=op.binary_operators.keys(),
    solo_ops=op.solo_operators.keys()
):
    ''' Prints ast to a pdf file
    '''
    from graphviz import Digraph

    u = Digraph('unix',filename=file_name,
                node_attr={'color': 'lightblue2', 'style': 'filled'})
    u.attr(size='6,6')

    ast_nums = []

    count_g = 0 # number of gate counter
    count_i = 0 # number of input counter
    # steps through the AST
    for l in range(len(ast)):
        if ast[l] in bin_ops or ast[l] in solo_ops:
            # names the node as a gate_gateCounter
            temp = 'gate_' + str(count_g)
            ast_nums.append(temp)
            # updates counter
            count_g += 1
        else:
            # names the node an input_insCounter
            temp = 'ins_' + str(count_i)
            ast_nums.append(temp)
            count_i += 1

    zipped_ast = list(zip(ast,ast_nums))
    count = 0
    for node in zipped_ast:
        # creates the nodes 
        u.node(node[1],node[0])
        count += 1

    # draws the lines between the nodes
    for l in range(len(ast)):
        if ast[l] in bin_ops:
            u.edge(zipped_ast[l][1],zipped_ast[l+1][1])
            if ast[l+1] in bin_ops:
                temp_l = checkDuoGate(l+2,ast,bin_ops,solo_ops)
                # temp_l contains the locations in the AST of this node's children since it is an operator. This only isn't true when the node is an input
                # zipped_ast[l][1] is the first child by default, zipped_ast[temp_l][1] is the second child
                u.edge(zipped_ast[l][1],zipped_ast[temp_l][1])
            elif ast[l+1] in solo_ops:
                temp_l = checkSoloGate(l+2,ast,bin_ops,solo_ops)
                u.edge(zipped_ast[l][1],zipped_ast[temp_l][1])
            else:
                u.edge(zipped_ast[l][1],zipped_ast[l+2][1])

        elif ast[l] in solo_ops:
            # next node in ast is it's child
            u.edge(zipped_ast[l][1],zipped_ast[l+1][1])

        else:
            # no need to draw a line if its a input
            pass

    u.render()


def main():
    from params import bin_ops,solo_ops
    treePrint(['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],bin_ops,solo_ops)

if __name__ == "__main__":
    main()