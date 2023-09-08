from simulation.simpy_adapter.node import Node
from simulation.core.system_builder import *


class TopologyBuilder:

    def __init__(self, env, dataSource):
        self.__env = env
        self.__ds = dataSource

    def build(self, systemBuilder):

        for nodeDescription in self.__ds.nodesDescriptions():
            systemBuilder.addVertex(Vertex(node=Node(env=self.__env, serviceTime=nodeDescription.serviceTime, index=nodeDescription.index), name='unused'))

        for edgeDescription in self.__ds.edgesDescriptions():
            systemBuilder.addEdge(Edge(source=edgeDescription.firstNode, target=edgeDescription.secondNode, weight=edgeDescription.transitionTime, name='unused'))

