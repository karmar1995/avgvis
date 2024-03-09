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

    def initialize(self):
        self.__requestStatus()

    def execute(self, task):
        print("Requesting: {} go to point: {}".format(self.__agvId, task))
        self.__agvControllerClient.requestGoToPoints(self.__agvId, [task])
        while self.getLocation() != str(task):
            self.__requestStatus()
            time.sleep(1)

    def updateStatus(self, status):
        self.__location = status.location

        onlineStatusChanged = self.__online != status.online
        self.__online = status.online

        if onlineStatusChanged:
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
