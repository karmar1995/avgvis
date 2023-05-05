from igraph import Graph


class System:
    def __init__(self):
        self.graph = Graph()

    def node(self, index):
        return self.graph.vs[index]['node']

    def edgeWeight(self, source, destination):
        return self.graph[source, destination]

    def nodesCount(self):
        return len(self.graph.vs)