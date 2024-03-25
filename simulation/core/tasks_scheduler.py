import time, threading


class TasksScheduler:
    def __init__(self, executorsManager, queueOptimizer):
        self.__executorsManager = executorsManager
        self.__queueOptimizer = queueOptimizer
        self.__jobsDict = None
        self.__tasksSources = dict()
        self.__queueProcessingThread = None
        self.__executorsManagerThread = None
        self.__killed = False
        self.__idle = False
        self.__started = False
        self.__tasksGuard = False

    def __processQueue(self):
        self.__started = True
        while not self.__killed:
            self.optimizeQueue(iterations=1000)  # todo: un-hardcode this stuff
            self.dispatchTasks()
            time.sleep(1)

    def __processExecutors(self):
        while not self.__killed:
            self.__executorsManager.performRequests()
            self.__executorsManager.refreshExecutors()
            time.sleep(1)

    # public only for testing purposes
    def optimizeQueue(self, iterations):
        return self.__queueOptimizer.optimizeQueue(iterations)

    def dispatchTasks(self):
        for _ in range(0, self.__executorsManager.freeExecutorsNumber()):
            if not self.__queueOptimizer.queue().empty():
                task = self.__queueOptimizer.queue().nextTask()
                executor = self.__executorsManager.closestFreeExecutor(task)
                if executor is not None:
                    executor.executeJob([self.__queueOptimizer.queue().popTask()])

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

    def __startQueueProcessingThread(self):
        self.__queueProcessingThread = threading.Thread(target=self.__processQueue)
        self.__queueProcessingThread.daemon = True
        self.__queueProcessingThread.start()

    def __startExecutorsProcessingThread(self):
        self.__executorsManagerThread = threading.Thread(target=self.__processExecutors)
        self.__executorsManagerThread.daemon = True
        self.__executorsManagerThread.start()

    def start(self):
        self.__startQueueProcessingThread()
        self.__startExecutorsProcessingThread()

    def shutdown(self):
        self.__killed = True
        self.__queueProcessingThread.join()
        self.__queueProcessingThread = None
        self.__executorsManagerThread.join()
        self.__executorsManagerThread = None
