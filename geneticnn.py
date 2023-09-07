from Weight import Weight
from tqdm import tqdm
from AgentNN import AgentNN
from functools import cmp_to_key
from copy import deepcopy
from Env.tetris import TetrisApp
import numpy as np
import random

INPUT_SHAPE = 4, 1
EPSILON = 0.6
NBESTPPOPULATION = 30
ROUNDS = 4
LIMITPIECE = 200

def cmp(a, b):
    if a < b: return 1
    else: return -1

class Geneticnn(object):
    def __init__(self, population, epochs, limit_piece, epsilon):
        self.epochs = epochs
        self.limit_piece = limit_piece
        self.epsilon = epsilon
        self.population = population
    def genIndv(self):
        return AgentNN(input_shape=INPUT_SHAPE)

    def genPopulations(self):
        weight_population = []
        for i in range(self.population):
            weight_population.append(self.genIndv())
        return weight_population

    def getFitness(self,indv):
        """
        play -> score
        :return: score of Agent: int
        """
        score = 0
        for round in range(ROUNDS):
            score += TetrisApp(playWithUI=True, seed=42, Ai=indv).run(LIMITPIECE)
        return score

    def getBestNPopulation(self, listAgent):
        """
        :param listAgent: list[(AgentNN, score)]
        :return: list[AgentNN]
        """
        return listAgent.sort(key=cmp_to_key(mycmp=cmp))[:NBESTPPOPULATION]

    def excuteCross(self,indv1, indv2) -> AgentNN:
        pass
    def crossGen(self, indv1, indv2):
        if np.random.rand() > 0.4:
            return self.excuteCross(indv1, indv2)
        else:
            return self.genIndv()

    def excuteMutate(self, indv):
        pass

    def mutateGen(self, indv):
        if np.random.rand() > 0.5:
            return self.excuteMutate(indv)
        else:
            return self.genIndv()

    def normalGen(self):
        pass

    def genRemain(self, nremain, nbestgen):
        remainGen = []
        for gen in range(remainGen):
            if np.random.rand() > 0.4:
                remainGen.append(self.mutateGen(random.choice(nbestgen)))
            else:
                remainGen.append(self.crossGen(*random.choices(nbestgen, k=2)))

    def trainGeneticNN(self, episode):
        gen = self.genPopulations()
        for epoch in tqdm(range(self.epochs)):
            listAgnt: list(tuple(AgentNN, int)) = []
            for idiv in gen:
                score = self.getFitness(idiv)
                listAgnt.append((idiv, score))

            bestPop = self.getBestNPopulation(listAgnt)

            gen = deepcopy(bestPop)
            gen.extend(self.genRemain(self.population - NBESTPPOPULATION, bestPop))

