# parameters for system
import operator

def And(x,y):
    return (x and y)

def Or(x,y):
    return (x or y)

def Not(x):
    return (not x)

x = True
y = False 

funcs = [And,Or]

for f in funcs:
    print(f(x,y))

def fitness(in1,in2,in3,in4):
    return ( (in1 and in2) or (in3 and in4) )

#print(fitness(True,True,False,True))

print(And(Or(True,False),False))
