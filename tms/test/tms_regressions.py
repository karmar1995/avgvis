import unittest, copy, time
from tms.composition_root import CompositionRoot as TmsRoot
from tms.composition_root import TmsInitInfo
from tms.test.fake_tcp_client import FakeTcpClient, FakeTcpClientsManager

mesIp = '10.10.0.0'
initInfoPrototype = TmsInitInfo(topologyDescriptionPath='testGraph.json',
                                mesIp=mesIp,
                                mesPort=8181,
                                mesTasksMappingPath='unused',
                                agvConnectionsData=[
                                    ('10.0.0.1', 80),
                                    ('10.0.0.2', 80),
                                    ('10.0.0.3', 80)
                                ])


class TasksSchedulingTests(unittest.TestCase):

    def setUp(self) -> None:
        self.fakeTcpClientsManager = FakeTcpClientsManager()
        self.__tmsRoot = TmsRoot(self.fakeTcpClientsManager)
        self.initInfo = copy.deepcopy(initInfoPrototype)

    def test_initializesCorrectly(self):
        self.__tmsRoot.initialize(self.initInfo)
        self.assertEqual(4, len(self.fakeTcpClientsManager.hosts))

    def test_whenMesSendsFrameTheTasksAreDistributedToAgv(self):
        self.__tmsRoot.initialize(self.initInfo)
        self.assertEqual(4, len(self.fakeTcpClientsManager.hosts))

        self.fakeTcpClientsManager.hosts[mesIp].setPacketsToRead(1)
        self.__tmsRoot.start()
        time.sleep(1)
        self.__tmsRoot.shutdown()

        self.assertEqual(0, len(self.fakeTcpClientsManager.hosts['10.0.0.1'].sentData))
        self.assertEqual(0, len(self.fakeTcpClientsManager.hosts['10.0.0.2'].sentData))
        self.assertEqual(2, len(self.fakeTcpClientsManager.hosts['10.0.0.3'].sentData))
        self.assertEqual('0', self.fakeTcpClientsManager.hosts['10.0.0.3'].sentData[0])
        self.assertEqual('1', self.fakeTcpClientsManager.hosts['10.0.0.3'].sentData[1])

