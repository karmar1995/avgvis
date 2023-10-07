import time
from simulation.core.task_executor import TaskExecutor
from agv_adapter.frame_builder import FrameBuilder


class AgvTaskExecutor(TaskExecutor):

    def __init__(self, agvSender):
        self.__agvSender = agvSender
        self.__frameBuilder = FrameBuilder()

    def execute(self, task):
        frame = self.__frameBuilder.startFrame().withNodeToVisit(task).consumeFrame()
        try:
            print("Sending task to AGV: {}".format(task))
            self.__waitForAgvResponse(0)
            self.__agvSender.sendDataToServer(frame)
            self.__waitForAgvResponse(0)
        except ConnectionRefusedError as e:
            print("Cannot connect to AGV")

    def __waitForAgvResponse(self, value):
        agvResponse = int.from_bytes(self.__agvSender.readDataFromServer(), 'big')
        while agvResponse != value:
            agvResponse = int.from_bytes(self.__agvSender.readDataFromServer(), 'big')
            time.sleep(0.25)
