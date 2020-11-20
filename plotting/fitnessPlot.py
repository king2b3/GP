#   Python 3.7.3
#   Bayley King
#   9/9/2020

import matplotlib.pyplot as plt
import numpy as np

maxEpochs = 1000

minSim = .3
startSim = .7
strucFit = []
logFit = []

for epochs in range(maxEpochs):
    temp = startSim*np.exp(-epochs/maxEpochs)
    if temp <= minSim:
        strucFit.append(minSim)
        logFit.append(1-minSim)
    else:
        strucFit.append(temp)
        logFit.append(1-temp)


epochs = range(maxEpochs)

fig, ax1 = plt.subplots()

a = ax1.plot(epochs,strucFit, 'r-',label='Structural Fitness')
b = ax1.plot(epochs,logFit, 'b-',label='Logical Fitness')

ax1.set_xlabel('Epochs')
ax1.set_ylabel('Tree Comp')
ax1.set_ylim([0,1])

plt.show()