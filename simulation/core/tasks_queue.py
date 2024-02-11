import copy, threading


class TasksQueueView:
    def __init__(self, queue):
        self.queue = queue

    def cost(self):
        return self.queue.cost()

    def tasksList(self):
        return self.queue.tasksList()

    def pendingTasksList(self):
        return self.queue.pendingTasksList()


class TasksQueue:
    def __init__(self):
        self.__queue = list()
        self.__pendingTasks = list()
        self.__cost = -1
        self.__lock = threading.Lock()
        self.__pendingLock = threading.Lock()

    def enqueue(self, task):
        if self.__lock.acquire(blocking=False):
            print("Enqueue: {}".format(task))
            self.__queue.append(task)
            self.__lock.release()
        else:
            self.__pendingLock.acquire()
            print("Enqueue pending: {}".format(task))
            self.__pendingTasks.append(task)
            self.__pendingLock.release()

    def batchEnqueue(self, tasks):
        if self.__lock.acquire(blocking=False):
            print("Enqueue: {}".format(tasks))
            self.__queue.extend(tasks)
            self.__lock.release()
        else:
            print("Enqueue pending: {}".format(tasks))
            self.__pendingLock.acquire()
            self.__pendingTasks.extend(tasks)
            self.__pendingLock.release()

    def onOptimizationStart(self):
        self.__lock.acquire()
        print("Optimizing queue start")

    def onOptimizationFeedback(self, newSequence, cost):
        self.__queue = newSequence
        self.__cost = cost

    def onOptimizationFinished(self):
        self.__pendingLock.acquire()
        self.__queue.extend(self.__pendingTasks)
        self.__pendingTasks = list()
        self.__pendingLock.release()
        self.__lock.release()
        print("Optimizing queue finished")

    def tasksList(self):
        return copy.deepcopy(self.__queue)

    def pendingTasksList(self):
        return copy.deepcopy(self.__pendingTasks)

    def size(self):
        return len(self.__queue)

    def queueView(self):
        return TasksQueueView(self)

    def popTask(self):
        return self.__queue.pop(0)

    def empty(self):
        return len(self.__queue) == 0

    def cost(self):
        return self.__cost