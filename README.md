# GA4Beamlines

## Goal
Alignment of x-ray beamlines is generally an iterative process wherein the operator varies a single element to optimize some beam feature (e.g. intensity or shape) measured downstream before moving to the next element. This manual process can be very time consuming.  In order to automate the procedure, one could treat the process as a search/optimization problem: search the space of possible optical arrangements to optimize some beam parameter, e.g. intensity or shape. One such approach is genetic algorithm [1].

This project aims to create a genetic algorithm package for aligning surrogate (modeled) and real beamlines. Genetic algorithms have been used on synchrotron beamlines [2] and storage rings [3]. However, in tandem with this project is the development of surrogate models for beamlines so that other approaches (e.g. evolution strategies, reinforcement learning, or other variations on genetic algorithm) to automating beamline alignment can be tested.

## Genetic Algorithm
Genetic algorithm is a metaheuristic designed to mimic aspects of natural selection, mainly recombination, mutation, and selection.

### Overview
In genetic algorithms, a population of solutions to a problem are evolved in order to find an optimal solution to the problem.  In this case, the problem is the arrangement of optical elements in a beamline to produce the optimal downstream beam parameter (either intensity or beam shape). The proposed solutions are evaluated and survivors selected based on fitness or age. From the survivors parents are selected and recombined to produce children.  These children undergo mutation and added to the pool of individuals subject to survivor selection. This completes one generation and the process continues until a “good” enough solution is found or the maximum number of generations have been carried out.

### Population:

### Selection
#### Survivor
##### Method 1 - Age + Elitism
In this method, the **elite** (the best *n* members of the current population) are selected to carry over into the next generation's population.  The rest of population is replaced by the **children** (new individuals generated during recombination and mutation) to finish creating the new population of the next generation.

##### Method 2 - Genitor
For this method, a number of children equal to the size of the current population, *p*, is generated.  Then, the individuals of the current population and the children are pooled together and ordered by their fitness.  The best *p* individuals of this pool are carried over to be the population of the next generation.

#### Parent
##### Method 1 - Rank-Based Probability


##### Method 2 - Fitness-Based Probability


### Variation
#### Recombination
##### Method 1
##### Method 2

#### Mutation
##### Method 1
##### Method 2

## Pseudocode
### Evolution
### Selection
### Variation

## Additions
### Observer Mode

## Testing
### Ackley Function
### Results
#### General objective function
#### Surrogate beamline

## Future work
### Steady-state
### 2-D or image-base objective
### Multi-objective

## References
[1] Eiben, A.E. and Smith, J.E. Introduction to Evolutionary Computing, 2nd ed Springer (2015)

[2] Xi, S., Borgna, L. S. & Du, Y.  General method for automatic on-line beamline optimization based on genetic algorithm J. Synchrotron Rad. 22, 661–665 (2015)

[3] Borland, M., Sajaev  V., Emery L., Xiao A. Direct methods of optimization of storage ring dynamic and momentum aperture Proceedings of PAC09, Vancouver, BC, Canada 3850-2 (2009)
