"""
For flight, the constant is 1.52 kcal per timestep

The states are: 
0 and 2 are flying, 
1's collecting pulp, 
3 and 4 moving on the comb, 
5-9 building one wall, 
10 building a base (so depositing 4 pulp)
"""

import Karsai_neat
import numpy as np


S = int(input("how many simulations would you like to run?  ")) # number of simulations to run
T = int(input("how many time steps within a simulation?  ")) # number of timesteps
N = int(input("how many bees?  ")) # number of bees 
plotter = bool(int(input("1 for plots, 0 for no plots "))) # make plots or not
states, cells = [], []
state_results = {'flying':0, 'collecting pulp':0, 'moving on a comb':0, 'building a wall':0, 'building a base':0}

for s in range(S):
	print(f"\nsimulation run number {s+1}/{S}")
	state, cell = Karsai_neat.main(N=N,T=T,plotter=plotter)
	states.append(state)
	state_results['flying'] += state[0] + state[2]
	state_results['collecting pulp'] += state[1]
	state_results['moving on a comb'] += sum(state[3:5])
	state_results['building a wall'] += sum(state[5:10])
	state_results['building a base'] += state[10]
	cells.append(cell)

cell_average = np.mean(cells)
cell_stddev = np.std(cells)
print(f"\nRaw data of final cell numbers: \n {cells}")
print(f"\nNumber of bees = {N}\nTime = {T}")
print(f"\nAvg={cell_average:.2f}, StdDev={cell_stddev:.2f}")
print(state_results, '\n')
