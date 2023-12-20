import random, copy, math
from simulation.core.path import Path
from simulation.core.traverser_base import TraverserBase


class SimulatedAnnealingTraverser(TraverserBase):
    def __init__(self, system, controller, nodesToVisit, maxIterations):
        super().__init__(system, nodesToVisit)
        self.generatePathFromTasks()
        self.__temperaturePoint = 0
        self.__temperatureStep = 10 / maxIterations

    def __generateSequence(self):
        self._tasksSequence = copy.deepcopy(self._tasksSequence)
        pos1 = random.randint(0, len(self._tasksSequence)-1)
        pos2 = random.randint(0, len(self._tasksSequence)-1)
        self._tasksSequence[pos1], self._tasksSequence[pos2] = self._tasksSequence[pos2], self._tasksSequence[pos1]

    def nextIteration(self):
        self.__generateSequence()
        self.__temperaturePoint += self.__temperatureStep

    def feedback(self, path, pathCost, collisions):
        self.__performStateTransition(Path(path, pathCost, collisions))

    def __performStateTransition(self, newPath):
        if self._bestPath is None:
            self._bestPath = newPath
        else:
            if random.random() < self.__transitionProbability(currentEnergy=self._bestPath.cost, newEnergy=newPath.cost):
                self._bestPath = newPath
                self._tasksSequence = self._tasksSequence

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

