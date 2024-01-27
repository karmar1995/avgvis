import random, copy, math
from simulation.core.path import Path


class TraverserBase:
    def __init__(self, system):
        self.system = system
        self._bestSequence = None
        self._bestCost = 0
        self._currentSequence = None
        self._currentCost = 0
        self._tmpSequence = None

    def assignSequence(self, sequence):
        self._bestCost = 0
        self._bestSequence = None
        self._currentCost = 0
        self._currentSequence = copy.deepcopy(sequence)
        self._tmpSequence = copy.deepcopy(sequence)

    def feedback(self, cost, collisions, timeInQueue, timeInPenalty, timeInTransition):
        self._currentCost += cost

    def finished(self):
        return len(self._tmpSequence) == 0

    def nextIteration(self):
        raise NotImplementedError("To be implemented in concrete traverser!")

    def tasks(self):
        if len(self._tmpSequence) > 0:
            t = self._tmpSequence.pop()
            return [t]
        return []

    def pathBetweenNodes(self, source, destination):
        return self.system.graph.get_k_shortest_paths(source.index, destination.index, 1)[0]

    def node(self, index):
        return self.system.node(index)

    def transitionTime(self, nodeIndex1, nodeIndex2):
        return self.system.graph[nodeIndex1, nodeIndex2]

    def sequence(self):
        return self._bestSequence

    def cost(self):
        return self._bestCost
