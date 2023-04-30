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
        for i in range(0, self.__executorsNumber):
            if i not in jobsDict:
                jobsDict[i] = list()
            jobsDict[i].append(tasks.pop(0))
        self.__jobsDict = self.__flatten(jobsDict)

    #techdebt: make __flatten not needed
    def __flatten(self, jobsDict):
        flat = dict()
        for jobId in jobsDict:
            tasks = jobsDict[jobId]
            flat[jobId] = list()
            for task in tasks:
                flat[jobId].append(task.source())
                flat[jobId].append(task.destination())
        return flat

    def coordinateJobs(self, iterations):
        return self.__pathsController.coordinatePaths(self.__jobsDict, iterations)