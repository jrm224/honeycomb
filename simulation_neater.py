# Put imports here
import matplotlib.pyplot as plt
import numpy as np
import random as rand
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (QVBoxLayout, QSlider, QDialog)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QBrush, QPen, QPolygon
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import copy

def calculate_action(bee_state, hive, parameters):
    """
    calculate the action for a particular bee to take in a timestep
    """
    N, Fp, Lu, Ds, D, move_parameters = parameters
    position, orientation, load, state, wall_number = bee_state
        
    ## Searching for Pulp ##
    if state == 0:   
        if rand.random() <= Fp:
            return [position, orientation, load, state + 1, wall_number]
        else:
            return bee_state
    
    ## Collecting Pulp ##
    elif state  == 1:
        load += 1
        if load == Lu:
            return [position, orientation, load, state + 1, wall_number]
        else:
            return [position, orientation, load, state, wall_number]
    
    ## Coming in to land ##
    elif state  == 2: 
        occupied, side, site, edges = find_landing_site(hive)        
        if occupied: # Failed to land, site was occupied
            return [position, orientation, load, state, wall_number]        
        elif side: # Landed on side
            hive.get_cells()[site].toggle_bee(True)
            return [site, rand.randint(0, 5), load, state + 1, wall_number]        
        else: # Landed on face
            hive.get_cells()[site].toggle_bee(True)            
            return [site, rand.randint(0, 5), load, state + 2, wall_number]
    
    ## Landed on Side, Move off the Side ##
    elif state  == 3:   
        # Find all possible turns
        cells = hive.get_cells().keys()
        x,y = position
        edges = check_for_edges(x,y,cells)
        poss_turns = [0,1,2,3,4,5]        
        # Remove any that represents a side
        for i in edges:
            poss_turns.remove(i)            
        # Choose from the not side options
        return [position, rand.choice(poss_turns), load, state + 1, wall_number]
    
    ## Arrived on the Face ##
    elif state  == 4:  
        # Find the number of tall walls
        walls = hive.get_cells()[position].walls
        tall_walls = np.where(walls>5)
        
        if len(tall_walls[0]) == 0: # it's a Small Cell we're very likely to stay            
            if rand.random() <= Ds: # We're staying, go to the build state
                return [position, orientation, load, state + 1, wall_number]            
            else: # We're moving, use the 'move' function
                movement = move(position, orientation, hive, move_parameters)
                if movement[0] != position:
                    hive.get_cells()[movement[0]].toggle_bee(True)
                    hive.get_cells()[position].toggle_bee(False)
                return [movement[0], movement[1], load, state, wall_number]
            
        else:  # it's not a Small cell, chance of staying depends on the num of tall walls
            if rand.random() <= D[len(tall_walls[0])]: # We're staying, go to the build state
                return [position, orientation, load, state + 2, wall_number]
            else: # We're moving, use the 'move' function
                movement = move(position, orientation, hive, move_parameters)
                if movement[0] != position:
                    hive.get_cells()[movement[0]].toggle_bee(True)
                    hive.get_cells()[position].toggle_bee(False)
                return [movement[0], movement[1], load, state, wall_number]
        
    ## Building a Small Cell ##
    elif state == 5:
        # If we're new here, choose any wall to start building     
        if wall_number == 99:  
            wall_number = rand.randint(0,5)
            load += -1
            hive.grow_cells(position, wall_number)
            return [position, orientation, load, state, wall_number]
        # From then on just go around the cell       
        else:  
            wall_number += 1
            wall_number = wall_number%6
            load += -1
            hive.grow_cells(position, wall_number)
            # If we're now empty remove the bee and reset
            if load == 0: 
                hive.get_cells()[position].toggle_bee(False)            
                return [(999,999), 0, 0, 0, 99]
            else:
                return [position, orientation, load, state, wall_number]
        
    ## Building a Large Cell ##
    elif state == 6:
        # Check if we're on the side
        cells = hive.get_cells().keys()
        x,y = position
        edges = check_for_edges(x,y,cells)
        
        # We're not on the side so lengthen
        if edges == []:  
            # Pick a valid wall to start on
            walls = hive.get_cells()[position].walls
            candidates = []
            for i in range(6):
                if walls[i] != max(walls) and walls[(i+1)%6] == max(walls):
                    candidates.append((i,True))
                if walls[i] != max(walls) and walls[(i-1)%6] == max(walls):
                    candidates.append((i,False))
            wall_number = rand.choice(candidates)            
            # Grow that wall
            hive.grow_cells(position,wall_number[0])
            load += -1
             # If we're empty remove bee and reset
            if load == 0:
                hive.get_cells()[position].toggle_bee(False)            
                return [(999,999), 0, 0, 0, 99]            
            # Otherwise continue in either the positive or negative direction
            elif wall_number[1]:
                return [position, orientation, load, state + 1, wall_number[0]]
            else:
                return [position, orientation, load, state + 2, wall_number[0]]
            
        # We're on the side so initiate
        else:  
            hive.add_cells(position, edges)
            load += -4
            return [position, orientation, load, state + 3, wall_number]
    
    ## Lengthen in the Positive Direction ##
    elif state == 7: 
        wall_number += 1
        hive.grow_cells(position,wall_number%6)
        load += -1
        if load == 0:
            hive.get_cells()[position].toggle_bee(False)            
            return [(999,999), 0, 0, 0, 99]
        else:
            return [position, orientation, load, state, wall_number]
    
    ## Lengthen in the Negative Direction ##
    elif state == 8:
        wall_number += -1
        hive.grow_cells(position,wall_number%6)
        load += -1
        if load == 0:
            hive.get_cells()[position].toggle_bee(False) 
            return [(999,999), 0, 0, 0, 99]
        else:
            return [position, orientation, load, state, wall_number]
    
    ## Build a Newly Initiated Cell ##
    elif state == 9:
        # Pick a valid wall to start on
        walls = hive.get_cells()[position].walls
        candidates = []
        for i in range(6):
            if walls[i] != max(walls) and walls[(i+1)%6] == max(walls):
                candidates.append((i,True))
            if walls[i] != max(walls) and walls[(i+1)%6] == max(walls):
                candidates.append((i,False))
        wall_number = rand.choice(candidates)
        # Grow that wall
        hive.grow_cells(position,wall_number[0])
        load += -1
        # If we're empty remove the bee and reset
        if load == 0:
            hive.get_cells()[position].toggle_bee(False)            
            return [(999,999), 0, 0, 0, 99]
        # Otherwise continue either in the positive or negative direction
        elif wall_number[1]:
            return [position, orientation, load, 7, wall_number[0]]
        else:
            return [position, orientation, load, 8, wall_number[0]]    
    
