import random, copy, math
from simulation.core.path import Path


class TraverserBase:
    def __init__(self, system, nodesToVisit):
        self.system = system
        self._bestSequence = nodesToVisit
        self._tasksSequence = nodesToVisit
        self._bestPath = None

    def generatePathFromTasks(self, tasks):
        path = []
        k = 1
        for i in range(0, len(tasks)):
            partialPath = random.choice(self.system.graph.get_k_shortest_paths(tasks[i].source(), tasks[i].destination(), k))
            if i > 0 and tasks[i-1].destination() == tasks[i].source():
                partialPath.pop(0)
            path.extend(partialPath)
            if (i < len(tasks) - 1) and tasks[i].destination() != tasks[i+1].source():
                partialPath = random.choice(self.system.graph.get_k_shortest_paths(tasks[i].destination(), tasks[i+1].source(), k))
                partialPath.pop(0)
                partialPath.pop()
                path.extend(partialPath)
        return self.__validatePath(path)

    def __validatePath(self, path):
        for i in range(0, len(path) - 2):
            if path[i] == path[i+1]:
                raise Exception("Invalid path!")
        return path

    def feedback(self, path, pathCost, collisions, timeInQueue, timeInPenalty, timeInTransition):
        raise NotImplementedError("To be implemented in concrete traverser!")

    def nextIteration(self):
        raise NotImplementedError("To be implemented in concrete traverser!")

    def path(self):
        return self.generatePathFromTasks(self._tasksSequence)

    def node(self, index):
        return self.system.node(index)

    def transitionTime(self, nodeIndex1, nodeIndex2):
        return self.system.graph[nodeIndex1, nodeIndex2]

    def bestPath(self):
        return self._bestPath
