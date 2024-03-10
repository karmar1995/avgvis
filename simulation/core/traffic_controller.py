import threading


LOCK_RANGE = 5


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
            path = self.__pickFreePath(paths)
            if path is None:
                path = self.__pickPartiallyFreePath(paths)
            if path is not None:
                self.__assignSegment(path, executor, 0, LOCK_RANGE)
                return path
        return None

    def requestNextSegment(self, path, executor, startingPoint):
        with self.__lock:
            self.__unassignSegment(path, executor, startingPoint - 1, LOCK_RANGE)
            if self.__segmentFree(path, startingPoint, LOCK_RANGE):
                self.__assignSegment(path, executor, startingPoint, LOCK_RANGE)
                return True
        return False

    def segmentNodes(self, path, startingPoint):
        return self.__segmentNodes(path, startingPoint, LOCK_RANGE)

    def revokePath(self, path, executor):
        with self.__lock:
            self.__unassignSegment(path, executor, 0, len(path))

    def __pickFreePath(self, paths):
        for path in paths:
            if self.__freePath(path):
                return path
        return None

    def __pickPartiallyFreePath(self, paths):
        for path in paths:
            if self.__partiallyFreePath(path):
                return path
        return None

    def __freePath(self, path):
        i = 1
        while i < len(path):
            executors = self.__system.edgeExecutors(path[i - 1], path[i])
            if len(executors) > 0:
                return False
            i += 1
        return True

    def __partiallyFreePath(self, path):
        return self.__segmentFree(path, 0, LOCK_RANGE)

    def __segmentFree(self, path, startingPoint, endingPoint):
        i = startingPoint + 1
        while i < len(path):
            executors = self.__system.edgeExecutors(path[i - 1], path[i])
            if len(executors) > 0:
                return False
            if (i - startingPoint - 1) == endingPoint:
                break
            i += 1
        return True
    def __segmentNodes(self, path, startingPoint, endingPoint):
        i = startingPoint
        segmentNodes = []
        while i < len(path):
            segmentNodes.append(path[i])
            i += 1
            if (i - startingPoint) == endingPoint:
                break
        return segmentNodes

    def __assignSegment(self, path, executor, startingPoint, endingPoint):
        i = startingPoint + 1
        while i < len(path):
            segmentExecutors = self.__system.edgeExecutors(path[i - 1], path[i])
            if len(segmentExecutors) > 1:
                raise Exception("Segment assigned to multiple agents!")
            segmentExecutors[id(executor)] = executor
            i += 1
            if (i - startingPoint - 1) == endingPoint:
                break

    def __unassignSegment(self, path, executor, startingPoint, endingPoint):
        i = startingPoint + 1
        while i < len(path):
            segmentExecutors = self.__system.edgeExecutors(path[i - 1], path[i])
            if id(executor) in segmentExecutors:
                del segmentExecutors[id(executor)]
            i += 1
            if (i - startingPoint - 1) == endingPoint:
                break
