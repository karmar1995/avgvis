from simulation.core.task_executor import TaskExecutor
import threading, time


class JobExecutor:
    def  __init__(self, actualExecutor: TaskExecutor, owner):
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

    def tasksCount(self):
        if self.__job is None:
            return 0
        return len(self.__job) - self.__currentTask

    def taskExecutorId(self):
        return self.__taskExecutor.getId()

    def job(self):
        return self.__job

    def currentTask(self):
        return self.__currentTask

    def __executeJob(self):
        for i in range(0, len(self.__job)):
            self.__currentTask = i
            points = self.__job[self.__currentTask].pointsSequence()
            path = self.__waitForFreePath(points[0], points[1])
            for point in path:
                self.__taskExecutor.execute(point)
            self.__owner.trafficController().revokePath(path, self)
        self.__onJobFinished()

    def __onJobFinished(self):
        self.__job = None
        self.__busy = False
        self.__currentTask = 0
        self.__owner.onExecutorFinished()

    def __waitForFreePath(self, source, destination):
        path = self.__owner.trafficController().requestPath(source, destination, self)
        while path is None:
            path = self.__owner.trafficController().requestPath(source, destination, self)
            time.sleep(1)
        return path

class JobExecutorView:
    def __init__(self, jobExecutor: JobExecutor):
        self.__executor = jobExecutor

    def tasksCount(self):
        return self.__executor.tasksCount()

    def executorId(self):
        return self.__executor.taskExecutorId()

    def tasksSequence(self):
        job = self.__executor.job()
        if job is not None:
            return job[self.__executor.currentTask():]
        return []