import simpy
from simulation.simpy_adapter.node import Node
from simulation.core.system_builder import *
from simulation.core.controller import Controller
from simulation.simpy_adapter.simpy_agents_factory import SimpyAgentsFactory


def buildTestGraph(builder):
    for i in range(0, 10):
        builder.addVertex(Vertex(node=Node(env=env, serviceTime=1)))

    for i in range(0, 10):
        for j in range(0, 10):
            builder.addEdge(Edge(source=i, target=j, weight=10 * i + j))


class EnvironmentWrapper:
    def __init__(self, environment, timeout):
        self.__env = environment
        self.__timeout = timeout

    def run(self):
        self.__env.run(until=self.__timeout)


env = simpy.Environment()
simulation = EnvironmentWrapper(environment=env, timeout=10000)
simpyAgentsFactory = SimpyAgentsFactory(env=env)

systemBuilder = SystemBuilder()
buildTestGraph(systemBuilder)

controller = Controller(system=systemBuilder.system(), agentsFactory=simpyAgentsFactory, simulation=simulation)
controller.findPath(0, 3)
