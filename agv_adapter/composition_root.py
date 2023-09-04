from agv_adapter.agv_task_executors_factory import AgvTaskExecutorFactory


class CompositionRoot:
    def __init__(self):
        self.__executorsFactory = None

    def initialize(self, agvSenders):
        self.__executorsFactory = AgvTaskExecutorFactory(agvSenders)

    def executorsFactory(self):
        return self.__executorsFactory