from dataclasses import dataclass
import threading, time


@dataclass
class Node:
    id: str
    x: float
    y: float


class AgvState:
    def __init__(self):
        self.x = None
        self.y = None


steps = 10
sleepTime = 0.1


class AgvLogic:
    def __init__(self, nodes):
        self.__nodes = dict()
        for node in nodes:
            self.__nodes[node.id] = node
        self.__observers = dict()
        self.__currentNode = nodes[0]
        self.__nextNode = None
        self.__nodesQueue = list()
        self.__thread = threading.Thread(target=self.__move)
        self.__working = False
        self.__state = AgvState()
        self.__state.x = self.__currentNode.x
        self.__state.y = self.__currentNode.y

    def addObserver(self, observer):
        self.__observers[id(observer)] = observer

    def removeObserver(self, observer):
        del self.__observers[id(observer)]

    def goToNode(self, nodeId):
        self.__nodesQueue.append(nodeId)
        if not self.__working:
            self.__working = True
            self.__thread.start()

    def x(self):
        return self.__state.x

    def y(self):
        return self.__state.y

    def __move(self):
        while len(self.__nodesQueue) > 0:
            self.__moveToNode(self.__nodes[self.__nodesQueue.pop(0)])

    def __moveToNode(self, nextNode):
        self.__nextNode = nextNode
        dx = nextNode.x - self.__state.x
        dy = nextNode.y - self.__state.y
        for i in range(0, steps):
            self.__state.x += dx / steps
            self.__state.y += dy / steps
            self.__onStateChanged()
            time.sleep(sleepTime)

    def __onStateChanged(self):
        for observerId in self.__observers:
                self.__observers[observerId].onAgvStateChanged(self)


