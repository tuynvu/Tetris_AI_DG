from Weight import Weight
from tqdm import tqdm
from AgentNN import AgentNN
from functools import cmp_to_key
from copy import deepcopy

INPUT_SHAPE = 4, 1
EPSILON = 0.6
NBESTPPOPULATION = 30

def cmp(a, b):
    if a < b: return 1
    else: return -1

class Geneticnn(object):
    def __init__(self, population, epochs, limit_piece, epsilon):
        self.epochs = epochs
        self.limit_piece = limit_piece
        self.epsilon = epsilon
        self.population = population

    def genPopulations(self):
        weight_population = []
        for i in range(self.population):
            weight_population.append(AgentNN(input_shape=INPUT_SHAPE))
        return weight_population

    def getFitness(self):
        """
        play -> score
        :return: score of Agent: int
        """
        pass

    def getBestNPopulation(self, listAgent):
        """
        :param listAgent: list[(AgentNN, score)]
        :return: list[AgentNN]
        """
        return listAgent.sort(key=cmp_to_key(mycmp=cmp))[:NBESTPPOPULATION]

    def crossGen(self):
        pass
    def mutateGen(self):
        pass
    def normalGen(self):
        pass
    def genRemain(self):
        pass
    def trainGeneticNN(self, episode):
        gen = self.genPopulations()
        for epoch in tqdm(range(self.epochs)):
            listAgnt: list(tuple(AgentNN, int)) = []
            for idiv in gen:
                score = self.getFitness(idiv)
                listAgnt.append((idiv, score))

            bestPop = self.getBestNPopulation(listAgnt)

            gen = deepcopy(bestPop)
            for genetic in range(self.population - NBESTPPOPULATION):
                gen.append(self.genRemain())

