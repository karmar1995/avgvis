import time, random
from simulation.core.task_executor import TaskExecutor, TaskExecutorException


BASE_POLLING_PROBABILITY = 0.1


class AgvTaskExecutor(TaskExecutor):

    def __init__(self, agvId, agvStatusProvider, agvRequestor, statusObserver, initialStatus):
        self.__agvId = agvId
        self.__agvStatusProvider = agvStatusProvider
        self.__agvRequestor = agvRequestor
        self.__statusObserver = statusObserver
        self.__location = initialStatus.location
        self.__online = initialStatus.online
        self.__status = ""
        self.__killed = False

    def initialize(self):
        self.__requestStatus()

    def execute(self, task, taskId):
        self.__agvRequestor.requestGoToPoints(self.__agvId, task, taskId)

        def locationPredicate():
            return self.getLocation() == str(task[0])

        def statusPredicate():
            return self.__status != 'busy'

        self.__waitFor(locationPredicate)
        self.__waitFor(statusPredicate)

    def updateStatus(self, status):
        if status is None:
            return
        self.__location = status.location

        onlineStatusChanged = self.__online != status.online
        self.__online = status.online
        self.__status = status.status

        if onlineStatusChanged:
            self.__statusObserver.onExecutorChanged()

    def assumeOffline(self):
        self.__online = False
        self.__statusObserver.onExecutorChanged()

    def getId(self):
        return self.__agvId

    def getLocation(self):
        return self.__location

    def isOnline(self):
        return self.__online

    def kill(self):
        self.__killed = True

    def __requestStatus(self):
        status = self.__agvStatusProvider.getAgvStatus(self.__agvId)
        if status is not None:
            self.updateStatus(status)
        return status is not None

    def __waitFor(self, predicate):
        pollingProbability = BASE_POLLING_PROBABILITY
        retries = 10
        sleepTime = 0.5
        while not predicate():
            if self.__killed:
                raise TaskExecutorException()

            if retries == 0:
                self.assumeOffline()
                return
            if random.random() < pollingProbability:
                pollingProbability += BASE_POLLING_PROBABILITY
                if not self.__requestStatus():
                    retries -= 1
            time.sleep(random.uniform(sleepTime * 0.5, sleepTime * 1.5))
