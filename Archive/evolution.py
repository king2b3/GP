#   Bayley King
#   Python 3.7.3
#   1-23
'''
import networkx as nx
import pickle
import random
import matplotlib.pyplot as plt
import operator
import json


from deap import base, creator, gp, tools
pset = gp.PrimitiveSet("MAIN", 2, "IN")
pset.renameArguments(IN0="X", IN1="Y", IN2="Z")
pset.renameArguments(IN3="D0", IN4="D1")
pset.addPrimitive(operator.and_, 2)
pset.addPrimitive(operator.or_, 2)
pset.addPrimitive(operator.not_, 2)
pset.addPrimitive(operator.xor, 2)


creator.create("Individual", gp.PrimitiveTree)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=3, max_=5)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)

expr = toolbox.individual()


print(expr)

pickle.dumps(expr)
print(expr)


with open('testPop.pickle', 'wb') as outfile:
    pickle.dump(expr,outfile)


A = pickle.load(open('testPop.pickle','rb'))

print(A)
#print(dir(A))
'''
############################################################
import operator
import random
import time
import pyrtl
from pyrtl.rtllib import aes, testingutils

from deap import base
from deap import creator
from deap import tools
from deap import gp

import networkx as nx
import matplotlib.pyplot as plt



def check(condition, retval):
    if condition:
        raise pyrtl.PyrtlError("Invalid")
    return retval


def key_gen(aes, key):
    return aes._key_gen(key)


def init_add_round_key(aes, key, plaintext):
    t = aes._add_round_key(plaintext, key[0])
    return (t, key)


def main_loop(aes, input, condition, func, func2, func3, func4, ifcondition, ifright, lamb):
    t = input[0]
    key = input[1]
    for i in condition:
        t = func(aes, func2(aes, ifcondition, func3(aes, func4(aes, t)), ifright, lamb), key, i)
    return t


def add_round_key(aes, t, key, roundn):
    return aes._add_round_key(t, key[roundn])


def if_then_else(aes, cond, t, ifright, lamb):
    if cond(t, ifright):
        return lamb(aes, t)
    return t


def shift_rows(aes, t):
    return aes._shift_rows(t)


def sub_bytes(aes, t):
    return aes._sub_bytes(t)


def mix_columns(aes, t):
    return aes._mix_columns(t)


def rangen(start, stop):
    return range(start, stop)


def trojan(s):
    # here Trojan would inject fault, or assign input to some other output in pyrtl
    # serial_out <<= s
    # print(s)
    return s


s = "main_loop(aes, init_add_round_key(aes, key_gen(aes, check(ne(len(key), 128), key)), check(ne(len(secret), 128), secret)), rangen(0, 11), ark, ite, sr, sb, note, 10, mc)"

pset = gp.PrimitiveSet("MAIN", 3, "IN")
pset.renameArguments(IN0="aes")
pset.renameArguments(IN1="secret")
pset.renameArguments(IN2="key")
pset.addPrimitive(main_loop, 10)
pset.addPrimitive(check, 2)
pset.addPrimitive(key_gen, 2)
pset.addPrimitive(init_add_round_key, 3)
pset.addPrimitive(operator.ne, 2, "ne")
pset.addPrimitive(add_round_key, 4)
pset.addPrimitive(if_then_else, 5)
pset.addPrimitive(shift_rows, 2)
pset.addPrimitive(sub_bytes, 2)
pset.addPrimitive(mix_columns, 2)
pset.addPrimitive(rangen, 2)
pset.addPrimitive(len, 1)
pset.addPrimitive(trojan, 1)
pset.addTerminal(operator.ne, "note")
pset.addTerminal(add_round_key, "ark")
pset.addTerminal(if_then_else, "ite")
pset.addTerminal(shift_rows, "sr")
pset.addTerminal(mix_columns, "mc")
pset.addTerminal(sub_bytes, "sb")
pset.addTerminal(10)
pset.addTerminal(128)
pset.addTerminal(0)
pset.addTerminal(11)


creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()
toolbox.register("expr", gp.genFull, pset=pset, min_=1, max_=5)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)
expr = toolbox.individual()


func = toolbox.compile(expr)#=individual)
nodes, edges, labels = gp.graph(expr)#=individual)

'''
toolbox.register("evaluate", eval_aes)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.decorate("mate", gp.staticLimit(operator.attrgetter('height'), 90))
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=3)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)
toolbox.register("shrink", gp.mutShrink)
'''
############################################################
#nodes, edges, labels = gp.graph(expr)

### Graph ###
g = nx.petersen_graph()
g.add_nodes_from(nodes)
g.add_edges_from(edges)
pos = nx.nx_agraph.graphviz_layout(g, prog="dot")

nx.draw_networkx_nodes(g, pos)
nx.draw_networkx_edges(g, pos)
nx.draw_networkx_labels(g, pos, labels)
plt.show()

