import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import time
import math

def rand_place_Ez(i):
    """
    is this used for randomised excavator placement? 
    N is not passed anywhere?
    also, there seems to be nothing returned
    """
    side = rnd.random()
    if side < 0.25:
        Ez_positions[i], Ez_angles[i] = (0,rnd.randrange(0,N,1)),rnd.randrange(-180, 180)*np.pi/180
    elif side < 0.5:
        Ez_positions[i], Ez_angles[i] = (N,rnd.randrange(0,N,1)),rnd.randrange(-180, 180)*np.pi/180
    elif side < 0.75:
        Ez_positions[i], Ez_angles[i] = (rnd.randrange(0,N,1),0),rnd.randrange(-180, 180)*np.pi/180
    else:
        Ez_positions[i], Ez_angles[i] = (rnd.randrange(0,N,1),1),rnd.randrange(-180, 180)*np.pi/180
    return

def Ez_area(position, angle, detect):
    """
    This finds all the grid points in a particular Ez or in a particular detection zone
    Position and angle come from the Ez placement. Detect is a bool that says if we're detecting.
    God knows what the a_valid and b_valid is, but I trust that the coordinate change (is that what's happening here?) works. 
    Does this return a list of positions in xy coordinates that is available for detection for a particular Ez? 
    """
#    a = range(round(-2*Ez_height),round(2*Ez_height))
#    b = range(round(-2*Ez_height),round(2*Ez_height))
#    a_valid = []
#    b_valid= []
    
    # These are the grid points in a coordinate system based on the Ez's angle
    if detect:
        a_valid = [-11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6]
        b_valid = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, -4, -3, -2, -1, 0, 1, 2, 3, 4, -3, -2, -1, 0, 1, 2, 3]
    else:
        a_valid = [-9, -9, -9, -9, -9, -9, -9, -9, -9, -8, -8, -8, -8, -8, -8, -8, -8, -8, -7, -7, -7, -7, -7, -7, -7, -7, -7, -6, -6, -6, -6, -6, -6, -6, -6, -6, -5, -5, -5, -5, -5, -5, -5, -5, -5, -4, -4, -4, -4, -4, -4, -4, -4, -4, -3, -3, -3, -3, -3, -3, -3, -3, -3, -2, -2, -2, -2, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4]#[-19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -19, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -18, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -17, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -16, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -15, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -14, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -13, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -12, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -11, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -10, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -9, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -8, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -6, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -5, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9]
        b_valid = [-4, -3, -2, -1, 0, 1, 2, 3, 4, -4, -3, -2, -1, 0, 1, 2, 3, 4, -4, -3, -2, -1, 0, 1, 2, 3, 4, -4, -3, -2, -1, 0, 1, 2, 3, 4, -4, -3, -2, -1, 0, 1, 2, 3, 4, -4, -3, -2, -1, 0, 1, 2, 3, 4, -4, -3, -2, -1, 0, 1, 2, 3, 4, -4, -3, -2, -1, 0, 1, 2, 3, 4, -4, -3, -2, -1, 0, 1, 2, 3, 4, -4, -3, -2, -1, 0, 1, 2, 3, 4, -4, -3, -2, -1, 0, 1, 2, 3, 4, -3, -2, -1, 0, 1, 2, 3, -2, -1, 0, 1, 2]#[-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
    positions = []
#    for i in a:
#        for j in b:
#            if (i > ((Ez_width/2)-Ez_height-detect_length) and abs(j) < (Ez_width/2+detect_length) and i < 0) or (i > 0 and np.sqrt(i**2 + j**2) < Ez_width/2+detect_length):
#                a_valid.append(i)
#                b_valid.append(j)
#    print('AAAA', a_valid)
#    print(' ')
#    print('BBBB', b_valid)
#    print(' ')
    
    # This is a coordinate transfromation to x,y
    for i in range(len(a_valid)):
        positions.append((int(round(a_valid[i]*np.cos(angle) + b_valid[i]*np.sin(angle) + position[0])), int(round(a_valid[i]*np.sin(angle) - b_valid[i]*np.cos(angle) + position[1]))))
    return positions
                    
    

## Parameters ##
    
N = 100 # size of the simulation
initial_wax = [1, int(N/2), int(N/2)] # length/2, origin (x,y)
num_steps = 500
num_frames = 20
Ez_width = 0.1*N
Ez_height = 0.15*N
detect_length = 0.02*N
min_wax_thick = 0.02*N
area_fraction = 0.15
growth_per_iter = 1
probability_side = 0.7
rotation_step = np.sqrt(2)/(Ez_height-Ez_width/2)
linear_step = np.sqrt(2)/5


