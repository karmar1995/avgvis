import sys, signal, csv
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


class SigIntHandler:
    def __init__(self, queueObeserver, logger):
        self.__observer = queueObeserver
        self.logger = logger

    def __call__(self, *args, **kwargs):
        tmsRoot.shutdown()
        self.logger.logLine("SIGINT or SIGTERM handled")
        self.__observer.save()
        sys.exit(0)


logger = Logger("tms_log.txt")
mesConnectionString = sys.argv[1].split(':')
mesIp, mesPort = mesConnectionString[0], int(mesConnectionString[1])

agvsConnectionsStrings = sys.argv[2].split(',')
agvsConnections = []
for agvConnectionString in agvsConnectionsStrings:
    splitted = agvConnectionString.split(':')
    agvsConnections.append((splitted[0], int(splitted[1])))

qlensObserver = CliQueueObserver('qlens.csv')
sigIntHandler = SigIntHandler(qlensObserver, logger)
s1 = signal.signal(signal.SIGINT, sigIntHandler)
s2 = signal.signal(signal.SIGTERM, sigIntHandler)
logger.logLine("Starting TMS with MES: {}:{} and AGVs: {}".format(mesIp, mesPort, agvsConnections))
initInfo = TmsInitInfo(topologyDescriptionPath=sys.argv[3], mesIp=mesIp, mesPort=mesPort, mesTasksMappingPath='unused', agvConnectionsData=agvsConnections, queueObserver=qlensObserver)
tmsRoot = CompositionRoot()
tmsRoot.initialize(tmsInitInfo=initInfo)
tmsRoot.start()
while True:
    pass