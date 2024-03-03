import time
from simulation.core.task_executor import TaskExecutor
from agv_adapter.agv_controller_client import AgvControllerClient


class AgvTaskExecutor(TaskExecutor):

    def __init__(self, agvId, agvControllerClient: AgvControllerClient, initialStatus):
        self.__agvId = agvId
        self.__agvControllerClient = agvControllerClient
        self.__location = initialStatus.location
        self.__online = initialStatus.online

    def initialize(self):
        status = self.__agvControllerClient.requestAgvStatus(self.__agvId)
        self.__location = status.location
        self.__online = status.online

    def execute(self, task):
        print("Requesting: {} go to point: {}".format(self.__agvId, task))
        self.__agvControllerClient.requestGoToPoints(self.__agvId, [task])
        while self.__agvControllerClient.requestAgvStatus(self.__agvId).location != str(task):
            time.sleep(1)

    def getId(self):
        return self.__agvId

    def getLocation(self):
        return self.__location

    def isOnline(self):
        return self.__online
