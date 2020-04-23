import Karsai_neat
import numpy as np


S = int(input("how many simulations would you like to run?  ")) # number of simulations to run
T = int(input("how many time steps within a simulation?  ")) # number of timesteps
N = int(input("how many bees?  ")) # number of bees 
plotter = bool(int(input("1 for plots, 0 for no plots "))) # make plots or not
states, cells = [], []

for s in range(S):
	print(f"simulation run number {s+1}/{S}")
	state, cell = Karsai_neat.main(N=N,T=T,plotter=plotter)
	states.append(state)
	cells.append(cell)

cell_average = np.mean(cells)
cell_stddev = np.std(cells)
print(f"\nRaw data of final cell numbers: \n {cells}")
print(f"\nNumber of bees = {N}\nTime = {T}")
print(f"\nAvg={cell_average:.2f}, StdDev={cell_stddev:.2f}")
