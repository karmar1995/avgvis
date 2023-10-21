import time
from simulation.core.task_executor import TaskExecutor
from agv_adapter.agv_frame_builder import AgvFrameBuilder
from agv_adapter.agv_response_parser import AgvResponseParser


class AgvTaskExecutor(TaskExecutor):

    def __init__(self, agvSender):
        self.__agvSender = agvSender

    def execute(self, task):
        frame = AgvFrameBuilder().startFrame().withNodeToVisit(task).consumeFrame()
        try:
            print("Sending task to AGV: {}".format(task))
            self.__waitForAgvResponse(0)
            self.__agvSender.sendDataToServer(frame)
            self.__waitForAgvResponse(0)
        except ConnectionRefusedError as e:
            print("Cannot connect to AGV")

    def __waitForAgvResponse(self, value):
        responseParser = AgvResponseParser(self.__agvSender.readDataFromServer())
        agvResponse = responseParser.getNaturalNavigationCommandFeedback()
        while agvResponse != value:
            responseParser = AgvResponseParser(self.__agvSender.readDataFromServer())
            agvResponse = responseParser.getNaturalNavigationCommandFeedback()
            time.sleep(0.25)
