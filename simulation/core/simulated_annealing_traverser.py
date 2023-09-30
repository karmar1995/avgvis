import random, copy, math
from simulation.core.path import Path


class SimulatedAnnealingTraverser:
    def __init__(self, system, controller, nodesToVisit, maxIterations):
        self.system = system
        self.controller = controller
        self.__bestPath = None
        self.__bestSequence = nodesToVisit
        self.__tasksSequence = nodesToVisit
        self.__generatePathFromTasks()
        self.__temperaturePoint = 0
        self.__temperatureStep = 10 / maxIterations

    def __generatePathFromTasks(self):
        path = []
        k = 1
        for i in range(0, len(self.__tasksSequence)):
            partialPath = random.choice(self.system.graph.get_k_shortest_paths(self.__tasksSequence[i].source(), self.__tasksSequence[i].destination(), k))
            print(partialPath)
            if i > 0 and self.__tasksSequence[i-1].destination() == self.__tasksSequence[i].source():
                partialPath.pop(0)
            path.extend(partialPath)
            if (i < len(self.__tasksSequence) - 1) and self.__tasksSequence[i].destination() != self.__tasksSequence[i+1].source():
                partialPath = random.choice(self.system.graph.get_k_shortest_paths(self.__tasksSequence[i].destination(), self.__tasksSequence[i+1].source(), k))
                partialPath.pop(0)
                partialPath.pop()
                path.extend(partialPath)
        return self.__validatePath(path)

    def __validatePath(self, path):
        for i in range(0, len(path) - 2):
            if path[i] == path[i+1]:
                raise Exception("Invalid path!")
        return path

    def __generateSequence(self):
        self.__tasksSequence = copy.deepcopy(self.__bestSequence)
        pos1 = random.randint(0, len(self.__tasksSequence)-1)
        pos2 = random.randint(0, len(self.__tasksSequence)-1)
        self.__tasksSequence[pos1], self.__tasksSequence[pos2] = self.__tasksSequence[pos2], self.__tasksSequence[pos1]

    def nextIteration(self):
        self.__temperaturePoint += self.__temperatureStep

    def path(self):
        self.__generateSequence()
        return self.__generatePathFromTasks()

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
                self.__bestSequence = self.__tasksSequence

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
