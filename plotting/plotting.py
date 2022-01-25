'''
   plotting.py - github.com/king2b3/GP
   Description: Plotting Functions for GP statistics (separate from tree printing)
   Start Date: 4 October 2020
   Author: Bayley King
'''

import matplotlib.pyplot as plt
import pickle as pkl

def decay_LR(t,tau,no):
    # copy of function from networks.py for testing
    import numpy as np
    a = no*np.exp(-t/tau)
    if a < .001:
        a = .001
    return a


def sigma(e,tauN,sigmaP):
    # copy of function from networks.py for testing


    return s


def plot_time_stats() -> None:
    import math
    plt.figure()
    s_fit = []
    l_fit = []
    t_fit = []

    for t in range(1000):
        temp = 0.7*math.exp(-t/1000)
        if temp <= 0.3:
            s_fit.append(0.3)
            l_fit.append(0.7)
        else:
            s_fit.append(temp)
            l_fit.append(1-temp)
        t_fit.append(1)

    gens = list(range(1000))

    plt.plot(gens,s_fit,'r-',label="Structural Fitness")
    plt.plot(gens,l_fit,'b-',label="Logical Fitness")
    plt.plot(gens,t_fit,'g-',label="Summed Fitness")
    plt.ylim([0,1.4])
    plt.xlabel('Generations')
    plt.ylabel('Fitness Score')
    plt.legend()
    plt.savefig('outputs/summed_fitness.jpeg')

plot_time_stats()