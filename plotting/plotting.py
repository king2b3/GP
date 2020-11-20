'''
   plotting.py - github.com/king2b3/GP
   Description: Plotting Functions for GP statistics (separate from tree printing)
   Start Date: 4 October 2020
   Author: Bayley King
'''

import matplotlib.pyplot as plt
import pickle as pkl

def plot_time_stats(fitness_path='outputs/fitness_time.pkl',
                    mutation_path='outputs/mutations_time.pkl'):
    with open(mutation_path,'rb') as f:
        mutations_time = pkl.load(f)

    with open(fitness_path,'rb') as f:
        fitness_time = pkl.load(f)

    plt.figure()

    epochs = list(range(len(mutations_time)))

    plt.plot(epochs,mutations_time,'ko',label="Mutations Time")
    plt.plot(epochs,fitness_time,'bx',label="Fitness Time")
    plt.xlabel('Epochs')
    plt.ylabel('Time (sec)')
    plt.title('Time for each portion during training')
    plt.legend()
    plt.savefig('outputs/time_plot.jpeg')

plot_time_stats()