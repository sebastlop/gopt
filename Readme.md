Genetic algorithm - based Optimizer 
==================================

This optimizer is based on the genetic algorithm, it preserves the different stages of it, namely: An initial distribution of individuals, selection, crossover and mutation.

For very simple functions, the optimizer can be used with a single population. But it allows more complex features as the ability to perform the algorithm over different populations, named tribes here. Tribes evolve isolated from others. After this stage, a merge of the best individuals of each tribes can be performed and evolved up to a convergence. This fact allows for a better domain sampling, which lead to avoid local minima.

The crossover between best individuals is performed in such way that genes of random best different individuals are averaged to create the next generation. In this algorithm, the best fitness half of the population survives to the next generation.

Mutations are random, and two distributions can be selected: uniform over the whole domain, or normal centered at the best individual in a tribe with a user provided standard deviation. The uniform model is slower convergent, but avoid local minima by itself (with a very large number of generations!). The normal model combined with the tribe concept, achieves to very good results with considerably less evaluations of the fitness function. 
