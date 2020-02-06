# honeycomb
simulation of how bees build honeycombs

## some stuff from the paper:

### Self-organization at the first stage of honeycomb construction: Analysis of an attachment-excavation model
*Takayuki Narumi, Kenta Uemichi, Hisao Honda, Koichi Osaki*

The attachment-excavation model is proposed as a way to understand the mechanisms of hon- eycomb construction; in this paper, especially the first stage of construction. At the most basic level, there are two types of workers: attachers, who secrete and attach wax, and excavators, who excise the attached wax using their mandibles.


We will consider a 2D system whose size is lx × ly. As the initial model condition, a fixed amount of wax is placed at the center of the system. In nature, the wax is attached in a number of places at the beginning of honeycomb construction. In our model, we observe the growth of one such comb because our focus is on the first stage of the honeycomb construction, which is not affected by other locations.
The attachers move freely within the system, each secreting one dollop of wax per unit time. The wax is added to the boundary of randomly selected preexisting wax. In nature, since worker honeybees operate in swarms, two or more workers will inevitably supply wax simulta- neously at different volumes at different points. In contrast, our model presumes that a worker attaches a fixed amount of wax to a single point on the boundary at each step. Thus, the time unit is regarded as the supply interval average.

Instead of tracking the motions of the attachers, this model follows wax growth, the dynamics of which are simulated by the Eden growth rule [19]. The system domain is divided into Nx × Ny lattice cells, where each cell has size Δx × Δy with Δx = lx/Nx and Δy = ly/Ny. The presence of wax in the system is expressed by a binary value assigned to each lattice cell. A lattice cell filled with wax is designated as being in the on-state, whereas an empty lattice cell is designated as being in the off-state. The Eden growth rule states that the off-state lattice cells around the on-state lattice cells are candidates for supplied wax at each step, after which a lattice cell selected randomly from the candidates is switched on at the next time step.

 
