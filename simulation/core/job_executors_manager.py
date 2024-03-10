import random
from simulation.core.job_executor import JobExecutor, JobExecutorView
from simulation.core.tasks_executor_manager import TasksExecutorManager


class JobExecutorsManager:
    def __init__(self, taskExecutorsManager : TasksExecutorManager, trafficController, queue):
        self.__executors = dict()
        self.__taskExecutorsManager = taskExecutorsManager
        self.__taskExecutorsManager.addTasksExecutorObserver(self)
        self.__trafficController = trafficController
        self.__queue = queue

    def freeExecutors(self):
        res = []
        for executorId in self.__executors:
            if self.__executors[executorId].availableForJobs():
                res.append(self.__executors[executorId])
        return res

    def freeExecutorsNumber(self):
        res = 0
        for executorId in self.__executors:
            if self.__executors[executorId].availableForJobs():
                res += 1
        return res

    def freeExecutor(self):
        executor = None
        while executor is None:
            executorId = random.choice(list(self.__executors.keys()))
            if self.__executors[executorId].availableForJobs():
                executor = self.__executors[executorId]
        return executor

    def closestFreeExecutor(self, task):
        candidates = self.freeExecutors()
        closestCost = None
        closestExecutor = None
        for executor in candidates:
            source = int(executor.location())
            destination = task.source()
            transitCost = self.trafficController().lowestCost(source, destination)
            if closestCost is None or closestCost > transitCost:
                closestCost = transitCost
                closestExecutor = executor
        return closestExecutor

    def onExecutorFinished(self):
        pass

    def executorsNumber(self):
        return len(self.__executors)

    def onlineExecutorsNumber(self):
        res = 0
        for executorId in self.__executors:
            if self.__executors[executorId].online():
                res += 1
        return res

    def executorsViews(self):
        res = list()
        for executorId in self.__executors:
            res.append(JobExecutorView(self.__executors[executorId]))
        return res

    def onTasksExecutorsChanged(self):
        self.__unregisterUnavailableExecutors()
        self.__refreshAvailableExecutors()

    def refreshExecutors(self):
        self.__taskExecutorsManager.refreshTasksExecutors()

    def trafficController(self):
        return self.__trafficController

    def __unregisterUnavailableExecutors(self):
        executorsToCleanup = []
        for executorId in self.__executors:
            found = False
            for tasksExecutor in self.__taskExecutorsManager.tasksExecutors():
                if tasksExecutor.getId() == executorId:
                    found = True
                    break
            if not found:
                executorsToCleanup.append(executorId)

        for executorId in executorsToCleanup:
            self.__revokeJobFromUnavailableExecutor(self.__executors[executorId])
            del self.__executors[executorId]

    def __revokeJobFromUnavailableExecutor(self, executor):
        self.__queue.batchEnqueue(executor.remainingJob())
        executor.kill()

    def __refreshAvailableExecutors(self):
        for tasksExecutor in self.__taskExecutorsManager.tasksExecutors():
            executorId = tasksExecutor.getId()
            if executorId not in self.__executors:
                self.__executors[executorId] = JobExecutor(tasksExecutor, self)
            else:
                if not tasksExecutor.isOnline() and self.__executors[executorId].busy():
                    self.__revokeJobFromUnavailableExecutor(self.__executors[executorId])
