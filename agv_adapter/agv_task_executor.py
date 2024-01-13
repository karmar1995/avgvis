import time
from simulation.core.task_executor import TaskExecutor
from agv_adapter.agv_frame_builder import AgvFrameBuilder
from agv_adapter.agv_response_parser import AgvResponseParser
from agv_adapter.agv_controller_client import AgvControllerClient


class AgvTaskExecutor(TaskExecutor):

    def __init__(self, agvId, agvControllerClient: AgvControllerClient):
        self.__agvId = agvId
        self.__agvControllerClient = agvControllerClient

    def execute(self, task):
        self.__agvControllerClient.requestGoToPoints([task])
        while self.__agvControllerClient.requestAgvStatus(self.__agvId).location != str(task):
            time.sleep(1)

    def getId(self):
        raise self.__agvId
