from dataclasses import dataclass
from mes_adapter.mes_client import MesClient
from mes_adapter.tasks_source import MesTasksSource
from mes_adapter.requestToTaskMapper import RequestToTaskMapper


@dataclass
class MesCompositionRootInitInfo:
    tasksMapperConfigPath: str
    dependencies: dict


class CompositionRoot:
    def __init__(self):
        self.__mesClient = None
        self.__tasksSource = None
        self.__requestMapper = None

    def initialize(self, initInfo: MesCompositionRootInitInfo):
        self.__requestMapper = RequestToTaskMapper(initInfo.tasksMapperConfigPath)
        self.__tasksSource = MesTasksSource(self.__requestMapper)
        self.__mesClient = MesClient(initInfo.dependencies['mesDataSource'], self.__tasksSource)
        self.__tasksSource.setTasksQueue(initInfo.dependencies['tasksQueue'])

    def start(self):
        self.__mesClient.start()

    def shutdown(self):
        self.__mesClient.kill()

    def isConnected(self):
        return self.__mesClient.isConnected()