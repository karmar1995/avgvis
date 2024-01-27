import time, threading


class TasksScheduler:
    def __init__(self, executorsManager, queueOptimizer):
        self.__executorsManager = executorsManager
        self.__queueOptimizer = queueOptimizer
        self.__jobsDict = None
        self.__tasksSources = dict()
        self.__queueProcessingThread = None
        self.__killed = False
        self.__idle = False
        self.__started = False
        self.__tasksGuard = False

    def __processQueue(self):
        self.__started = True
        while not self.__killed:
            self.optimizeQueue(iterations=100)  # todo: un-hardcode this stuff
            time.sleep(1)

    # public only for testing purposes
    def optimizeQueue(self, iterations):
        return self.__queueOptimizer.optimizeQueue(iterations)

    # only for testing purposes
    def waitForQueueProcessed(self):
        for i in range(0, 15):
            time.sleep(0.5)
            if self.__started:
                break
        if self.__started:
            while not self.__idle:
                time.sleep(0.5)
            while self.__executorsManager.freeExecutorsNumber() < self.__executorsManager.executorsNumber():
                time.sleep(1)
        else:
            raise Exception("Queue not started yet!")

    def start(self):
        self.__queueProcessingThread = threading.Thread(target=self.__processQueue)
        self.__queueProcessingThread.daemon = True
        self.__queueProcessingThread.start()

    def shutdown(self):
        self.__killed = True
        self.__queueProcessingThread.join()
        self.__queueProcessingThread = None