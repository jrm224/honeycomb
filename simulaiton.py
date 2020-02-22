# Put imports here
import matplotlib.pyplot as plt
import numpy as np

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
	
	NOTES
	in contrast to what we've discussed before, I reckon numbering the walls 0-6 clockwise is the best option (easier to determine which cells grow in what turns etc)
	"""
	def __init__(self, position, walls=np.zeros(6)):
		# initialises the cell, by default with walls of height 0
		self.position = position	# [x,y], position within the beehive, gets passed to the cell when the cell gets initiated
		self.walls = walls		# wall height where wall id is the index in that list and the value is the wall height
	
	def grow_wall(self, wall=0):
		# grows a certain wall cell
		self.walls(wall) += 1
	
	

class Bee:
	"""
	defines bee's behaviour. holds information on position, orientation (?), flying/not flying, weight of carried pulp...
	"""

class Viewer:
	"""
	defines how the GUI and the display looks like 
	"""

