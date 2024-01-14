from agv_adapter.agv_task_executors_manager import AgvTaskExecutorManager


class CompositionRoot:
    def __init__(self):
        self.__executorsManager = None

    def initialize(self, agvControllerIp, agvControllerPort):
        self.__executorsManager = AgvTaskExecutorManager(agvControllerIp, agvControllerPort)

    def executorsManager(self):
        return self.__executorsManager