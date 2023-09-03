from dataclasses import dataclass
from mes_adapter.tcp_client import MesTcpClient
from mes_adapter.tasks_source import MesTasksSource
from mes_adapter.requestToTaskMapper import RequestToTaskMapper


@dataclass
class MesCompositionRootInitInfo:
    tcpServerIp: str
    tcpServerPort: int
    tasksMapperConfigPath: str
    dependencies: dict


class CompositionRoot:
    def __init__(self):
        self.__tcpClient = None
        self.__tasksSource = None
        self.__requestMapper = None

    def initialize(self, initInfo : MesCompositionRootInitInfo):
        self.__requestMapper = RequestToTaskMapper(initInfo.tasksMapperConfigPath)
        self.__tasksSource = MesTasksSource(self.__requestMapper)
        self.__tcpClient = MesTcpClient(initInfo.tcpServerIp, initInfo.tcpServerPort, self.__tasksSource)
        #TODO: inject tasks scheduler
#        self.__tasksSource.setTasksQueue(initInfo.dependencies['tasksScheduler'])

    def start(self):
        self.__tcpClient.start()

    def shutdown(self):
        self.__tcpClient.kill()


root = CompositionRoot()
root.initialize(MesCompositionRootInitInfo('localhost', 1234, 'unused', {}))
root.start()
while True:
    pass