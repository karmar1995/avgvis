from agv_adapter.agv_task_executor import AgvTaskExecutor


class AgvTaskExecutorFactory:
    def __init__(self, agvsSenders):
        self.__agvsSenders = agvsSenders

    def __call__(self, *args, **kwargs):
        try:
            return AgvTaskExecutor(self.__agvsSenders.pop())
        except IndexError:
            raise Exception("Number of available executors exceeded!")