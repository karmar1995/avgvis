from simulation.core.traverser_base import *


GENE_POOL_SIZE = 40
MUTATION_PROBABILITY = 0.1


class Genome:
    def __init__(self, tasks):
        if tasks is None:
            raise RuntimeError("Invalid tasks sequence")
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
    def __init__(self, system, nodesToVisit, maxIterations):
        super().__init__(system, nodesToVisit)
        self._genes = []
        self.__generateGenes()
        self.__currentGene = -1
        self._bestGene = None

    def __generateGenes(self):
        for i in range(0, GENE_POOL_SIZE):
            self._genes.append(Genome(random.sample(self._tasksSequence, k=len(self._tasksSequence))))

    def nextIteration(self):
        self.__currentGene += 1
        if self.__currentGene >= len(self._genes):
            self.__depopulate()
            self.__mutate()
            self.__crossover()
            self.__currentGene = 0
        self._tasksSequence = self._genes[self.__currentGene].tasks
        if self._tasksSequence is None:
            raise RuntimeError("Invalid tasks sequence")

    def feedback(self, path, pathCost, collisions, timeInQueue, timeInPenalty):
        self._genes[self.__currentGene].cost = pathCost
        if self._bestGene is None or self._bestGene.cost > pathCost:
            self._bestGene = self._genes[self.__currentGene]
            self._bestSequence = self._bestGene.tasks
            self._bestPath = Path(path, pathCost, collisions, timeInQueue, timeInPenalty)

    def __crossover(self):
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
        l = len(self._genes)
        if l % 2 != 0:
            raise RuntimeError("Invalid population size")
        self._genes.sort()
        self._genes = self._genes[0: int(l / 2)]