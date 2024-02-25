import threading


class TrafficController:
    def __init__(self, system):
        self.__system = system
        self.__lock = threading.Lock()

    def requestPath(self, source, destination, executor):
        k = 3
        with self.__lock:
            paths = self.__system.graph.get_k_shortest_paths(source.index, destination.index, k=k)
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
        while i < len(path):
            executors = self.__system.edgeExecutors(path[i - 1], path[i])
            if len(executors) > 0:
                return False
        return True

    def __assignPath(self, path, executor):
        i = 1
        while i < len(path):
            self.__system.edgeExecutors(path[i - 1], path[i])[id(executor)] = executor

    def __unassignPath(self, path, executor):
        i = 1
        while i < len(path):
            del self.__system.edgeExecutors(path[i - 1], path[i])[id(executor)]
