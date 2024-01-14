from simulation.core.tasks_executor_manager import TasksExecutorManager
from agv_adapter.agv_task_executor import AgvTaskExecutor
from agv_adapter.agv_controller_client import AgvControllerClient


class AgvTaskExecutorManager(TasksExecutorManager):
    def __init__(self, agvControllerIp, agvControllerPort):
        self.__agvControllerClient = AgvControllerClient(agvControllerIp, agvControllerPort)
        self.__agvTaskExecutors = dict()
        for agvId in self.__agvControllerClient.requestAgvsIds():
            agvStatus = self.__agvControllerClient.requestAgvStatus(agvId)
            if agvStatus.online:
                self.__agvTaskExecutors[agvId] = AgvTaskExecutor(agvId, self.__agvControllerClient)

    def tasksExecutors(self):
        return list(self.__agvTaskExecutors.values())
