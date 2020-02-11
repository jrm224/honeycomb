import numpy as np
import random as rnd
import matplotlib.pyplot as plt
import time

def rand_place_Ez(i):
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

## Parameters ##
N = 200
initial_wax = [1, int(N/2), int(N/2)] # length/2, origin (x,y)
num_steps = 1000
num_frames = 20
Ez_width = 0.1*N
Ez_height = 0.15*N
detect_length = 0.02*N
min_wax_thick = 0.02*N
area_fraction = 0.15
growth_per_iter = 1
probability_side = 0.7

## Initialisation ##
plot = np.zeros((N,N))
# Initial wax
plot[initial_wax[1]-initial_wax[0]:initial_wax[1]+initial_wax[0],initial_wax[1]-initial_wax[0]:initial_wax[1]+initial_wax[0]] = 1
wax_x, wax_y = np.where(plot == 1)
wax = list(zip(wax_x,wax_y))
# Initialise excavation zones
area_Ez = (Ez_height-Ez_width/2)**2+(np.pi*(Ez_width/2)**2)/2
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
    for i in range(growth_per_iter):
        side_or_end = rnd.random()
        if side_or_end > probability_side:
            new_wax = rnd.choice(candidates_side)
        else:
            new_wax = rnd.choice(candidates_ends)
        wax.append(new_wax)
        plot[new_wax]=1
    
    ## Excavation Zones ##
    
    for i in range(num_Ez):        
        move = True
        
        # Check for hitting another bee #
        # (nb. we're currently assuming all collisions happen on the semicircles)
        for f in range(num_Ez):
            if f != i and np.sqrt((Ez_positions[i][0]-Ez_positions[f][0])**2 + (Ez_positions[i][1]-Ez_positions[f][1])**2)  < Ez_width:
                rand_place_Ez(i)                
                #if i == 0:
                    #print('Teleported :o', i)
        
        # Check for near wax and thin walls #
        # Find any wax within detection distance of this Ez, this is super inefficient!    
        # (nb. again assuming this wax is closest to the semicricle)
        close_wax = []
        for k in wax:
            if np.sqrt((Ez_positions[i][0]-k[0])**2+(Ez_positions[i][1]-k[1])**2) < ((Ez_width/2)+detect_length):
                close_wax.append(k)
        
        # If there is close wax
        if close_wax != []:            
            # Find the angle between some of the close wax and the Ez
            Ez_wax_angle = np.arctan((Ez_positions[i][1]-close_wax[0][1])/(Ez_positions[i][0]-close_wax[0][0]))
            
            # Check for thin walls #
            # If the wax is in front and there's no wax min_wax_thick away from the current position
            if (round(Ez_positions[i][0] + ((Ez_width/2)+min_wax_thick)*np.cos(Ez_wax_angle)), round(Ez_positions[i][1] + ((Ez_width/2)+min_wax_thick)*np.sin(Ez_wax_angle))) not in wax: #(Ez_wax_angle < 0.1 or Ez_wax_angle > 0.1) and 
                # if we can, twist up
                move = False
                if (round(Ez_positions[i][0] + ((Ez_width/2)+min_wax_thick)*np.cos(Ez_wax_angle+0.01)), round(Ez_positions[i][1] + ((Ez_width/2)+min_wax_thick)*np.sin(Ez_wax_angle+0.01))) in wax:
                    Ez_wax_angle = Ez_wax_angle + 0.01
                # if we can, twist down
                elif (round(Ez_positions[i][0] + ((Ez_width/2)+min_wax_thick)*np.cos(Ez_wax_angle-0.01)), round(Ez_positions[i][1] + ((Ez_width/2)+min_wax_thick)*np.sin(Ez_wax_angle-0.01))) in wax:
                    Ez_wax_angle = Ez_wax_angle - 0.01
            Ez_angles[i] = Ez_wax_angle
                
        # Unless we're staying put, take a step
        if move:
            Ez_positions[i] = (round(Ez_positions[i][0] + (min_wax_thick/2)*np.cos(Ez_angles[i])), round(Ez_positions[i][1] + (min_wax_thick/2)*np.sin(Ez_angles[i])))
            # And scroll over edges
            if Ez_positions[i][0] > N:
                Ez_positions[i] = (Ez_positions[i][0]-N, Ez_positions[i][1])
            if Ez_positions[i][1] > N:
                Ez_positions[i] = (Ez_positions[i][0], Ez_positions[i][1]-N)
            if Ez_positions[i][0] < 0:
                Ez_positions[i] = (Ez_positions[i][0]+N, Ez_positions[i][1])
            if Ez_positions[i][1] < 0:
                Ez_positions[i] = (Ez_positions[i][0], Ez_positions[i][1]+N)
        
        # Now actually remove wax!
        remove_wax = []
        for k in range(len(wax)):
            if np.sqrt((Ez_positions[i][0]-wax[k][0])**2+(Ez_positions[i][1]-wax[k][1])**2) < (Ez_width/2)*0.9:
                plot[wax[k]] = 0
                remove_wax.append(wax[k])
        # And record that it's gone
        for k in remove_wax:
            wax.remove(k)   
             
    #print(Ez_positions[0],Ez_angles[0])
    # Save some frames
    if n % (num_steps/num_frames) == 0:
       print('Plot number', n)
       saved_plot = plot.copy()
       j = 0
       for i in Ez_positions:
           j += 1
           saved_plot[int(i[0])-5:int(i[0])+3,int(i[1])-5:int(i[1])+3] = j/num_Ez
       plots.append((n,saved_plot))

#plt.imshow(plot, cmap='hot', interpolation='nearest')
    #title = 'Iteration Number ' + str(i[0])
    #plt.title(title)
#plt.show()

fig, ax_lst = plt.subplots(4,5)
ax_lst = ax_lst.ravel()

data = np.random.rand(N, N)
for i in range(20):
    im = ax_lst[i].imshow(plots[i][1])

#for i in range(len(plots)):
#    t_start = time.time()
#    data = plots[i][1]
#    im.set_data(data) 
#    plt.pause(0.5)
#    t_end = time.time()
#    print("fps = {0}".format(999 if t_end == t_start else 1/(t_end-t_start)))


