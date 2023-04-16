import random
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


class SimpleTraverser:
    def __init__(self, system, controller):
        self.system = system
        self.controller = controller
        self.__paths = None
        self.__source = None
        self.__destination = None
        self.__bestPath = None

    def findPath(self, source, destination):
        self.__source = source
        self.__destination = destination
        self.__paths = self.system.graph.get_k_shortest_paths(source, destination, 3)

    def path(self):
        return random.choice(self.__paths)

    def node(self, index):
        return self.system.node(index)

    def transitionTime(self, nodeIndex1, nodeIndex2):
        time = self.system.graph[nodeIndex1, nodeIndex2]
        return time

    def feedback(self, path, pathCost):
        p = Path(path, pathCost)
        if self.__bestPath is None:
            self.__bestPath = p
        elif self.__bestPath > p:
            self.__bestPath = p
        print("Path: {} cost: {}".format(path, pathCost))
        self.controller.onAgentFinished()

    def bestPath(self):
        return self.__bestPath


class Controller:
    def __init__(self, system, agentsFactory : AgentsFactory, simulation):
        self.__system = system
        self.__agentsFactory = agentsFactory
        self.__traverser = SimpleTraverser(system=system, controller=self)
        self.__simulation = simulation
        self.__iterations = 100
        self.__convergence = 10

    def findPath(self, source, destination):
        self.__traverser.findPath(source, destination)
        self.__startAgent()
        currentPath = None
        for i in range(0, self.__iterations):
            self.__simulation.run()
            if currentPath is None or currentPath > self.__traverser.bestPath():
                currentPath = self.__traverser.bestPath()
                self.__convergence = 10
            else:
                self.__convergence -= 1
            if self.__convergence == 0:
                break
        return currentPath

    def onAgentFinished(self):
        self.__startAgent()

    def __startAgent(self):
        self.__agentsFactory.createAgent({'traverser': self.__traverser}).start()
