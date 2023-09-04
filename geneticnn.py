from Weight import Weight
class Geneticnn(object):
    def __init__(self, population, epochs, limit_piece, epsilon):
        self.epochs = epochs
        self.limit_piece = limit_piece
        self.epsilon = epsilon
        self.population = population

    def genPopulations(self):
        weight_population = []
        for i in range(self.population):
            weight_population.append(Weight.random())
        return weight_population

    def getFitness(self):
        pass
    def getBestNPopulation(self):
        pass
    def crossGen(self):
        pass
    def mutateGen(self):
        pass
    def normalGen(self):
        pass
    def trainGeneticNN(self, episode):
        pass