def move(position, orientation, hive, parameters):
    """
    defines movement of a bee
    """
    Am, ASm, Bm, BSm = parameters
    X = rand.random()
    if X <= Am:
        return move_given_orientation(position, orientation, hive)
    elif X <= Am + ASm:
        if rand.random() <= 0.5:
            return move_given_orientation(position, (orientation+1)%6, hive)
        else:
            return move_given_orientation(position, (orientation-1)%6, hive)
    elif X <= Am + ASm + Bm:
        return move_given_orientation(position, (orientation+3)%6, hive)
    else:# X <= Am + ASm + Bm + BSm:
        if rand.random() <= 0.5:
            return move_given_orientation(position, (orientation+4)%6, hive)
        else:
            return move_given_orientation(position, (orientation+2)%6, hive)
    
def move_given_orientation(position, orientation, hive):
    """
    find the position given by moving along orientation and checks for a bee
    """
    if orientation ==0:
        new_position = (position[0]+1, position[1])
        if new_position not in hive.get_cells().keys():
            return position, orientation
        elif hive.get_cells()[new_position].bee:
            return position, orientation
        else:
            return new_position, orientation
    if orientation ==1:
        new_position = (position[0]+1, position[1]-1)
        if new_position not in hive.get_cells().keys():
            return position, orientation
        elif hive.get_cells()[new_position].bee:
            return position, orientation
        else:
            return new_position, orientation
    if orientation ==2:
        new_position = (position[0], position[1]-1)
        if new_position not in hive.get_cells().keys():
            return position, orientation
        elif hive.get_cells()[new_position].bee:
            return position, orientation
        else:
            return new_position, orientation
    if orientation ==3:
        new_position = (position[0]-1, position[1])
        if new_position not in hive.get_cells().keys():
            return position, orientation
        elif hive.get_cells()[new_position].bee:
            return position, orientation
        else:
            return new_position, orientation
    if orientation ==4:
        new_position = (position[0]-1, position[1]+1)
        if new_position not in hive.get_cells().keys():
            return position, orientation
        elif hive.get_cells()[new_position].bee:
            return position, orientation
        else:
            return new_position, orientation
    if orientation ==5:
        new_position = (position[0], position[1]+1)
        if new_position not in hive.get_cells().keys():
            return position, orientation
        elif hive.get_cells()[new_position].bee:
            return position, orientation
        else:
            return new_position, orientation
        
