from dataclasses import dataclass
import json


@dataclass
class OrderDefinition:
    orderId: int
    source: int
    destination: int


class MesMappingStorage:
    def __init__(self):
        self.__data = None
        self.__filename = ""

    def read(self, filename):
        self.__filename = filename
        with open(filename, 'r') as f:
            self.__data = json.load(f)

    def ordersDefintions(self):
        nodes = list()
        for node in self.__data['orders']:
            nodes.append(OrderDefinition(int(node['orderId']), int(node['source']), int(node['destination'])))
        return nodes
