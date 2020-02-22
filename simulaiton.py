# Put imports here
import matplotlib.pyplot as plt
import numpy

# Actual code to run here


# Classes here

class Hive:
	"""
	holds information on indivudal cells, accesses cells and performs operations on cells and cell walls
	"""
	def __init__(self):
		

class Cell:
	"""
	holds information about own walls (height) and base (built, not built)
	"""
	def __init__(self, position):
		self.position = position	# [x,y], position within the beehive, gets passed to the cell when the cell gets initiated
		self.walls = [0,0,0,0,0,0]	# wall height where wall id is the index in that list and the value is the wall height
	
	

class Bee:
	"""
	defines bee's behaviour. holds information on position, orientation (?), flying/not flying, weight of carried pulp...
	"""

class Viewer:
	"""
	defines how the GUI and the display looks like 
	"""