def find_landing_site(hive):
    """
    find a random unoccupied landing site on the hive
    """
    cells = list(hive.get_cells().keys())
    x,y = rand.choice(cells)
    if hive.get_cells()[(x,y)].bee: # Another bee there, abort
        return [True, False, (0,0), []]
    edges = check_for_edges(x,y,cells)
    if edges != []:
        return [False, True, (x,y), edges] # Landed on the side
    else:
        return [False, False, (x,y), []] # Landed on the face

def check_for_edges(x,y,cells):
    """ 
    Return the possible turns towards the hive for a bee on the edge
    """
    edges = []
    if (x+1, y) not in cells:
        edges.append(0)
    if (x-1, y) not in cells:
        edges.append(3)
    if (x, y+1) not in cells:
        edges.append(5)
    if (x, y-1) not in cells:
        edges.append(2)
    if (x+1, y-1) not in cells:
        edges.append(1)
    if (x-1, y+1) not in cells:
        edges.append(4)
    return edges
    
def initialise_bees(N):
    """
    initialise N Bee classes in a list
    """
    bees = []
    for i in range(N):
        bees.append(Bee([(999.999),0,0,0,99]))
    return bees

# Classes here

class Hive:
    """
    holds information on individual cells, accesses cells and performs operations on cells and cell walls
    """
    def __init__(self):
        # Initialise 2 cells with walls of height 6 surrounded by cells of height 0 (ie. 'sides') 
        self.cells = {}
        for i in range(10):
            if i < 4:
                self.cells[(i-1,0)] = copy.deepcopy(Cell(position=(i-1,0)))
            elif i < 7:
                self.cells[(i-5,1)] = copy.deepcopy(Cell(position=(i-5,1)))
            else:
                self.cells[(i-7,-1)] = copy.deepcopy(Cell(position=(i-7,-1)))
        for j in range(6):
            self.cells[(0,0)].grow_wall(j)
            self.cells[(1,0)].grow_wall(j)
        #self.cells = {(0,0):Cell(position=(0,0)),(1,0):Cell(position=(1,0))}	# use tuple as key and position (keys in python dicts have to be immutable)
    
    def get_cells(self):
        return self.cells
        
    def grow_cells(self, position, wall):
        self.cells[position].grow_wall(wall)
        
    def add_cells(self, position, edges):
        # Add zero height cells to all adjacent positions, this is because the cell we're on has become a cell rather than a 'side' 
        x,y = position
        for i in edges:
            if i == 0:
                self.cells[(x+1,y)] = copy.deepcopy(Cell(position=(x+1,y)))
            if i == 1:
                self.cells[(x+1,y-1)] = copy.deepcopy(Cell(position=(x+1,y-1)))
            if i == 2:
                self.cells[(x,y-1)] = copy.deepcopy(Cell(position=(x,y-1)))
            if i == 3:
                self.cells[(x-1,y)] = copy.deepcopy(Cell(position=(x-1,y)))
            if i == 4:
                self.cells[(x-1,y+1)] = copy.deepcopy(Cell(position=(x-1,y+1)))
            if i == 5:
                self.cells[(x,y+1)] = copy.deepcopy(Cell(position=(x,y+1)))
        
