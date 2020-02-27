# Put imports here
import matplotlib.pyplot as plt
import numpy as np
import random as rnd

# Actual code to run here


# Classes here

class Hive:
	"""
	holds information on individual cells, accesses cells and performs operations on cells and cell walls
	"""
	def __init__(self):
		self.cells = {(0,0):Cell(position=(0,0))}	# use tuple as key and position (keys in python dicts have to be immutable)

class Cell:
	"""
	holds information about own walls (height) and base (built, not built)
	
	NOTES
	in contrast to what we've discussed before, I reckon numbering the walls 0-5 clockwise is the best option (easier to determine which cells grow in what turns etc)
	"""
	def __init__(self, position, walls=np.zeros(6)):
		# initialises the cell, by default with walls of height 0
		self.position = position	# (x,y), position within the beehive, gets passed to the cell when the cell gets initiated
		self.walls = walls		# wall height where wall id is the index in that list and the value is the wall height
	
	def grow_wall(self, wall=0):
		# grows a certain wall cell
		self.walls[wall] += 1	

class Bee:
	"""
	defines bee's behaviour. holds information on position, orientation (?), flying/not flying, weight of carried pulp...
    
    NOTES
    I think we can contain all useful information in position and pulp where position = [x,y,theta] and then if it's flying we can set [999,999,0] or something like that
	I think the only action Bee class has to make is updating it's position, so we may as well just pass it's new position to it as it depends on the hive class
    """
    def __init__(self, position):
        self.position = position
        self.pulp = 0
    
    def get_current_state():
        return self.position, self.pulp
        
    def request_action(action):
        self.position = action
        
class Viewer:
	"""
	defines how the GUI and the display looks like 
	"""

