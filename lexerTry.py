#lex = ['or','and','not','in1','in2','and','not','in2','in1','and','and','in1','in2','in1']
lex = ['or','and','not',False,False,'and','not',False,False]
#lex = ['or',False,False,]
Ins = ['in2','in2']
binOps = ['or','and']
soloOps = ['not']

class AST():
    def __init__(self,ast,inputs):
        self.origAST = tuple(ast)
        self.counterLoc = 0
        self.currentAST = list(self.origAST)
        self.numIts = 0
        self.inputs = inputs
        self.currentfit = 0

    def funcTest(self,l,loc):
        if l in binOps:
            children = self.currentAST[loc+1:loc+3]
            #print('\tBin Op:',l,'with children:',children)
            for c in range(len(children)):
                if children[c] in binOps or children[c] in soloOps:
                    #print('CHILD CHANGED, ORIGINAL',children)
                    children[c] = self.funcTest(children[c],loc+1)
                    children[c+1] = self.currentAST[loc+3]
                    #print('CHILD CHANGED, NEW',children)
                loc += 1
            #print('\t\tBinops results',children,BinOps(children,l))
            return BinOps(children,l)
                
        elif l in soloOps:
            child = self.currentAST[loc+1]
            #print('\tSolo Op:',l,'with child:',child)
            if child in binOps or child in soloOps:
                self.funcTest(child,loc+1)
            else:
                #print('\t\tSolo Results',SoloOps(child,l))
                return SoloOps(child,l)

        elif type(l) == bool:
            pass
        
        else:
            self.error()


    def error(self):
        raise Exception('Invalid operator in AST')


def BinOps(children,l):
    if l == 'or':
        return children[0] or children[1]
    elif l == 'and':
        return children[0] and children[1]

def SoloOps(child,l):
    if l == 'not':
        return not child



def main():

    import re
    lex = ('or','and','not','in1','in2','and','not','in2','in1','and','and','in1','in2','in1')
    results = []
    '''
    for l in lex:
        print('operator is',l)
        results.append(ast.funcTest(l,ast.counterLoc))
    #while ast.fit =! 1:
    results = list(filter(lambda a: a !=None,results))
    print(results)
    '''

    for in1 in [True,False]:
        for in2 in [True,False]:
            lext = list(lex)
            for l in range(len(lex)):
                if lext[l] == 'in1':
                    lext[l] = in1
                elif lext[l] == 'in2':
                    lext[l] = in2
            ast = AST(lext,Ins)
            print(lext)
            print(ast.funcTest(lext[0],ast.counterLoc))
    



if __name__ == '__main__':
    main()