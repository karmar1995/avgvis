import sys, signal, csv, time
from tms.composition_root import CompositionRoot, TmsInitInfo, QueueObserver
from tms.test_utils.logger import Logger


class CliQueueObserver(QueueObserver):
    def __init__(self, logFilename):
        self.__qlens = list()
        self.__fields = ['time', 'qlen']
        self.__filename = logFilename

    def probeQueueState(self, queue, timePoint):
        self.__qlens.append({'time': round(timePoint, 2), 'qlen': len(queue)})

    def save(self):
        with open(self.__filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.__fields)
            writer.writeheader()
            writer.writerows(self.__qlens)


class SignalHandler:
    def __init__(self):
        self.s1 = signal.signal(signal.SIGINT, self.handleExit)
        self.s2 = signal.signal(signal.SIGTERM, self.handleExit)

        self.killed = False

    def handleExit(self, *args):
        self.killed = True


logger = Logger("tms_log.txt")
mesConnectionString = sys.argv[1].split(':')
mesIp, mesPort = mesConnectionString[0], int(mesConnectionString[1])

agvsConnectionsStrings = sys.argv[2].split(',')
agvsConnections = []
for agvConnectionString in agvsConnectionsStrings:
    splitted = agvConnectionString.split(':')
    agvsConnections.append((splitted[0], int(splitted[1])))

qlensObserver = CliQueueObserver('qlens.csv')
sigIntHandler = SignalHandler()
logger.logLine("Starting TMS with MES: {}:{} and AGVs: {}".format(mesIp, mesPort, agvsConnections))
initInfo = TmsInitInfo(topologyDescriptionPath=sys.argv[3], mesIp=mesIp, mesPort=mesPort, mesTasksMappingPath='unused', agvConnectionsData=agvsConnections, queueObserver=qlensObserver)
tmsRoot = CompositionRoot()
tmsRoot.initialize(tmsInitInfo=initInfo)
tmsRoot.start()
while not sigIntHandler.killed:
    time.sleep(1)
    qlensObserver.save()

tmsRoot.shutdown()
logger.logLine("SIGINT or SIGTERM handled")
sys.exit(0)
