import time, threading
from simulation.core.tasks_source import TasksSource


MAX_JOB_LENGTH = 10


class TasksScheduler:
    def __init__(self, tasksQueue, pathsController, executorsManager):
        self.__queue = tasksQueue
        self.__pathsController = pathsController
        self.__executorsManager = executorsManager
        self.__queue.addQueueObserver(self)
        self.__jobsDict = None
        self.__tasksSources = dict()
        self.__tasks = list()
        self.__queueProcessingThread = threading.Thread(target=self.__processQueue)
        self.__queueProcessingThread.daemon = True
        self.__killed = False
        self.__idle = False
        self.__started = False
        self.__queueProcessingThread.start()
        self.__tasksGuard = False

    def onEnqueue(self):
        if not self.__tasksGuard:
            self.__tasks.extend(self.__queue.consume())

    def tasks(self):
        return self.__tasks

    def __processQueue(self):
        self.__started = True
        while not self.__killed:
            print("Queue length: {}".format(len(self.__tasks)))
            if len(self.__tasks) > 0 and self.__executorsManager.freeExecutorsNumber() > 0:
                jobsDict = dict()
                length = 0
                self.__tasksGuard = True
                while len(self.__tasks) > 0:
                    freeExecutors = self.__executorsManager.freeExecutorsNumber()
                    for i in range(0, freeExecutors):
                        if len(self.__tasks) == 0 or length >= MAX_JOB_LENGTH:
                            break
                        if i not in jobsDict:
                            jobsDict[i] = list()
                        if len(self.__tasks) > 0:
                            jobsDict[i].append(self.__tasks.pop(0))
                            length += 1
                    if length >= MAX_JOB_LENGTH:
                        break
                self.__tasksGuard = False
                self.__jobsDict = jobsDict
                pathsPerJobId = self.coordinateJobs(iterations=100)  # todo: un-hardcode this stuff
                for jobId in pathsPerJobId:
                    self.__executorsManager.freeExecutor().executeJob(pathsPerJobId[jobId].path)
                self.__idle = False
            else:
                self.__idle = True
                time.sleep(0.1)

    def addTasksSource(self, source: TasksSource):
        self.__tasksSources[id(source)] = source
        source.setTasksQueue(self.__queue)

    def removeTasksSource(self, source):
        del self.__tasksSources[id(source)]

    # public only for testing purposes
    def coordinateJobs(self, iterations):
        return self.__pathsController.coordinatePaths(self.__jobsDict, iterations)

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

    def shutdown(self):
        self.__killed = True
        self.__queueProcessingThread.join()
        self.__queueProcessingThread = None