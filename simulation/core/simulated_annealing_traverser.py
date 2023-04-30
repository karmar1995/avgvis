import random, copy, math
from simulation.core.path import Path


class SimulatedAnnealingTraverser:
    def __init__(self, system, controller, nodesToVisit, maxIterations):
        self.system = system
        self.controller = controller
        self.__bestPath = None
        self.__nodesToVisit = nodesToVisit
        self.__generateInitialPath()
        self.__temperaturePoint = 0
        self.__temperatureStep = 10 / maxIterations

    def __generateInitialPath(self):
        path = [self.__nodesToVisit[0]]
        for i in range(0, len(self.__nodesToVisit) - 1):
            partialPath = random.choice(self.system.graph.get_k_shortest_paths(self.__nodesToVisit[i], self.__nodesToVisit[i+1], 1))
            partialPath.pop(0)
            path.extend(partialPath)
        self.__path = path

    def __generatePath(self):
        if self.__bestPath is not None:
            self.__path = copy.deepcopy(self.__bestPath.path)
            pos1 = random.randint(0, len(self.__path)-1)
            pos2 = random.randint(0, len(self.__path)-1)
            self.__path[pos1], self.__path[pos2] = self.__path[pos2], self.__path[pos1]

    def nextIteration(self):
        self.__temperaturePoint += self.__temperatureStep

    def path(self):
        self.__generatePath()
        return self.__path

    def node(self, index):
        return self.system.node(index)

    def transitionTime(self, nodeIndex1, nodeIndex2):
        time = self.system.graph[nodeIndex1, nodeIndex2]
        return time

    def feedback(self, path, pathCost, collisions):
        self.__performStateTransition(Path(path, pathCost, collisions))

    def __performStateTransition(self, newPath):
        if self.__bestPath is None:
            self.__bestPath = newPath
        else:
            if random.random() < self.__transitionProbability(currentEnergy=self.__bestPath.cost, newEnergy=newPath.cost):
                self.__bestPath = newPath

    def __transitionProbability(self, currentEnergy, newEnergy):
        upwardsTransitionProbability = self.__temperature()
        if newEnergy > currentEnergy:
            return upwardsTransitionProbability
        return 1 - upwardsTransitionProbability

    def __temperatureFunction(self, x):
        f1 = math.exp(-x)
        f2 = math.cos(x*x)**2
        return f1*f2 * 0.1

    def __temperature(self):
        return self.__temperatureFunction(self.__temperaturePoint)

    def bestPath(self):
        return self.__bestPath
