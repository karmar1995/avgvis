from agv_adapter.agv_task_executors_manager import AgvTaskExecutorManager


class CompositionRoot:
    def __init__(self):
        self.__executorsManager = None

    def initialize(self, agvSenders):
        self.__executorsManager = AgvTaskExecutorManager(agvSenders)

    def executorsManager(self):
        return self.__executorsManager