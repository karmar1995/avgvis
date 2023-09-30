class Edge:
    def __init__(self, source, destination, weight):
        self.source = source
        self.destination = destination
        self.weight = weight


class Graph:
    def __init__(self):
        self.vs = dict()
        self.es = dict()

    def add_edges(self, edges):
        pass

    def add_vertex(self, node):
        i = len(self.vs)
        self.vs[i] = dict()
        self.vs[i]['node'] = node

    def __getitem__(self, item):
        return 1.0


    def __setitem__(self, key, value):
        pass

    def get_k_shortest_paths(self, s, d, k):
        return [s,d]