## Initialisation ##

plot = np.zeros((N,N))
# Initial wax
plot[initial_wax[1]-initial_wax[0]:initial_wax[1]+initial_wax[0],initial_wax[1]-initial_wax[0]:initial_wax[1]+initial_wax[0]] = 1
wax_x, wax_y = np.where(plot == 1)
wax = list(zip(wax_x,wax_y))
# Initialise excavation zones

# I've checked it up to here so far

area_Ez = (Ez_height-Ez_width/2)*Ez_width+(np.pi*(Ez_width)**2)/8
num_Ez = round(N*N*area_fraction/area_Ez)
Ez_positions = np.zeros(num_Ez, dtype=object)
Ez_angles = np.zeros(num_Ez, dtype=object)
for i in range(num_Ez):
    rand_place_Ez(i)
plots = []
old_plot = np.zeros((N,N))

## Run Animation ##  *Note not yet actual animation and currently only wax growth modelled
for n in range(num_steps):
    
    
    ## Wax Growth ##
    
    # Find all candidates for wax growth, this is probably a v slow way of doing it!!
    candidates_side = [] # Candidates off the side
    candidates_ends = [] # Candidates off the top or bottom
    for j in wax:
        if (j[0]+1,j[1]) not in wax and j[0]+1 < N:
            candidates_side.append((j[0]+1,j[1]))            
        if (j[0],j[1]+1) not in wax and j[1]+1 < N:
            candidates_ends.append((j[0],j[1]+1))           
        if (j[0]-1,j[1]) not in wax and j[0]-1 >= 0:
            candidates_side.append((j[0]-1,j[1]))
        if (j[0],j[1]-1) not in wax and j[1]-1 >= 0:
            candidates_ends.append((j[0],j[1]-1))
    # Break if we are full already
    if len(candidates_side) + len(candidates_ends) < growth_per_iter:
        print('Final Plot',plot)
        print('Iteration number', n,'the plot is full, break...')
        break
    # Add new wax
    if True:#n % 2 == 0:
        for i in range(growth_per_iter):
            if rnd.random() > probability_side:
                new_wax = rnd.choice(candidates_side)
            else:
                new_wax = rnd.choice(candidates_ends)
            wax.append(new_wax)
            plot[new_wax]=1
    
    
    ## Excavation Zones ##
    
    for i in range(num_Ez):        
        move = True
        
        # Check for near wax and thin walls #
        # Find any wax within detection distance of this Ez, this is super inefficient!    
        # (nb. again assuming this wax is closest to the semicricle)
        close_wax = []
        for k in Ez_area(Ez_positions[i],Ez_angles[i],True):
            if k in wax:
                close_wax.append(k)
        
        # If there is close wax
        if close_wax != []:            
            # Find the angle between some of the close wax and the Ez
            random_wax = rand.choice(close_wax)
            Ez_wax_angle = np.arctan((Ez_positions[i][1]-random_wax[1])/(Ez_positions[i][0]-random_wax[0]))
            #print('close!', n)
            # Check for thin walls #
            # If the wax is in front and there's no wax min_wax_thick away from the current position
            r = (round(Ez_positions[i][0] - ((Ez_width/2)+min_wax_thick)*np.cos(Ez_wax_angle)), round(Ez_positions[i][1] - ((Ez_width/2)+min_wax_thick)*np.sin(Ez_wax_angle)))
            if (r not in wax):# or ((r[0]+1,r[1]+1) not in wax) or ((r[0],r[1]+1) not in wax) or ((r[0]+1,r[1]) not in wax) or ((r[0]-1,r[1]-1) not in wax) or ((r[0]-1,r[1]) not in wax) or ((r[0],r[1]-1) not in wax) or ((r[0]+1,r[1]-1) not in wax) or ((r[0]-1,r[1]+1) not in wax): #(Ez_wax_angle < 0.1 or Ez_wax_angle > 0.1) and 
                # if we can, twist up
                move = False
                #print('thin!', n)
                if rnd.random() > 0.5: 
                    r = (round(Ez_positions[i][0] - ((Ez_width/2)+min_wax_thick)*np.cos(Ez_wax_angle+rotation_step)), round(Ez_positions[i][1] - ((Ez_width/2)+min_wax_thick)*np.sin(Ez_wax_angle+rotation_step)))
                    if (r in wax):# and ((r[0]+1,r[1]+1) in wax) and ((r[0],r[1]+1) in wax) and ((r[0]+1,r[1]) in wax) and ((r[0]-1,r[1]-1) in wax) and ((r[0]-1,r[1]) in wax) and ((r[0],r[1]-1) in wax) and ((r[0]+1,r[1]-1) in wax) and ((r[0]-1,r[1]+1) in wax): #(Ez_wax_angle < 0.1 or Ez_wax_angle > 0.1) and 
                        #print('up', n)
                        Ez_wax_angle = Ez_wax_angle + rotation_step
                else:
                    # if we can, twist down
                    r = (round(Ez_positions[i][0] - ((Ez_width/2)+min_wax_thick)*np.cos(Ez_wax_angle-rotation_step)), round(Ez_positions[i][1] - ((Ez_width/2)+min_wax_thick)*np.sin(Ez_wax_angle-rotation_step)))
                    if (r in wax):# and ((r[0]+1,r[1]+1) in wax) and ((r[0],r[1]+1) in wax) and ((r[0]+1,r[1]) in wax) and ((r[0]-1,r[1]-1) in wax) and ((r[0]-1,r[1]) in wax) and ((r[0],r[1]-1) in wax) and ((r[0]+1,r[1]-1) in wax) and ((r[0]-1,r[1]+1) in wax): #(Ez_wax_angle < 0.1 or Ez_wax_angle > 0.1) and 
                        #print('down', n)
                        Ez_wax_angle = Ez_wax_angle - rotation_step
            if Ez_wax_angle > Ez_angles[i]:
                Ez_angles[i] += rotation_step
            else:
                Ez_angles[i] += -rotation_step
                    
        # Unless we're staying put, take a step
        if move:
            Ez_positions[i] = (Ez_positions[i][0] + (linear_step)*np.cos(Ez_angles[i]), Ez_positions[i][1] + (linear_step)*np.sin(Ez_angles[i]))
            # And scroll over edges
            if Ez_positions[i][0] > N:
                Ez_positions[i] = (Ez_positions[i][0]-N, Ez_positions[i][1])
            if Ez_positions[i][1] > N:
                Ez_positions[i] = (Ez_positions[i][0], Ez_positions[i][1]-N)
            if Ez_positions[i][0] < 0:
                Ez_positions[i] = (Ez_positions[i][0]+N, Ez_positions[i][1])
            if Ez_positions[i][1] < 0:
                Ez_positions[i] = (Ez_positions[i][0], Ez_positions[i][1]+N)
        
        # Check for hitting another bee #
        # (nb. we're currently assuming all collisions happen on the semicircles)
        for f in range(num_Ez):
            if f != i and np.sqrt((Ez_positions[i][0]-Ez_positions[f][0])**2 + (Ez_positions[i][1]-Ez_positions[f][1])**2)  < Ez_width:
                rand_place_Ez(i)                
                #if i == 0:
                    #print('Teleported :o', i)
        
        # Now actually remove wax!
        for k in Ez_area(Ez_positions[i],Ez_angles[i],False):
            if k in wax:
                plot[k] = 0
                wax.remove(k)   
             
    #print(Ez_positions[0],Ez_angles[0])
    # Save some frames
    if n % (num_steps/num_frames) == 0:
       print('Plot number', n)
       saved_plot = plot.copy()
       j = 0
       for i in range(len(Ez_positions)):
           j += 1
           for i in Ez_area(Ez_positions[i],Ez_angles[i],False):
               try:
                   saved_plot[i] = j/num_Ez
               except:
                   pass
           #saved_plot[int(round(i[0]))-5:int(round(i[0]))+3,int(round(i[1]))-5:int(round(i[1]))+3] = j/num_Ez
       plots.append((n,saved_plot))

#plt.imshow(plot, cmap='hot', interpolation='nearest')
    #title = 'Iteration Number ' + str(i[0])
    #plt.title(title)
#plt.show()

fig, ax_lst = plt.subplots(int(num_frames/5),5)
ax_lst = ax_lst.ravel()

data = np.random.rand(N, N)
for i in range(num_frames):
    im = ax_lst[i].imshow(plots[i][1])

#for i in range(len(plots)):
#    t_start = time.time()
#    data = plots[i][1]
#    im.set_data(data) 
#    plt.pause(0.5)
#    t_end = time.time()
#    print("fps = {0}".format(999 if t_end == t_start else 1/(t_end-t_start)))


