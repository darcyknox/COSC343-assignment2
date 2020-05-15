import numpy as np
import matplotlib.pyplot as plt
import random

playerName = "myAgent"
nPercepts = 75  #This is the number of percepts
nActions = 7    #This is the number of actions

avgFitData = [] # for plotting data

# This is the class for your creature/agent

class MyCreature:

    def __init__(self, chromosome=None):

        # fitness attribute - used for selection
        self.fitness = 0

        if chromosome is None:
            self.chromosome = np.random.rand(nPercepts, nActions)
        else:
            self.chromosome = chromosome


    def AgentFunction(self, percepts):

        # initialised with zero values
        actions = np.zeros(nActions)

        # percepts matrix is flattened so it can be iterated through easily
        percepts = percepts.flatten()

        # Agent function mapping percepts to actions (action = sum of (percepts * weights))
        for x in range(nPercepts):
            for y in range(nActions):
                actions[y] = actions[y] + ((percepts[x] * self.chromosome[x][y]))

        # Eats strawberry when the creature is on a strawberry
        if percepts[37] == 1:
            actions[5] = actions[5] * 2

        return actions


# Creates a new generation based on the old population - Genetic Algorithm
def newGeneration(old_population):

    N = len(old_population)

    # Fitness for all agents
    fitness = np.zeros((N))

    # used for survival rate
    numSurvivors = 0

    # Attributes a fitness score for each creature in the population
    for n, creature in enumerate(old_population):

        # creature.alive - boolean, true if creature is alive at the end of the game
        # creature.turn - turn that the creature lived to (last turn if creature survived the entire game)
        # creature.size - size of the creature
        # creature.strawb_eats - how many strawberries the creature ate
        # creature.enemy_eats - how much energy creature gained from eating enemies

        if creature.alive:
            numSurvivors = numSurvivors + 1

        survivalRate = numSurvivors/(n + 1)

        # FITNESS FUNCTION
        fitnessValue = (creature.alive * creature.turn * creature.enemy_eats) + (creature.alive * creature.turn * creature.strawb_eats) + creature.turn
        fitnessValue = fitnessValue + survivalRate # separated for readability

        # Add the fitness to the population fitness list.
        fitness[n] = fitnessValue

        # Give the fitness attribute of the individual creature its fitness value.
        # This is used for sorting after selection.
        creature.fitness = fitnessValue

    # SELECTING PARENTS, MIXING CHROMOSOMES, MAKING NEW GENERATION
    new_population = list()
    for n in range(N):

        # . Tournament selection - select a subset of 70% of the old population.
        # . Pick the fittest 2 individuals from that subset.
        # . Create a new chromosome for the new creature using the parents' 'genes'

        # proportion size of old population that the subset will be comprised of
        subsetProportion = 0.70

        # get random creature objects and their fitness from a proportion of the old population
        randomSubset = random.sample(old_population, round(len(old_population) * subsetProportion))

        # sort the subset by individual fitness value (fittest at the front of the list)
        randomSubset.sort(key= lambda x:x.fitness, reverse=True)

        # Chosen parents are the two fittest in the subset
        mother = randomSubset[0]
        father = randomSubset[1]

        # Initialise chromosome of new_creature
        new_chromosome = np.ndarray(shape=(nPercepts, nActions))

        # Select a single point crossover point
        crossoverPoint = random.randint(1, nPercepts * nActions)

        # Current point in new chromosome
        c = 0

        # Elitism -
        # First 3 creatures in the new population will be clones of the fittest individual in the subset
        if n < 3:
            new_creature = MyCreature(mother.chromosome) # copies the genes of the 3 fittest creatures
        else:
            # Mixing chromosomes
            for i in range(nPercepts):
                for j in range(nActions):
                    if c < crossoverPoint:
                        new_chromosome[i][j] = mother.chromosome[i][j]
                    else:
                        new_chromosome[i][j] = father.chromosome[i][j]
                    # Mutation
                    if random.randint(0, 100) < 3:
                        new_chromosome[i][j] = random.uniform(0, np.amax(father.chromosome))
                    c = c + 1

            # Create a new creature with the new_chromosome
            new_creature = MyCreature(new_chromosome)

        # Add the new agent to the new population
        new_population.append(new_creature)

    # At the end you need to compute average fitness and return it along with your new population
    avg_fitness = np.mean(fitness)
    avgFitData.append(avg_fitness)

    # Plotting fitness data
    plt.close('all')
    plt.figure()
    plt.xlabel('Epochs')
    plt.ylabel('Average fitness')
    plt.plot(avgFitData, 'k.')
    plt.show()

    return (new_population, avg_fitness)
