import Karsai_neat
import numpy as np


S = int(input("how many simulations would you like to run?  ")) # number of simulations to run
T = int(input("how many time steps within a simulation?  ")) # number of timesteps
N = int(input("how many bees?  ")) # number of bees

states, cells = [], []

for s in range(S):
	print("simulation run number {}".format(s))
	state, cell = Karsai_neat.main(N=N,T=T)
	states.append(state)
	cells.append(cell)

cell_average = np.mean(cells)
print("\nRaw data of final cell numbers: \n {}".format(cells))
print("\nNumber of bees = {}\nTime = {}\nCell average:  {}".format(N,T,cell_average))
