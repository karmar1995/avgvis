from simulation.core.traverser_base import *


class SimulatedAnnealingTraverser(TraverserBase):
    def __init__(self, system):
        super().__init__(system)
        self.__temperaturePoint = 0
        self.__temperatureStep = 0.1

    def __generateSequence(self):
        self._currentSequence = copy.deepcopy(self._bestSequence)
        self.__modifySequence()
        self._tmpSequence = copy.deepcopy(self._currentSequence)

    def __modifySequence(self):
        swaps = int(len(self._currentSequence) * 0.05)
        for i in range(0, swaps):
            pos1 = random.randint(0, len(self._currentSequence)-1)
            pos2 = random.randint(0, len(self._currentSequence)-1)
            self._currentSequence[pos1], self._currentSequence[pos2] = self._currentSequence[pos2], self._currentSequence[pos1]

    def nextIteration(self):
        self.__performStateTransition(self._currentCost)
        self.__generateSequence()
        self.__temperaturePoint += self.__temperatureStep
        self._currentCost = 0

    def feedback(self, cost, collisions, timeInQueue, timeInPenalty, timeInTransition):
        super().feedback(cost, collisions, timeInQueue, timeInPenalty, timeInTransition)

    def __performStateTransition(self, cost):
        if self._bestSequence is None:
            self._bestCost = cost
            self._bestSequence = copy.deepcopy(self._currentSequence)
        else:
            if random.random() < self.__transitionProbability(currentEnergy=self._bestCost, newEnergy=cost):
                self._bestCost = cost
                self._bestSequence = copy.deepcopy(self._currentSequence)

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

