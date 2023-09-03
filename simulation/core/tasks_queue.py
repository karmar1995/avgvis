class TasksQueue:
    def __init__(self):
        self.__queue = list()
        self.__queueObservers = list()

    def addQueueObserver(self, observer):
        self.__queueObservers.append(observer)

    def enqueue(self, task):
        self.__queue.append(task)
        self.__notifyOnEnqueue()

    def batchEnqueue(self, tasks):
        self.__queue.extend(tasks)
        self.__notifyOnEnqueue()

    def consume(self):
        res = self.__queue
        self.__queue = list()
        return res

    def __notifyOnEnqueue(self):
        for observer in self.__queueObservers:
            observer.onEnqueue()

    def size(self):
        return len(self.__queue)