#   Python 3.7.3
#   Bayley King
#   9/9/2020

import matplotlib.pyplot as plt 


ins = [3,4,5,6,7]

suc = [
    [0.67, 0.34, 0.00, 0.34, 0.34], #-hb-r
    [0.34, 0.67, 0.67, 0.67, 0.67], #-hb-ct
    [1.00, 0.67, 0.34, 0.00, 0.00], #-hb-d
    [], #-e-r
    [], #-e-ct
    [], #-e-d
    [1.00, 1.00, 1.00, 1.00, 1.00], #-s-r
    [], #-s-ct
    [], #-s-d
]

epochs = [
    [1450.67, 2772.00, 4000.00, 3130.00, 2744.67], #-hb-r
    [2669.67, 1972.33, 1591.00, 2365.00, 1567.00], #-hb-ct
    [88.67,   1358.67, 2690.67, 4000.00, 4000.00], #-hb-d
    [], #-e-r
    [], #-e-ct
    [], #-e-d
    [21.67,   27.67,   07.67,   582.33,  248.0  ], #-s-r
    [], #-s-ct
    [], #-s-d
]

distance = [
    [3.44, 3.01, 2.21, 2.21, 1.69], #-hb-r
    [1.10, 1.15, 1.20, 1.12, 1.06], #-hb-ct
    [1.11, 1.23, 1.11, 1.23, 1.01], #-hb-d
    [], #-e-r
    [], #-e-ct
    [], #-e-d
    [3.78, 2.44, 2.02, 1.89, 1.17], #-s-r
    [], #-s-ct
    [], #-s-d
]

#######  SUCCESS PLOTS #######
fig, ax1 = plt.subplots()

a = ax1.plot(ins,suc[0], 'r.',label='HereBOY Random')
b = ax1.plot(ins,suc[1], 'r*',label='HereBOY Combinational Trojan')
c = ax1.plot(ins,suc[2], 'r^',label='HereBOY Diverse Variant')
#d = ax1.plot(ins,suc[3], 'b.',label='Exhaustive Checking Random')
#e = ax1.plot(ins,suc[4], 'b*',label='Exhaustive Checking Combinational Trojan')
#f = ax1.plot(ins,suc[5], 'b^',label='Exhaustive Checking Diverse Variant')
g = ax1.plot(ins,suc[6], 'g.',label='Stochastic Random')
#h = ax1.plot(ins,suc[7], 'g*',label='Stochastic Combinational Trojan')
#i = ax1.plot(ins,suc[8], 'g^',label='Stochastic Diverse Variant')

ax1.set_xlabel('Number of Inputs')
ax1.set_ylabel('Success Rates (%)')
ax1.set_ylim([0,100])
ax1.legend()

plt.savefig('plotting/success_plots.png')
##############################

#######  SUCCESS PLOTS #######
fig, ax1 = plt.subplots()

a = ax1.plot(ins,epochs[0], 'r.',label='HereBOY Random')
b = ax1.plot(ins,epochs[1], 'r*',label='HereBOY Combinational Trojan')
c = ax1.plot(ins,epochs[2], 'r^',label='HereBOY Diverse Variant')
#d = ax1.plot(ins,epochs[3], 'b.',label='Exhaustive Checking Random')
#e = ax1.plot(ins,epochs[4], 'b*',label='Exhaustive Checking Combinational Trojan')
#f = ax1.plot(ins,epochs[5], 'b^',label='Exhaustive Checking Diverse Variant')
g = ax1.plot(ins,epochs[6], 'g.',label='Stochastic Random')
#h = ax1.plot(ins,epochs[7], 'g*',label='Stochastic Combinational Trojan')
#i = ax1.plot(ins,epochs[8], 'g^',label='Stochastic Diverse Variant')

ax1.set_xlabel('Number of Inputs')
ax1.set_ylabel('Epochs Needed')
ax1.set_ylim([0,100])
ax1.legend()

plt.savefig('plotting/epochs_plots.png')
##############################

#######  SUCCESS PLOTS #######
fig, ax1 = plt.subplots()

a = ax1.plot(ins,distance[0], 'r.',label='HereBOY Random')
b = ax1.plot(ins,distance[1], 'r*',label='HereBOY Combinational Trojan')
c = ax1.plot(ins,distance[2], 'r^',label='HereBOY Diverse Variant')
#d = ax1.plot(ins,distance[3], 'b.',label='Exhaustive Checking Random')
#e = ax1.plot(ins,distance[4], 'b*',label='Exhaustive Checking Combinational Trojan')
#f = ax1.plot(ins,distance[5], 'b^',label='Exhaustive Checking Diverse Variant')
g = ax1.plot(ins,distance[6], 'g.',label='Stochastic Random')
#h = ax1.plot(ins,distance[7], 'g*',label='Stochastic Combinational Trojan')
#i = ax1.plot(ins,distance[8], 'g^',label='Stochastic Diverse Variant')

ax1.set_xlabel('Number of Inputs')
ax1.set_ylabel('Edit Distance / Length of Longest Tree (%)')
ax1.set_ylim([0,100])
ax1.legend()

plt.savefig('plotting/distance_plots.png')
##############################