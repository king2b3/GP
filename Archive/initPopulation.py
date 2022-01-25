import json

from deap import base, creator, gp, tools


creator.create("FitnessMax", base.Fitness, weights=(1.0, 1.0))
creator.create("Individual", list, fitness=creator.FitnessMax)

def initIndividual(icls, content):
    return icls(content)

def initPopulation(pcls, ind_init, filename):
    with open(filename, "r") as pop_file:
        contents = json.load(pop_file)
    return contents["population"] #pcls(contents["population"])

toolbox = base.Toolbox()

toolbox.register("population_guess", initPopulation, list, creator.Individual, "my_guess.json")

population = toolbox.population_guess()

print(population)

r = list(population)
print(r)

##########


creator.create("Individual", gp.PrimitiveTree)
toolbox.register("expr", gp.genHalfAndHalf, pset=population, min_=1, max_=2)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)

expr = toolbox.individual()

print(expr)




'''
for e in population_guess:
    print(e)
'''