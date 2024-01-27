import copy


class TasksQueueView:
    def __init__(self, cost, sequence):
        self.cost = cost
        self.sequence = sequence


class TasksQueue:
    def __init__(self):
        self.__queue = list()
        self.__pendingTasks = list()
        self.__optimizationInProgress = False
        self.__cost = -1

    def enqueue(self, task):
        if self.__optimizationInProgress:
            self.__pendingTasks.append(task)
        else:
            self.__queue.append(task)

    def batchEnqueue(self, tasks):
        if self.__optimizationInProgress:
            self.__pendingTasks.extend(tasks)
        else:
            self.__queue.extend(tasks)

    def onOptimizationStart(self):
        self.__optimizationInProgress = True

    def onOptimizationFinished(self, newSequence, cost):
        if self.__cost == -1 or cost < self.__cost:
            self.__queue = newSequence
            self.__cost = cost
        self.__queue.extend(self.__pendingTasks)
        self.__optimizationInProgress = False

    def tasksList(self):
        return copy.deepcopy(self.__queue)

    def pendingTasksList(self):
        return copy.deepcopy(self.__pendingTasks)

    def size(self):
        return len(self.__queue)

    def queueView(self):
        return TasksQueueView(self.__cost, self.tasksList())