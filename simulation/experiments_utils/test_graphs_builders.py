from simulation.simpy_adapter.node import Node
from simulation.core.system_builder import *


class FullGraphBuilder:

    def __init__(self, env):
        self.__nodesNumber = 0
        self.__env = env

    def setNodesNumber(self, number):
        self.__nodesNumber = number
        return self

    def build(self, systemBuilder):
        n = self.__nodesNumber
        for i in range(0, n):
            systemBuilder.addVertex(Vertex(node=Node(env=self.__env, serviceTime=i * 100, index=i)))

        for i in range(0, n ):
            for j in range(0, n ):
                systemBuilder.addEdge(Edge(source=i, target=j, weight=10 * i + j))
