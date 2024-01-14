import time
from simulation.core.task_executor import TaskExecutor
from agv_adapter.agv_controller_client import AgvControllerClient


class AgvTaskExecutor(TaskExecutor):

    def __init__(self, agvId, agvControllerClient: AgvControllerClient):
        self.__agvId = agvId
        self.__agvControllerClient = agvControllerClient

    def execute(self, task):
        print("Requesting: {} go to point: {}".format(self.__agvId, task))
        self.__agvControllerClient.requestGoToPoints(self.__agvId, [task])
        agvLoc = self.__agvControllerClient.requestAgvStatus(self.__agvId).location
        while agvLoc != str(task):
            time.sleep(1)

    def getId(self):
        return self.__agvId
