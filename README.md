# GA4Beamlines

## Goal
Alignment of x-ray beamlines is generally an iterative process wherein the operator varies a single element to optimize some beam feature (e.g. intensity or shape) measured downstream before moving to the next element. This manual process can be very time consuming.  In order to automate the procedure, one could treat the process as a search/optimization problem: search the space of possible optical arrangements to optimize some beam parameter, e.g. intensity or shape. One such approach is genetic algorithm [1].

This project aims to create a genetic algorithm package for aligning surrogate (modeled) and real beamlines. Genetic algorithms have been used on synchrotron beamlines [2] and storage rings [3]. However, in tandem with this project is the development of surrogate models for beamlines so that other approaches (e.g. evolution strategies, reinforcement learning, or other variations on genetic algorithm) to automating beamline alignment can be tested.

## Genetic Algorithm
Genetic algorithm is a metaheuristic designed to mimic aspects of natural selection, mainly recombination, mutation, and selection.

### Overview
In genetic algorithms, a population of solutions to a problem are evolved in order to find an optimal solution to the problem.  In this case, the problem is the arrangement of optical elements in a beamline to produce the optimal downstream beam parameter (either intensity or beam shape). The proposed solutions are evaluated and survivors selected based on fitness or age. From the survivors parents are selected and recombined to produce children.  These children undergo mutation and added to the pool of individuals subject to survivor selection. This completes one generation and the process continues until a “good” enough solution is found or the maximum number of generations have been carried out.

### Population:
A collection of potential solutions, called **individuals**.  Maintains the same size across generations, though the individuals within change.
### Individual:
Drawing from its influence in biology, individuals have a **chromosome** which contains a series of values called **genes**
### Gene:
For this problem, each gene of the chromosome is a motor position within the beamline.

### Selection
There are two types of selection in this algorithm: **survivor** and **parent**.  Survivor selection determines which individuals will carry over into the next generation.  Parent selection decides which individuals will potentially contribute toward creating the next generation of individuals.
#### Survivor
##### Method 1 - Age + Elitism
In this method, the **elite** (the best *n* members of the current population) are selected to carry over into the next generation's population.  The rest of population is replaced by the **children** (new individuals generated during recombination and mutation) to finish creating the new population of the next generation.

##### Method 2 - Genitor
For this method, a number of children equal to the size of the current population *p* is generated.  Then, the individuals of the current population and the children are pooled together and ordered by their fitness.  The best *p* individuals of this pool are carried over to be the population of the next generation.

#### Parent
The members of the population are ranked from *p* - 1 to 0 (0 being the worst) based on their fitness.  From there, one of the following methods is used to assign the probability of each individual being selected as a potential **parent** (one of two or more individuals used in recombination to generate a child).  Once the probabilities are determined, potential parents are selected from the population using **Stochastic Universal Sampling** (see [1]).
##### Method 1 - Rank-Based Probability
This method calculates the probability of selecting an individual as a parent using the following formula:

<p style = "text-align: center;">(2 - s) / p + 2 * rank * (s - 1) / p / (p - 1)</p>

Where 1 < *s* <= 2 and *rank* is the rank of the individual.  *s* is used to determine the base chance of selecting an individual regardless of their rank.  As the value of s approaches 1, the probability of selecting an individual becomes the same for all individuals in the population.  As the value of s approaches 2, rank has a larger impact on the probability and the probability of selecting the worst individual (rank of 0) becomes 0.
##### Method 2 - Fitness-Based Probability
This method calculates the probability of selecting an individual as a parent by first calculating the cumulative fitness of the population and then dividing each individual's fitness by the cumulative fitness.


### Variation
Variation is what enables the population to explore the space of possible solutions.  There are two types of variation in this algorithm: **Recombination** and **Mutation**.  Recombination generates children from existing individuals to potentially become part of the next generation.  Mutation is applied to the children and serves as a way to keep the population from being overtaken by a few, well-adapted individuals.
#### Recombination
Takes pairs of parents and an  *alpha* (0.0 <= *alpha* <= 1.0, which is the percentage of contribution from each parent) and uses one of the following methods to generate two new children:
##### Method 1 - Single Arithmetic Recombination
A position within the parents *k* is randomly selected.  The first child is equal to the first parent, except the value at position *k* is:

<p style = "text-align: center;"> parent1's value at k * (1 - alpha) + parent2's value at k * alpha</p>

The second child is calculated in a similar manner, only the parents are reversed.
##### Method 2 - Simple Arithmetic Recombination
A position within the parents *k* is randomly selected.  The first 0 - *k* values of child one is equal to the same values in the same positions of the first parent, except the values at position *k* and after are :

<p style = "text-align: center;"> parent1's values from k to the end * (1 - alpha) + parent2's values from k to the end * alpha</p>

The second child is calculated in a similar manner, only the parents are reversed.
##### Method 3 - Whole Arithmetic Recombination
The first child's values would be calculated by:

<p style = "text-align: center;"> parent1's values * (1 - alpha) + parent2's values * alpha</p>

The second child is calculated in a similar manner, only the parents are reversed.  In the case that *alpha* is 0.5, the values of both children would be the average of the parents.

#### Mutation
Mutation occurs in the *children* produced from recombination.
##### Method 1 - Uniform
For each value in the child, a random value within a previously specified range is selected from a <ins>uniform distribution</ins>.
##### Method 2 - Gaussian
For each value in the child, a random value is selected from a <ins>gaussian distribution</ins> centered on the current value with a previously specified sigma range.

## Pseudocode
### Evolution
### Selection
### Variation

## Additions
### Observer Mode
Intended for use when working with physical beamlines.  When enabled, program will monitor the quality of the beam (based on specified criteria) as it transitions between beamline configurations within the population.  If a configuration better than the previous one is found during the transition, the previous configuration is replaced by the new one.

## Testing
### Ackley Function
### Results
- While both the **Age + Elitism** and **Genitor** methods of survivor selection are capable of finding satisfactory solutions, genitor generally can find a solution in less generations than age + elitism.
- **Uniform** mutation causes the algorithm to almost never generate a satisfactory solution (fitness >= 0.9) for all method configurations.
#### General objective function
#### Surrogate beamline

## Future work
### Steady-state
Another method of survivor selection.  Unlike the current methods, which can potentially generate an entirely new population each generation, this method prioritizes making small changes to the population over time.  For each generation, the *n* worst individuals are replaced with children and the rest of the population is carried over to the next generation.
### 2-D or image-base objective
### Multi-objective

## References
[1] Eiben, A.E. and Smith, J.E. Introduction to Evolutionary Computing, 2nd ed Springer (2015)

[2] Xi, S., Borgna, L. S. & Du, Y.  General method for automatic on-line beamline optimization based on genetic algorithm J. Synchrotron Rad. 22, 661–665 (2015)

[3] Borland, M., Sajaev  V., Emery L., Xiao A. Direct methods of optimization of storage ring dynamic and momentum aperture Proceedings of PAC09, Vancouver, BC, Canada 3850-2 (2009)
