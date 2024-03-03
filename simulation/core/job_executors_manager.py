import random
from simulation.core.job_executor import JobExecutor, JobExecutorView
from simulation.core.tasks_executor_manager import TasksExecutorManager


class JobExecutorsManager:
    def __init__(self, taskExecutorsManager : TasksExecutorManager, trafficController):
        self.__executors = dict()
        self.__taskExecutorsManager = taskExecutorsManager
        self.__taskExecutorsManager.addTasksExecutorObserver(self)
        self.__trafficController = trafficController

    def createExecutors(self):
        self.__executors = dict()
        for tasksExecutor in self.__taskExecutorsManager.tasksExecutors():
            self.__executors[tasksExecutor.getId()] = JobExecutor(tasksExecutor, self)

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

    def onTasksExecutorsChanged(self):
        self.createExecutors()

    def trafficController(self):
        return self.__trafficController