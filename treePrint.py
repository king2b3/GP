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
):
    ''' Checks if the current node is a duo gate or not
    '''
    # checks what the current node is
    if op.checkBinaryGate(ast[new_l]):
        temp_l = checkDuoGate(new_l + 1,ast)
    elif op.checkSoloGate(ast[new_l]):
        temp_l = checkSoloGate(new_l + 1,ast)
    else:
        # if not a bin or solo op, then look at the next child
        temp_l = new_l + 1

    if op.checkBinaryGate(ast[temp_l]):
        temp_l = checkDuoGate(temp_l + 1,ast)   
    elif op.checkSoloGate(ast[temp_l]):
        temp_l = checkSoloGate(temp_l + 1,ast)   
    else:
        # check the next node to be a child
        temp_l += 1
    
    return temp_l

def checkSoloGate(
    new_l, ast,
):
    ''' Checks if the current node is a solo gate
    '''
    if op.checkBinaryGate(ast[new_l]):
        new_l = checkDuoGate(new_l+1,ast)
    elif op.checkSoloGate(ast[new_l]):
        new_l = checkSoloGate(new_l+1,ast)
    else:
        new_l += 1
    return new_l

def treePrint(
    ast,
    fname='temp/temp/output',
    file_name='temp/test-output.gv',
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
    len_ast = len(ast)
    for l in range(len_ast):
        if op.checkGate(ast[l]):
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
    for l in range(len_ast):
        if op.checkBinaryGate(ast[l]):
            u.edge(zipped_ast[l][1],zipped_ast[l+1][1])
            if op.checkBinaryGate(ast[l+1]):
                temp_l = checkDuoGate(l+2,ast)
                # temp_l contains the locations in the AST of this node's children since it is an operator. This only isn't true when the node is an input
                # zipped_ast[l][1] is the first child by default, zipped_ast[temp_l][1] is the second child
                u.edge(zipped_ast[l][1],zipped_ast[temp_l][1])
            elif op.checkSoloGate(ast[l+1]):
                temp_l = checkSoloGate(l+2,ast)
                u.edge(zipped_ast[l][1],zipped_ast[temp_l][1])
            else:
                u.edge(zipped_ast[l][1],zipped_ast[l+2][1])

        elif op.checkSoloGate(ast[l]):
            # next node in ast is it's child
            u.edge(zipped_ast[l][1],zipped_ast[l+1][1])

        else:
            # no need to draw a line if its a input
            pass

    u.render(filename=fname,format='png')


def main():
    treePrint(['or','or','and','and','not','s1','not','s2','d0','and','and','not','s1','s0','d1','or','and','and','s1','not','s0','d0','and','and','s1','s0','d3'])
    #treePrint(['nor', 'nand', 'Sel', 'or', 'nor', 'I1', 'nand', 'not', 'I0', 'I1', 'nand', 'and', 'Sel', 'nand', 'I1'])

if __name__ == "__main__":
    main()