class Cell:
    """
    holds information about own walls (height), and whether there'sa bee present
    
    NOTES
    """
    
    def __init__(self, position, walls=np.zeros(6)):
        # initialises the cell, by default with walls of height 0
        self.position = position	# (x,y), position within the beehive, gets passed to the cell when the cell gets initiated
        self.walls = walls		# wall height where wall id is the index in that list and the value is the wall height
        self.bee = False
    
    def toggle_bee(self,toggle):
        self.bee = toggle
        
    def grow_wall(self, wall):
        # grows a certain wall cell
        self.walls[wall] += 1	
    

class Bee:
    """
    defines bee's behaviour. holds information on position, orientation (?), flying/not flying, weight of carried pulp...
    
    NOTES
    position = [(x,y), orientation, load, state, wall_number]
    """
    def __init__(self, position):
        self.position = position
    
    def get_current_state(self):
        return self.position
        
    def request_action(self, action):
        self.position = action
        
class Viewer(QDialog):
    """
    defines how the GUI and the display looks like, I never developed this 
    """
#    def __init__(self):
#        super().__init__()
#        self.initUI()
#        
#    def initUI(self):  
#        
#        self.setWindowTitle('Parsai & Penzes 1992 Simulation')
#        
#        self.simulation = pg.PlotWidget()
#        self.simulation.plot([0,0,0],[1,1,1])
#        
#        self.time_slider = QSlider(Qt.Horizontal)
#        
#        self.layout = QVBoxLayout()
#        
#        self.layout.addWidget(self.simulation)           
#        self.layout.addWidget(self.time_slider)
#        
#        self.setLayout(self.layout)
#        self.show()    
#        
#    def update_gui(self, hive):
#        cells = hive.get_cells().keys()
##        for i in cells:
##            painter = QPainter()
##            painter.setPen(QPen(Qt.black,  3, Qt.SolidLine))
##            x,y = i
##            points = [QPoint(x+5,y+10), QPoint(x+10,y), QPoint(x+5,y-10), QPoint(x-5,y-10), QPoint(x-10,y), QPoint(x-5,y+10)]
##            poly = QPolygon(points)
##            painter.drawPolygon(poly)
#            
#    def get_params(self):
#        print("N, Fp, Lu, Ds, D0-5, Am, ASm, Bm, BSm")
#        return [10,0.25,9,0.95,[0,0,0.1,0.5,0.8,0.9],[0.5,0.2,0.02,0.04]]#[input() , input(), input(), [input(), input(), input(), input(), input(), input()], [input(), input(), input(), input()]]

# Actual code to run here
#viewer = Viewer()
    
def line(pos0,pos1):
    """
    This give the x and y values of a line between two points
    """
    x0, y0 = pos0
    x1, y1 = pos1
    xpoints = []
    ypoints = []
    for i in range(100):
        xpoints.append(x0 + i/100*(x1-x0))
        ypoints.append(y0 + i/100*(y1-y0))
    return xpoints, ypoints

def hexagon(position,r):
    """
    This gives the x and y valeus of a hexagon of a particular size at given it's centre point
    """
    x,y = position
    long = np.sqrt((4/3)*r**2)
    short = r
    xpoints = line((x,y+long),(x+short,y+long/2))[0]+line((x+short,y+long/2),(x+short,y-long/2))[0]+line((x+short,y-long/2),(x,y-long))[0]+line((x,y-long),(x-short,y-long/2))[0]+line((x-short,y-long/2),(x-short,y+long/2))[0]+line((x-short,y+long/2),(x,y+long))[0]
    ypoints = line((x,y+long),(x+short,y+long/2))[1]+line((x+short,y+long/2),(x+short,y-long/2))[1]+line((x+short,y-long/2),(x,y-long))[1]+line((x,y-long),(x-short,y-long/2))[1]+line((x-short,y-long/2),(x-short,y+long/2))[1]+line((x-short,y+long/2),(x,y+long))[1]
    return xpoints, ypoints

