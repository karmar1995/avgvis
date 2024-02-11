from dataclasses import dataclass
import random, copy, math


@dataclass
class TraverserStatistics:
    collisions: int
    timeInQueue: float
    timeInPenalty: float
    timeInTransition: float


class TraverserBase:
    def __init__(self, system):
        self.system = system
        self._bestSequence = None
        self._bestCost = 0
        self._bestStatistics = None
        self._currentSequence = None
        self._currentCost = 0
        self._currentStatistics = None
        self._tmpSequence = None

    def assignSequence(self, sequence):
        self._bestCost = -1
        self._bestSequence = copy.deepcopy(sequence)
        self._currentCost = 0
        self._currentSequence = copy.deepcopy(sequence)
        self._tmpSequence = copy.deepcopy(sequence)
        self._currentStatistics = TraverserStatistics(0, 0, 0, 0)

    def feedback(self, cost, collisions, timeInQueue, timeInPenalty, timeInTransition):
        self._currentCost += cost
        self._currentStatistics.collisions += collisions
        self._currentStatistics.timeInQueue += timeInQueue
        self._currentStatistics.timeInPenalty += timeInPenalty
        self._currentStatistics.timeInTransition += timeInTransition

    def nextIteration(self):
        raise NotImplementedError("To be implemented in concrete traverser!")

    def finished(self):
        return len(self._tmpSequence) == 0

    def statistics(self):
        return self._bestStatistics

    def tasks(self):
        if len(self._tmpSequence) > 0:
            t = self._tmpSequence.pop()
            return [t]
        return []

    def pathBetweenNodes(self, source, destination):
        return self.system.graph.get_k_shortest_paths(source.index, destination.index, 1)[0]

    def node(self, index):
        return self.system.node(index)

    def edgeAgents(self, source, destination):
        return self.system.edgeAgents(source, destination)

    def transitionTime(self, nodeIndex1, nodeIndex2):
        return self.system.graph[nodeIndex1, nodeIndex2]

    def sequence(self):
        return self._bestSequence

    def cost(self):
        return self._bestCost

    def _acceptCurrentSolution(self):
        self._bestCost = self._currentCost
        self._bestSequence = copy.deepcopy(self._currentSequence)
        self._bestStatistics = copy.deepcopy(self._currentStatistics)
