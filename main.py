#   Python 3.7.3
#   Bayley King
#   University of Cincinnati MIND Lab
'''
    General container and "main" file for GP system using here boy algorithm.
    Takes in from mutations.py, lexer.py, stringComp.py and exhaustiveTest.py.
    
'''
import StringComp
import HereBoy 
#from exhaustiveTest import exhaustiveTest
#from mutations import mutations

### Definitions ###
maxEpochs = 1000
#ast,inputs = loadAST()
inputs = ['in1','in2']
####################


newTree2 = ['or','in1','and','in1','or','in1','in2']
#newTree1 = ['or','in1','and','in1','or','in1','in2']
newTree1 = ['or','in1','in2']
if len(newTree1) > len(newTree2):
    tree2 = tuple(newTree1)
    tree1 = newTree2
elif len(newTree1) < len(newTree2):
    tree2 = tuple(newTree2)
    tree1 = newTree1
else:
    tree2 = tuple(newTree1)
    tree1 = newTree2

test1 = HereBoy.HereBoy(tree1,inputs)
tree1, tree2 = test1.strCmp.structure(tree1,tree2)
print(test1.strCmp.diffCount)
print(tree1,'\n',tree2)

tree1,tree2 = test1.strCmp.nodes(tree1,tree2)
print(test1.strCmp.diffCount)
print(tree1,'\n',tree2)

'''
while fit != 0 or epoch != maxEpochs:
    changeFitness()
    test1.m.mutate()
    test1.strCmp.compare()
'''