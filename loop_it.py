"""
For flight, the constant is 1.52 kcal per timestep
For building it's 1.26 kcal per cell

The states are: 
0 and 2 are flying, 
1's collecting pulp, 
3 and 4 moving on the comb, 
5-9 building one wall, 
10 building a base (so depositing 4 pulp)
"""

import Karsai_neat
import numpy as np


def calculate_energy(s_r, c_a):
	'''
	a function to calculate the energy expenditure of building a nest
	units are kcal/cell
	s_e is state energy - that's the result
	c_a is average cell number reported by the simulation
	'''

	flight_cost = 1
	deposition_cost = 3
	moving_cost = 0
	collection_cost = 0

	s_e = s_r.copy()

	s_e['flying'] *= flight_cost
	s_e['collecting pulp'] *= collection_cost
	s_e['moving on a comb'] *= moving_cost
	s_e['building'] = (s_e['building a wall'] + 4 * s_e['building a base']) * deposition_cost 

	s_e.pop('building a wall'); s_e.pop('building a base')

	return s_e

S = int(input("how many simulations would you like to run?  ")) # number of simulations to run
T = int(input("how many time steps within a simulation?  ")) # number of timesteps
N = int(input("how many bees?  ")) # number of bees 
huj = input('To use stock parameters press ENTER\nOtherwise Dparams in format 0,1,2,3,4,5: ')
try:
	Dparams = [float(i) for i in huj.split(',')]
except:
	Dparams = [0,0,0.1,0.5,0.8,0.9]
# plotter = bool(int(input("1 for plots, 0 for no plots "))) # make plots or not
states, cells, figures = [], [], []
state_results = {'flying':0, 'collecting pulp':0, 'moving on a comb':0, 'building a wall':0, 'building a base':0}

s = 0
while s < S:
	try:
		print(f"\nsimulation run number {s+1}/{S}")
		state, cell, fig = Karsai_neat.main(N=N,T=T,Dparams=Dparams)
		states.append(state)
		state_results['flying'] += (state[0] + state[2])/S
		state_results['collecting pulp'] += state[1]/S
		state_results['moving on a comb'] += sum(state[3:5])/S
		state_results['building a wall'] += sum(state[5:10])/S
		state_results['building a base'] += state[10]/S
		cells.append(cell)
		figures.append(fig)
		s += 1

	except Exception as ex:
		print('simulation failed')
		print(ex)

cell_average = np.mean(cells)
cell_stddev = np.std(cells)
energy_results = calculate_energy(state_results,cell_average)

print(f"\nNumber of bees = {N}\nTime = {T}")
print(f"\nRaw data of final cell numbers: \n {cells}")
print(f"Avg={cell_average:.2f}, StdDev={cell_stddev:.2f}\n")
print(state_results, '\n')
print('energy costs:\n', energy_results, '\n')

