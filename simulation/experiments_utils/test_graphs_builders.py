from simulation.simpy_adapter.node import Node
from simulation.core.system_builder import *


class VeryLongServiceTimeFullGraphBuilder:

    def __init__(self, nodesNumber):
        self.__nodesNumber = nodesNumber
        self.__env = None

    def setEnvironment(self, env):
        self.__env = env
        return self

    def build(self, systemBuilder):
        n = self.__nodesNumber
        for i in range(0, n):
            systemBuilder.addVertex(Vertex(node=Node(env=self.__env, serviceTime=i * 500, index=i)))

        for i in range(0, n ):
            for j in range(0, n ):
                systemBuilder.addEdge(Edge(source=i, target=j, weight=10 * i + j))


class LongServiceTimeFullGraphBuilder:

    def __init__(self, nodesNumber):
        self.__nodesNumber = nodesNumber
        self.__env = None

    def setEnvironment(self, env):
        self.__env = env
        return self

    def build(self, systemBuilder):
        n = self.__nodesNumber
        for i in range(0, n):
            systemBuilder.addVertex(Vertex(node=Node(env=self.__env, serviceTime=i * 100, index=i)))

        for i in range(0, n ):
            for j in range(0, n ):
                systemBuilder.addEdge(Edge(source=i, target=j, weight=10 * i + j))


class ShortServiceTimeFullGraphBuilder:

    def __init__(self, nodesNumber):
        self.__nodesNumber = nodesNumber
        self.__env = None

    def setEnvironment(self, env):
        self.__env = env
        return self

    def build(self, systemBuilder):
        n = self.__nodesNumber
        for i in range(0, n):
            systemBuilder.addVertex(Vertex(node=Node(env=self.__env, serviceTime=i * 1, index=i)))

        for i in range(0, n ):
            for j in range(0, n ):
                systemBuilder.addEdge(Edge(source=i, target=j, weight=10 * i + j))


class TreeGraphBuilder:

    def __init__(self, switches, hostsPerSwitch):
        self.__switchesNumber = switches
        self.__hostsNumberPerSwitch = hostsPerSwitch
        self.__env = None
        self.__switches = list()
        self.__hosts = list()

    def setEnvironment(self, env):
        self.__env = env
        return self

    def build(self, systemBuilder):
        index = 0
        n = self.__switchesNumber
        for i in range(0, n):
            self.__switches.append(index)
            systemBuilder.addVertex(Vertex(node=Node(env=self.__env, serviceTime=10, index=index)))
            index += 1

        for i in range(0, n ):
            for j in range(0, n ):
                systemBuilder.addEdge(Edge(source=i, target=j, weight=10))

        n = self.__hostsNumberPerSwitch
        for switch in self.__switches:
            for i in range(0, n):
                systemBuilder.addVertex(Vertex(node=Node(env=self.__env, serviceTime=0, index=index)))
                self.__hosts.append(index)
                systemBuilder.addEdge(Edge(source=index, target=switch, weight=1))
                index += 1
