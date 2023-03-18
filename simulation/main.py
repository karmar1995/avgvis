import simpy
from simulation.simpy_adapter.node import Node
from simulation.simpy_adapter.agent import Agent
from simulation.core.system_builder import *


class SimpleTraverser:
    def __init__(self, system):
        self.system = system
        self.__path = None

    def setPath(self, path):
        self.__path = path

    def path(self):
        return self.__path

    def node(self, index):
        return self.system.node(index)

    def transitionTime(self, nodeIndex1, nodeIndex2):
        time = self.system.graph[nodeIndex1, nodeIndex2]
        return time


env = simpy.Environment()

builder = SystemBuilder()
builder.addVertex(Vertex(node=Node(env=env, serviceTime=1)))
builder.addVertex(Vertex(node=Node(env=env, serviceTime=1)))
builder.addVertex(Vertex(node=Node(env=env, serviceTime=1)))

builder.addEdge(Edge(source=0, target=1, weight=1))
builder.addEdge(Edge(source=1, target=2, weight=1))

traverser = SimpleTraverser(system=builder.system())
traverser.setPath([0, 1, 2])

agent = Agent(env, 1, traverser)

env.process(agent.run())


env.run(until=40)