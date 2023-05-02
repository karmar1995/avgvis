class TasksScheduler:
    def __init__(self, tasksQueue, pathsController, executorsNumber):
        self.__queue = tasksQueue
        self.__pathsController = pathsController
        self.__executorsNumber = executorsNumber
        self.__queue.addQueueObserver(self)
        self.__jobsDict = None

    def onEnqueue(self):
        tasks = self.__queue.consume()
        jobsDict = dict()
        while len(tasks) > 0:
            for i in range(0, self.__executorsNumber):
                if i not in jobsDict:
                    jobsDict[i] = list()
                if len(tasks) > 0:
                    jobsDict[i].append(tasks.pop(0))
        self.__jobsDict = jobsDict

    def coordinateJobs(self, iterations):
        return self.__pathsController.coordinatePaths(self.__jobsDict, iterations)