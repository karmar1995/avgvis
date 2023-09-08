from simulation.core.task_executor import TaskExecutor
from agv_adapter.frame_builder import FrameBuilder


class AgvTaskExecutor(TaskExecutor):

    def __init__(self, agvSender):
        self.__agvSender = agvSender
        self.__frameBuilder = FrameBuilder()

    def execute(self, task):
        frame = self.__frameBuilder.startFrame().withNodeToVisit(task).consumeFrame()
        self.__agvSender.sendDataToServer(frame)
