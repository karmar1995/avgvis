import threading, time
from dataclasses import dataclass
from simulation.core.composition_root import CompositionRoot as SimulationRoot
from simulation.simpy_adapter.composition_root import CompositionRoot as SimpyRoot
from mes_adapter.composition_root import CompositionRoot as MesRoot, MesCompositionRootInitInfo
from agv_adapter.composition_root import CompositionRoot as AgvRoot
from tms.topology_builder import TopologyBuilder
from tcp_utils.client_utils import TcpClient
from storage.graph_storage import GraphStorage


class QueueObserver:
    def probeQueueState(self, queue, timePoint):
        pass


@dataclass
class TmsInitInfo:
    topologyDescriptionPath: str
    mesIp: str
    mesPort: int
    mesTasksMappingPath: str
    agvConnectionsData: list
    queueObserver: QueueObserver


class QueueObservingThread:
    def __init__(self, queue, queueObserver):
        self.__working = False
        self.__thread = None
        self.__queue = queue
        self.__queueObserver = queueObserver

    def start(self):
        self.__working = True
        self.__thread = threading.Thread(target=self.__observeQueue)
        self.__thread.daemon = True
        self.__thread.start()

    def shutdown(self):
        self.__working = False
        self.__thread.join()
        self.__thread = None

    def __observeQueue(self):
        timePoint = 0
        interval = 0.2
        while self.__working:
            self.__queueObserver.probeQueueState(self.__queue, timePoint)
            time.sleep(interval)
            timePoint += interval


class CompositionRoot:
    def __init__(self, networkSenderFactory=TcpClient):
        self.__simulationRoot = SimulationRoot()
        self.__simpyRoot = SimpyRoot(1000000)
        self.__mesRoot = MesRoot()
        self.__agvRoot = AgvRoot()
        self.__networkSenderFactory = networkSenderFactory
        self.__queueObservingThread = None

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
        self.__queueObservingThread = QueueObservingThread(self.__simulationRoot.tasksScheduler().tasks(), tmsInitInfo.queueObserver)

    def start(self):
        self.__mesRoot.start()
        self.__queueObservingThread.start()

    def shutdown(self):
        self.__mesRoot.shutdown()
        self.__simulationRoot.shutdown()
        self.__queueObservingThread.shutdown()
