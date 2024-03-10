import time
from simulation.core.task_executor import TaskExecutor
from agv_adapter.agv_controller_client import AgvControllerClient


class AgvTaskExecutor(TaskExecutor):

    def __init__(self, agvId, agvControllerClient: AgvControllerClient, initialStatus, statusObserver):
        self.__agvId = agvId
        self.__agvControllerClient = agvControllerClient
        self.__location = initialStatus.location
        self.__online = initialStatus.online
        self.__statusObserver = statusObserver
        self.__status = ""

    def initialize(self):
        self.__requestStatus()

    def execute(self, task, taskId):
        print("Requesting: {} go to point: {}".format(self.__agvId, task))
        self.__agvControllerClient.requestGoToPoints(self.__agvId, task, taskId)

        def locationPredicate():
            return self.getLocation() == str(task[0])

        def statusPredicate():
            print("Waiting for status not busy, current: {}".format(self.__status))
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

    def __requestStatus(self):
        status = self.__agvControllerClient.requestAgvStatus(self.__agvId)
        if status is not None:
            self.updateStatus(status)
        return status is not None

    def __waitFor(self, predicate):
        retries = 10
        while not predicate():
            if retries == 0:
                self.assumeOffline()
                return
            if not self.__requestStatus():
                retries -= 1
            time.sleep(1)
