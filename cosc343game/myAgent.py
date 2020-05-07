import numpy as np
import matplotlib.pyplot as plt
import random

playerName = "myAgent"
nPercepts = 75  #This is the number of percepts
nActions = 7    #This is the number of actions

avgFitData = []
turns = 0

b = 2

# This is the class for your creature/agent

class MyCreature:

    def __init__(self, chromosome=None):
        # chromosome=None
        # You should initialise self.chromosome member variable here (whatever you choose it
        # to be - a list/vector/matrix of numbers - and initialise it with some random
        # values

        self.fitness = 0
        self.fitnessWeights = np.random.rand(5)

        if chromosome is None:
            self.chromosome = np.random.rand(nPercepts, nActions)
        else:
            self.chromosome = chromosome

        testPercept = np.zeros(shape=(5, 5, 3))

        testChrome = np.zeros(shape=(nPercepts, nActions))

        #print("flat percept")
        #print(testPercept.flatten().size)

        #print("flat chrome")
        #print(testChrome.flatten().size)

        # .
        # .
        # .


    def AgentFunction(self, percepts):

        actions = np.zeros(nActions)

        # You should implement a model here that translates from 'percepts' to 'actions'
        # through 'self.chromosome'.
        #
        # The 'actions' variable must be returned and it must be a 7-dim numpy vector or a
        # list with 7 numbers.
        #
        # The index of the largest numbers in the 'actions' vector/list is the action taken
        # with the following interpretation:
        # 0 - move left
        # 1 - move up
        # 2 - move right
        # 3 - move down
        # 4 - do nothing
        # 5 - eat
        # 6 - move in a random direction
        #
        # Different 'percepts' values should lead to different 'actions'.  This way the agent
        # reacts differently to different situations.
        #
        # Different 'self.chromosome' should lead to different 'actions'.  This way different
        # agents can exhibit different behaviour.

        # .
        # .
        # .

        # Percepts matrix is flattened so it can be iterated through more easily
        percepts = percepts.flatten()

        # Agent function mapping percepts to actions (currently action = sum of percepts * weights)
        for x in range(nPercepts):
            for y in range(nActions):
                actions[y] = actions[y] + ((percepts[x] * self.chromosome[x][y])) # + b

        return actions



def newGeneration(old_population):

    # This function should return a list of 'new_agents' that is of the same length as the
    # list of 'old_agents'.  That is, if previous game was played with N agents, the next game
    # should be played with N agents again.

    # This function should also return average fitness of the old_population
    N = len(old_population)

    # Fitness for all agents
    fitness = np.zeros((N))



    numSurvivors = 0
    totalSize = 0
    avgSize = 0

    # This loop iterates over your agents in the old population - the purpose of this boiler plate
    # code is to demonstrate how to fetch information from the old_population in order
    # to score fitness of each agent
    # FITNESS FUNCTION
    # Attributes a fitness score for each creature in the population
    for n, creature in enumerate(old_population):

        # creature is an instance of MyCreature that you implemented above, therefore you can access any attributes
        # (such as `self.chromosome').  Additionally, the objects has attributes provided by the
        # game engine:
        #
        # creature.alive - boolean, true if creature is alive at the end of the game
        # creature.turn - turn that the creature lived to (last turn if creature survived the entire game)
        # creature.size - size of the creature
        # creature.strawb_eats - how many strawberries the creature ate
        # creature.enemy_eats - how much energy creature gained from eating enemies

        # . alive * everything
        # . size/turn

        fitnessValue = (creature.strawb_eats/creature.turn + creature.enemy_eats/creature.turn) * creature.size
        #fitnessValue = (creature.strawb_eats / creature.turn + creature.enemy_eats / creature.turn) + creature.size**2 + creature.turn**2
        #fitnessValue = creature.strawb_eats * creature.fitnessWeights[0] + creature.enemy_eats * creature.fitnessWeights[1] + creature.turn * creature.fitnessWeights[2] + creature.size * creature.fitnessWeights[3]

        fitnessValue = pow(fitnessValue, (creature.alive + 1))

        # This fitness functions just considers length of survival.  It's probably not a great fitness
        # function - you might want to use information from other stats as well
        fitness[n] = fitnessValue
        creature.fitness = fitnessValue

    # At this point you should sort the agent according to fitness and create new population
    # SELECTING PARENTS, MIXING CHROMOSOMES, MAKING NEW GENERATION
    new_population = list()
    for n in range(N):

        # Create new creature
        #new_creature = MyCreature()

        # Here you should modify the new_creature's chromosome by selecting two parents (based on their
        # fitness) and crossing their chromosome to overwrite new_creature.chromosome

        # Consider implementing elitism, mutation and various other
        # strategies for producing new creature.

        # . Tournament selection - pick 10 random creatures
        # . Pick the best 2 from that selection
        # . Create a new chromosome for the new creature using the parents' 'genes'

        # get 10 random creature objects and their fitness from the old population
        randomSubset = random.sample(old_population, round(len(old_population) * 0.8))

        #Print random subset - tournament selection
        '''print("random subset")
        print(randomSubset)'''

        randomSubset.sort(key= lambda x:x.fitness, reverse=True)


        # Print fitnesses in order
        '''for i in range(len(randomSubset)):
            print(randomSubset[i].fitness)'''

        mother = randomSubset[0]
        father = randomSubset[1]

        # Initialise chromosome of new_creature
        new_chromosome = np.ndarray(shape=(nPercepts, nActions))

        mutationFactor = random.randint(0, 100)

        # Mixing chromosomes
        for i in range(nPercepts):
            for j in range(nActions):
                if i < round(nPercepts * 0.75):
                    new_chromosome[i][j] = mother.chromosome[i][j]
                else:
                    new_chromosome[i][j] = father.chromosome[i][j]
                    #print("father " + str(i) + " " + str(j))
                if random.randint(0, 100) < 5: # mutation
                    new_chromosome[i][j] = random.uniform(0, np.amax(father.chromosome))

        new_creature = MyCreature(new_chromosome)


        # Add the new agent to the new population
        new_population.append(new_creature)

    # At the end you need to compute average fitness and return it along with your new population
    avg_fitness = np.mean(fitness)
    avgFitData.append(avg_fitness)

    plt.close('all')
    plt.figure()
    plt.xlabel('Epochs')
    plt.ylabel('Average fitness')
    plt.plot(avgFitData, 'k.')
    plt.show()

    return (new_population, avg_fitness)
