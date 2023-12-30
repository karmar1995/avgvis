from simulation.core.agents_factory import AgentsFactory
from simulation.core.simulated_annealing_traverser import SimulatedAnnealingTraverser


class PathsController:
    def __init__(self, system, agentsFactory : AgentsFactory, simulation):
        self.__system = system
        self.__agentsFactory = agentsFactory
        self.__simulation = simulation

    def coordinatePaths(self, jobsDict, iterations, traverserFactory=SimulatedAnnealingTraverser):
        def assignTraversersToResult(__res, __traversers):
            for __jobId in __traversers:
                __res[__jobId] = __traversers[__jobId].bestPath()

        traversers = dict()
        res = dict()

        for jobId in jobsDict:
            traversers[jobId] = traverserFactory(system=self.__system, nodesToVisit=jobsDict[jobId], maxIterations=iterations)

        for i in range(0, iterations):
            for jobId in jobsDict:
                traverser = traversers[jobId]
                self.__startAgent(traverser)
                traverser.nextIteration()

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
