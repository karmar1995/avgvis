from dataclasses import dataclass
from simulation.core.composition_root import CompositionRoot as SimulationRoot
from simulation.simpy_adapter.composition_root import CompositionRoot as SimpyRoot
from mes_adapter.composition_root import CompositionRoot as MesRoot, MesCompositionRootInitInfo
from agv_adapter.composition_root import CompositionRoot as AgvRoot
from tms.topology_builder import TopologyBuilder
from tcp_utils.client_utils import TcpClient
from storage.graph_storage import GraphStorage


@dataclass
class TmsInitInfo:
    topologyDescriptionPath: str
    mesIp: str
    mesPort: int
    mesTasksMappingPath: str
    agvConnectionsData: list


class CompositionRoot:
    def __init__(self, networkSenderFactory=TcpClient):
        self.__simulationRoot = SimulationRoot()
        self.__simpyRoot = SimpyRoot(1000000)
        self.__mesRoot = MesRoot()
        self.__agvRoot = AgvRoot()
        self.__networkSenderFactory = networkSenderFactory

    def initialize(self, tmsInitInfo: TmsInitInfo):
        graphStorage = GraphStorage()
        graphStorage.read(tmsInitInfo.topologyDescriptionPath)
        topologyBuilder = TopologyBuilder(self.__simpyRoot.simulation.env, graphStorage)
        agvsSenders = list()
        for agvConnectionData in tmsInitInfo.agvConnectionsData:
            agvsSenders.append(self.__networkSenderFactory(agvConnectionData[0], agvConnectionData[1]))
        executorsNumber = len(agvsSenders)
        self.__agvRoot.initialize(agvsSenders)

        dependencies = {
            'agentsFactory': self.__simpyRoot.simpyAgentsFactory,
            'simulation': self.__simpyRoot.simulation,
            'tasksExecutorsFactory': self.__agvRoot.executorsFactory()
        }
        simulationInitInfo = {'executorsNumber': executorsNumber}
        self.__simulationRoot.initialize(dependencies, topologyBuilder, simulationInitInfo)
        mesInitInfo = MesCompositionRootInitInfo(tasksMapperConfigPath=tmsInitInfo.mesTasksMappingPath, dependencies={
            'mesDataSource': self.__networkSenderFactory(host=tmsInitInfo.mesIp, port=tmsInitInfo.mesPort),
            'tasksQueue': self.__simulationRoot.tasksQueue()
        })
        self.__mesRoot.initialize(mesInitInfo)


    def start(self):
        self.__mesRoot.start()

    def shutdown(self):
        self.__mesRoot.shutdown()
        self.__simulationRoot.shutdown()