def arrow(position,orientation):
    """
    This gives the x and y values of an arrow in a particular orientation at a particular position.
    This was to reprsent a bee but didn't work well and is no longer used, instead bees are represented by two small hexagons.
    """
    x,y = position
    if orientation == 0:
        sin = 0
        cos = 1
    if orientation == 1:
        sin = 0.5
        cos = -np.sqrt(3)/2
    if orientation == 2:
        sin = -0.5
        cos = -np.sqrt(3)/2
    if orientation == 3:
        sin = 0
        cos = -1
    if orientation == 4:
        sin = -0.5
        cos = np.sqrt(3)/2
    if orientation == 5:
        sin = 0.5
        cos = np.sqrt(3)/2
    xpoints = line((x-cos,y-cos),(x+cos,y+sin))[0] + line((x+cos*3/4,y),(x+cos,y+sin))[0]+ line((x,y+sin*3/4),(x+cos,y+sin))[0]
    ypoints = line((x-cos,y-cos),(x+cos,y+sin))[1] + line((x+cos*3/4,y),(x+cos,y+sin))[1]+ line((x,y+sin*3/4),(x+cos,y+sin))[1]
    return xpoints, ypoints





### Main Loop ###
    
# Manually set parameters since I never develoepd the viewer 
#             [N,   Fp, Lu,   Ds,                          D0-5, [ Am, ASm,   Bm,  BSm]
parameters =  [4, 0.25,  9, 0.95, [0.2,0.2,0.3,0.5,0.8,0.9,0.2], [0.5, 0.2, 0.02, 0.04]] #viewer.get_params()

# Initialise N bees
N = parameters[0]
bees = initialise_bees(N)

# Initialise the hive
hive = Hive()

# Viewer was never developed
#viewer.update_gui(hive)



## Simulation ##

# For each bee at each time step get it's state and then using it's state calculate it's action
data = []
for t in range(1001):
    if t % 250 == 0:
        print('Time Step ', t, ' of 1001')
    for bee in bees:
        bee_state = bee.get_current_state()
        bee.request_action(calculate_action(bee_state, hive, parameters))        
    # Then record the state of the hive at each time step for plotting
    data.append(copy.deepcopy(hive.get_cells()))
    
    
    
## Plotter ##   (since the Viewer was never Developed)
    
# Set up axes for plot of four timesteps
fig, ax_lst = plt.subplots(2,2)
ax_lst = ax_lst.ravel()
for i in range(4):
    print('Plotting Subplot ', i,' of 4')
    # Create lists for the x and y values of lines in the plot and their colour
    x = []
    y = []
    C = []
    
    # On each plot, plot each cell as a large hexagon with a smaller hexagon within it that's coloured by it's average height
    for cell in list(data[i*250].keys()):
        # Convert to hexagonal coordinate system
        x_ = (cell[0] + cell[1]/2)*10
        y_ = (cell[1]*np.sqrt(3)/2)*10     
        # Record x and y values
        if height != 0:
            x = x + hexagon((x_,y_),5)[0] + hexagon((x_,y_),4)[0]
            y = y + hexagon((x_,y_),5)[1] + hexagon((x_,y_),4)[1]
            # Record Colour, colour = 0 for the outer hexagon and the average height for the inner
            for j in range(600):
                C.append(0)
            for k in range(600):
                C.append(np.mean(data[i*250][cell].walls.copy()))
                
        # This optionally plots the side as smaller hexagons                
        #else:
        #    x = x + hexagon((x_,y_),2)[0]
        #    y = y + hexagon((x_,y_),2)[1]
        #    for j in range(600):
        #        C.append(0)
        
        # Then add the bees as two smaller hexagons colour = 5
        if data[i*250][cell].bee:
            x = x + hexagon((x_-1,y_),1)[0]+ hexagon((x_+1,y_),1)[0]
            y = y + hexagon((x_-1,y_),1)[1]+ hexagon((x_+1,y_),1)[1]
            for j in range(1200):
                C.append(5)
            
# I think this was an old way of converting coordinates that can now be ignored    
#        print(data[i*500][cell].walls)
#    x = [x for _,x in sorted(zip(C,x), reverse = True)]
#    y = [x for _,x in sorted(zip(C,y), reverse = True)]
#    C = sorted(C, reverse = True)
#    x = [ x + y/2 for x, y in data[i*100] ]
#    y = [ y*np.sqrt(3)/2 for x, y in data[i*100] ]
#    print(x,y)
    
    # Plot on a hexbin heatmap
    im = ax_lst[i].hexbin(x,y,C, gridsize = 1000)
# Add one colour bar to the whole plot (not one for each subplot)
cb = fig.colorbar(im, ax=ax_lst)