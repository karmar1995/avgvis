from simulation.core.task_executor import TaskExecutor
import threading


class JobExecutor:
    def __init__(self, actualExecutor: TaskExecutor, owner):
        self.__job = None
        self.__taskExecutor = actualExecutor
        self.__currentTask = 0
        self.__busy = False
        self.__owner = owner
        self.__thread = None

    def busy(self):
        return self.__busy

    def executeJob(self, job):
        self.__busy = True
        self.__currentTask = 0
        self.__job = job
        self.__thread = threading.Thread(target=self.__executeJob)
        self.__thread.daemon = True
        self.__thread.start()

    def wait(self):
        self.__thread.join()
        self.__thread = None

    def __executeJob(self):
        for i in range(0, len(self.__job)):
            self.__currentTask = i
            self.__taskExecutor.execute(self.__job[self.__currentTask])
        self.__onJobFinished()

    def __onJobFinished(self):
        self.__job = None
        self.__busy = False
        self.__owner.onExecutorFinished()

