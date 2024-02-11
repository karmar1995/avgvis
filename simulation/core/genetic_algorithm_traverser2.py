from simulation.core.traverser_base import *


DEFAULT_POOL_SIZE = 120
MUTATION_PROBABILITY = 0.15


class Genome:
    def __init__(self, tasks):
        if tasks is None:
            raise RuntimeError("Invalid tasks sequence - None")
        if len(tasks) == 0:
            raise RuntimeError("Invalid tasks sequence - empty list")

        self.tasks = tasks
        self.cost = 0

    def crossover(self, other):
        l1 = int(len(self.tasks) / 2)
        l2 = int(len(other.tasks) / 2)
        selfLowerHalf = copy.deepcopy(self.tasks[0: l1])
        selfUpperHalf = copy.deepcopy(self.tasks[l1:])
        otherLowerHalf = copy.deepcopy(other.tasks[0: l2])
        otherUpperHalf = copy.deepcopy(other.tasks[l2:])

        selfLowerHalf.extend(otherUpperHalf)
        otherLowerHalf.extend(selfUpperHalf)
        return Genome(selfLowerHalf), Genome(otherLowerHalf)

    def mutate(self):
        if random.random() < MUTATION_PROBABILITY:
            self.tasks = copy.deepcopy(self.tasks)
            pos1 = random.randint(0, len(self.tasks)-1)
            pos2 = random.randint(0, len(self.tasks)-1)
            self.tasks[pos1], self.tasks[pos2] = self.tasks[pos2], self.tasks[pos1]

    def reset(self):
        self.cost = 0

    def __lt__(self, other):
        return self.cost < other.cost


class GeneticAlgorithmTraverser(TraverserBase):
    def __init__(self, system):
        super().__init__(system)
        self._genes = []
        self.__currentGene = -1
        self.__genePoolSize = DEFAULT_POOL_SIZE

    def assignSequence(self, sequence):
        super().assignSequence(sequence)
        self.__genePoolSize = self.__calculatePoolSize(len(sequence))
        self.__generateGenes()

    def __calculatePoolSize(self, sequenceLength):
        return DEFAULT_POOL_SIZE

    def __generateGenes(self):
        self._genes.append(Genome(self._currentSequence))
        for i in range(0, self.__genePoolSize-1):
            self._genes.append(Genome(random.sample(self._currentSequence, k=len(self._currentSequence))))

    def nextIteration(self):
        self._genes[self.__currentGene].cost = self._currentCost
        if self._bestCost == -1 or self._bestCost > self._currentCost:
            self._acceptCurrentSolution()

        self.__currentGene += 1
        if self.__currentGene >= len(self._genes):
            l1 = len(self._genes)
            self.__depopulate()
            self.__mutate()
            self.__crossover()
            l2 = len(self._genes)
            if l1 != l2:
                raise Exception("Genes pool broken")
            self.__currentGene = 0

        self._currentSequence = self._genes[self.__currentGene].tasks
        self._tmpSequence = copy.deepcopy(self._currentSequence)
        self._currentCost = 0
        self._currentStatistics = TraverserStatistics(0, 0, 0, 0)

    def feedback(self, cost, collisions, timeInQueue, timeInPenalty, timeInTransition):
        super().feedback(cost, collisions, timeInQueue, timeInPenalty, timeInTransition)

    def __crossover(self):
        self.__validatePool()
        newGenes = []
        while len(self._genes) > 0:
            genom1 = self._genes.pop(random.randint(0, len(self._genes)-1))
            genom2 = self._genes.pop(random.randint(0, len(self._genes)-1))
            newGenom1, newGenom2 = genom1.crossover(genom2)
            genom1.reset()
            genom2.reset()
            newGenes.append(newGenom1)
            newGenes.append(newGenom2)
            newGenes.append(genom1)
            newGenes.append(genom2)
        self._genes = newGenes

    def __mutate(self):
        for genome in self._genes:
            genome.mutate()

    def __depopulate(self):
        self.__validatePool()
        self._genes.sort()
        self._genes = self._genes[0: int(len(self._genes) / 2)]
        self.__validatePool()

    def __validatePool(self):
        l = len(self._genes)
        if l % 2 != 0:
            raise RuntimeError("Invalid population size")
