import threading


class TrafficController:
    def __init__(self, system):
        self.__system = system
        self.__lock = threading.Lock()

    def requestPath(self, source, destination, executor):
        k = 3
        sourceNode = self.__system.node(source)
        destinationNode = self.__system.node(destination)
        with self.__lock:
            paths = self.__system.graph.get_k_shortest_paths(sourceNode.index, destinationNode.index, k=k)
            for path in paths:
                if self.__freePath(path):
                    self.__assignPath(path, executor)
                    return path
        return None

    def revokePath(self, path, executor):
        with self.__lock:
            self.__unassignPath(path, executor)

    def __freePath(self, path):
        i = 1
        print("Checking path: ", str(path))
        while i < len(path):
            executors = self.__system.edgeExecutors(path[i - 1], path[i])
            if len(executors) > 0:
                return False
            i += 1
        return True

    def __assignPath(self, path, executor):
        print("Assigning path: ", str(path))
        i = 1
        while i < len(path):
            self.__system.edgeExecutors(path[i - 1], path[i])[id(executor)] = executor
            i += 1
        print("Path assigned: ", str(path))

    def __unassignPath(self, path, executor):
        i = 1
        while i < len(path):
            del self.__system.edgeExecutors(path[i - 1], path[i])[id(executor)]
            i += 1
