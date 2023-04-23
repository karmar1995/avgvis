import random, copy
from simulation.core.agents_factory import AgentsFactory


class Path:
    def __init__(self, path, cost):
        self.path = path
        self.cost = cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __lt__(self, other):
        return other > self

    def __eq__(self, other):
        return not self > other and not other > self


class SimulatedAnnealingTraverser:
    def __init__(self, system, controller, nodesToVisit):
        self.system = system
        self.controller = controller
        self.__bestPath = None
        self.__nodesToVisit = nodesToVisit
        self.__generateInitialPath()
        self.__temperature = 1.0

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
            random.shuffle(self.__path)

    def path(self):
        self.__generatePath()
        return self.__path

    def node(self, index):
        return self.system.node(index)

    def nodeNeedsVisitation(self, index):
        return index in self.__nodesToVisit

    def transitionTime(self, nodeIndex1, nodeIndex2):
        time = self.system.graph[nodeIndex1, nodeIndex2]
        return time

    def feedback(self, path, pathCost):
        self.__performStateTransition(Path(path, pathCost))

    def __performStateTransition(self, newPath):
        if self.__bestPath is None:
            self.__bestPath = newPath
        else:
            if random.random() < self.__transitionProbability(currentEnergy=self.__bestPath.cost, newEnergy=newPath.cost):
                self.__bestPath = newPath

    def __transitionProbability(self, currentEnergy, newEnergy):
        minimalUpwardTransitionProbability = 0.01
        upwardsTransitionProbability = (0.1 * self.__temperature) + minimalUpwardTransitionProbability
        if newEnergy > currentEnergy:
            return upwardsTransitionProbability
        return 1 - upwardsTransitionProbability

    def bestPath(self):
        return self.__bestPath


class Controller:
    def __init__(self, system, agentsFactory : AgentsFactory, simulation):
        self.__system = system
        self.__agentsFactory = agentsFactory
        self.__simulation = simulation
        self.__iterations = 200

    def coordinatePaths(self, jobsDict):
        def assignTraversersToResult(__res, __traversers):
            for __jobId in __traversers:
                __res[__jobId] = __traversers[__jobId].bestPath()

        traversers = dict()
        res = dict()

        for jobId in jobsDict:
            traversers[jobId] = SimulatedAnnealingTraverser(system=self.__system, controller=self, nodesToVisit=jobsDict[jobId])

        for i in range(0, self.__iterations):
            for jobId in jobsDict:
                self.__startAgent(traversers[jobId])

            self.__simulation.run()

            currentOverallCost = 0
            newOverallCost = 0
            for jobId in res:
                currentOverallCost += res[jobId].cost
                newOverallCost += traversers[jobId].bestPath().cost

            if len(res) == 0 or currentOverallCost > newOverallCost:
                assignTraversersToResult(res, traversers)

        return res

    def __startAgent(self, traverser):
        self.__agentsFactory.createAgent({'traverser': traverser}).start()
