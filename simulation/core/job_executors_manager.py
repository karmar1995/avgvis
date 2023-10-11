import random
from simulation.core.job_executor import JobExecutor, JobExecutorView


class JobExecutorsManager:
    def __init__(self, executorsNumber, taskExecutorsFactory):
        self.__executorsNumber = executorsNumber
        self.__executors = dict()
        self.__taskExecutorsFactory = taskExecutorsFactory
        self.__tasksScheduler = None

    def setTasksScheduler(self, scheduler):
        self.__tasksScheduler = scheduler

    def createExecutors(self):
        for i in range(self.__executorsNumber):
            executor = JobExecutor(self.__taskExecutorsFactory(), self)
            self.__executors[id(executor)] = executor

    def freeExecutors(self):
        res = []
        for executorId in self.__executors:
            if not self.__executors[executorId].busy():
                res.append(self.__executors[executorId])
        return res

    def freeExecutorsNumber(self):
        res = 0
        for executorId in self.__executors:
            if not self.__executors[executorId].busy():
                res += 1
        return res

    def freeExecutor(self):
        executor = None
        while executor is None:
            executorId = random.choice(list(self.__executors.keys()))
            if not self.__executors[executorId].busy():
                executor = self.__executors[executorId]
        return executor

    def onExecutorFinished(self):
        pass

    def executorsNumber(self):
        return len(self.__executors)

    def executorsViews(self):
        res = list()
        for executorId in self.__executors:
            res.append(JobExecutorView(self.__executors[executorId]))
        return res