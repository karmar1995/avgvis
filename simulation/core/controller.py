import random
from simulation.core.agents_factory import AgentsFactory


class SimpleTraverser:
    def __init__(self, system, controller):
        self.system = system
        self.controller = controller
        self.__paths = None
        self.__source = None
        self.__destination = None

    def findPath(self, source, destination):
        self.__source = source
        self.__destination = destination
        self.__paths = self.system.graph.get_k_shortest_paths(source, destination, 5)

    def path(self):
        return random.choice(self.__paths)

    def node(self, index):
        return self.system.node(index)

    def transitionTime(self, nodeIndex1, nodeIndex2):
        time = self.system.graph[nodeIndex1, nodeIndex2]
        return time

    def feedback(self, path, pathCost):
        print("Path: {} cost: {}".format(path, pathCost))
        self.controller.onAgentFinished()


class Controller:
    def __init__(self, system, agentsFactory : AgentsFactory, simulation):
        self.__system = system
        self.__agentsFactory = agentsFactory
        self.__traverser = SimpleTraverser(system=system, controller=self)
        self.__simulation = simulation

    def findPath(self, source, destination):
        self.__traverser.findPath(source, destination)
        self.__startAgent()
        self.__simulation.run()

    def onAgentFinished(self):
        self.__startAgent()

    def __startAgent(self):
        self.__agentsFactory.createAgent({'traverser': self.__traverser}).start()
