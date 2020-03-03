# Put imports here
import matplotlib.pyplot as plt
import numpy as np
import random as rnd

# Actual code to run here
viewer = Viewer()
parameters = viewer.get_params()
N = parameters[0]
bees = initialise_bees(N)
hive = Hive()
for t in range(T):
    for bee in bees:
        bee_state = bee.get_current_state()
        bee.request_action(calculate_action(bee_state, hive, parameters))
        hive.set_cells()
        
def calculate_action(bee_state, hive, parameters):
    """
    calculate the action for a particular bee to take in a timestep
    """
    N, Fp, Lu = parameters
    position, orientation, load, state = bee_state
    if state == 0:   # Searching for Pulp
        if rand.random() <= Fp:
            return [position, orientation, load, state + 1]
        else:
            return bee_state
        
    elif state  == 1:   # Collecting Pulp
        load = load + 1
        if load == Lu:
            return [position, orientation, load, state + 1]
        else:
            return bee_state
        
    elif state  == 2:   # Coming in to land
        occupied, side, site, edges = find_landing_site(hive)
        if occupied: # Failed to land, site was occupied
            return bee_state 
        elif side: # Landed on side
            return [site, rand.randint(6), load, state + 1] 
        else: # Landed on face
            return [site, rand.randint(6), load, state + 2]
    
    elif state  == 3:   # Just landed on the side
        return [position, rand.choice(edges), load, state + 1] # Turn to face
    
    elif state  == 4:   # On the face`
        
        
def find_landing_site(hive):
    """
    find a random unoccupied landing site on the hive
    """
    cells = hive.get_cells().keys()
    x,y = rand.choice(cells)
    if hive.get_cells()((x,y)).bee: # Another bee there, abort
        return [True, False, (0,0), []]
    edges = check_for_edges(x,y,cells)
    elif  edges != []:
        return [False, True, chosen_site, edges] # Landed on the side
    else:
        return [False, False, chosen_site, []] # Landed on the face

def check_for_edges(x,y,cells):
    """ 
    Return the possible turns towards the hive for a bee on the edge
    """
    edges = [0,1,2,3,4,5]
    if (x+1, y) not in cells:
        edges.remove(0)
    if (x-1, y) not in cells:
        edges.remove(3)
    if (x, y+1) not in cells:
        edges.remove(5)
    if (x, y-1) not in cells:
        edges.remove(2)
    if (x+1, y-1) not in cells:
        edges.remove(1)
    if (x-1, y+1) not in cells:
        edges.remove(4)
    return edges
    
def initialise_bees(N):
    """
    initialise N Bee classes in a list
    """
    bees = []
    for i in range(N):
        bees.append(Bee([(999.999),0]))
    return bees

# Classes here

class Hive:
	"""
	holds information on individual cells, accesses cells and performs operations on cells and cell walls
	"""
	def __init__(self):
		self.cells = {(0,0):Cell(position=(0,0))}	# use tuple as key and position (keys in python dicts have to be immutable)
    
    def get_cells(self):
        return self.cells
        
    def grow_cells(self, action):
        Cell.grow_wall(action)
        
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
	    self.bee = False
    
    def landing(self):
        self.bee = True
        
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
    
    def get_current_state(self):
        return self.position, self.pulp
        
    def request_action(self, action):
        self.position = action
        
class Viewer:
	"""
	defines how the GUI and the display looks like 
	"""

