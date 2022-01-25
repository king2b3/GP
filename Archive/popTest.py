# Simple Example #i                                                                                                                                                                                                                            
import numpy
import networkx as nx
import pickle
import random
import matplotlib.pyplot as plt
import operator
import json
from functools import wraps

from deap import base, creator, gp, tools

def counter(func):
    @wraps(func)
    def tmp(*args, **kwargs):
        tmp.count += 1
        return func(*args, **kwargs)
    tmp.count = 0
    return tmp




@counter
def cp():
    i = cp.count - 1
    CP = C[i,:]

    #CP = C[0][i,:]                                                                                                                                                                                                                            
    return(CP)


X = 0
Y = 0

#C = numpy.array([operator.or_(X,Y)])

creator.create("Individual", gp.PrimitiveTree)





print(C)

creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

def initIndividual(icls, content):
    return icls(content)

def initPopulation(pcls, ind_init, filename):
    C = pickle.load(open('testPop.pickle','rb'))
    return pcls(C)

toolbox = base.Toolbox()

toolbox.register("individual_guess", initIndividual, creator.Individual)
toolbox.register("population_guess", initPopulation, list, toolbox.individual_guess, C)

population = toolbox.population_guess()

