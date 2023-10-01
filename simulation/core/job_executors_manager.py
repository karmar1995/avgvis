import random
from simulation.core.job_executor import JobExecutor


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

    def freeExecutorsNumber(self):
        res = 0
        for executorId in self.__executors:
            if not self.__executors[executorId].busy():
                res += 1
        return res

    def freeExecutor(self):
        for i in range(0, len(self.__executors)):
            executorId = random.choice(list(self.__executors.keys()))
            if not self.__executors[executorId].busy():
                return self.__executors[executorId]
        return None

    def onExecutorFinished(self):
        pass

    def executorsNumber(self):
        return len(self.__executors)