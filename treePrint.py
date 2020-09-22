#   Bayley King
#   Python 3.7.1
#   AST plotting software

'''
    Library installion as follows
        pip3 install graphviz
'''


def checkDuoGate(new_l,ast,bin_ops,solo_ops):
    #print('here is the new_l',new_l)
    if ast[new_l] in bin_ops:
        #print('checkDuoGate found bin op for child 1: ',ast[new_l])
        temp_l = checkDuoGate(new_l + 1,ast,bin_ops,solo_ops)
    elif ast[new_l] in solo_ops:
        #print('checkDuoGate found solo op for child 1:',ast[new_l])
        temp_l = checkSoloGate(new_l + 1,ast,bin_ops,solo_ops)
    else:
        #print('child 1 is not a gate')
        temp_l = new_l + 1

    #print('temp_l from inside the loop part 1: ',temp_l)
    if ast[temp_l] in bin_ops:
        #print('checkDuoGate found bin op for child 2')
        temp_l = checkDuoGate(temp_l + 1,ast,bin_ops,solo_ops)   
    elif ast[temp_l] in solo_ops:
        #print('checkDuoGate found solo op for child 2')
        temp_l = checkSoloGate(temp_l + 1,ast,bin_ops,solo_ops)   
    else:
        #print('child 2 is not a gate')
        temp_l += 1
    
    #print('temp_l from inside the loop part 2: ',temp_l+new_l)
    return temp_l

def checkSoloGate(new_l,ast,bin_ops,solo_ops):
    if ast[new_l] in bin_ops:
        temp_l = checkDuoGate(new_l+1,ast,bin_ops,solo_ops)
        #print('temp_l from solo ops bin check: ',temp_l)
        return temp_l

    elif ast[new_l] in solo_ops:
        temp_l = checkSoloGate(new_l+1,ast,bin_ops,solo_ops)
        #print('temp_l from solo ops solo check: ',temp_l)
        return temp_l 
    else:
        return new_l + 1

def treePrint(ast,bin_ops,solo_ops,file_name='test-output.gv'):
    from graphviz import Digraph

    u = Digraph('unix',filename=file_name,
                node_attr={'color': 'lightblue2', 'style': 'filled'})
    u.attr(size='6,6')

    ast_nums = []

    count_g = 0 
    count_i = 0
    for l in range(len(ast)):
        if ast[l] in bin_ops or ast[l] in solo_ops:
            temp = 'gate_' + str(count_g)
            ast_nums.append(temp)
            count_g += 1
        else:
            temp = 'ins_' + str(count_i)
            ast_nums.append(temp)
            count_i += 1

    zipped_ast = list(zip(ast,ast_nums))
    count = 0
    for node in zipped_ast:
        u.node(node[1],node[0])
        count += 1

    for l in range(len(ast)):
        if ast[l] in bin_ops:
            # next value is child
            # check conditions for second child
            u.edge(zipped_ast[l][1],zipped_ast[l+1][1])
            if ast[l+1] in bin_ops:
                temp_l = checkDuoGate(l+2,ast,bin_ops,solo_ops)
                u.edge(zipped_ast[l][1],zipped_ast[temp_l][1])
            elif ast[l+1] in solo_ops:
                temp_l = checkSoloGate(l+2,ast,bin_ops,solo_ops)
                u.edge(zipped_ast[l][1],zipped_ast[temp_l][1])
            else:
                u.edge(zipped_ast[l][1],zipped_ast[l+2][1])

        elif ast[l] in solo_ops:
            u.edge(zipped_ast[l][1],zipped_ast[l+1][1])

        else:
            pass

    u.render()


def main():
    from params import bin_ops,solo_ops
    treePrint(['nand','nand','I0','Sel','nand','I1','nand','Sel','Sel'],bin_ops,solo_ops)

if __name__ == "__main__":
    main()