from dataclasses import dataclass
import json


@dataclass
class NodeInfo:
    name: str
    x: float
    y: float
    serviceTime: float


@dataclass
class EdgeInfo:
    name: str
    source: str
    target: str
    transitionTime: float


class GraphStorage:
    def __init__(self):
        self.__data = None
        self.__filename = ""

    def read(self, filename):
        self.__filename = filename
        with open(filename, 'r') as f:
            self.__data = json.load(f)

    def nodes(self):
        nodes = list()
        for node in self.__data['nodes']:
            nodes.append(NodeInfo(node['name'], float(node['x']), float(node['y']), float(node['serviceTime'])))
        return nodes

    def edges(self):
        edges = list()
        for edge in self.__data['edges']:
            edges.append(EdgeInfo(edge['name'], edge['source'], edge['target'], float(edge['transitionTime'])))
        return edges

