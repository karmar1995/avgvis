import sys
from tms.composition_root import CompositionRoot, TmsInitInfo


mesPort = int(sys.argv[1])
agvsConnections = [('localhost', int(port)) for port in sys.argv[2].split(',')]

initInfo = TmsInitInfo(topologyDescriptionPath=sys.argv[3], mesIp='localhost', mesPort=mesPort, mesTasksMappingPath='unused', agvConnectionsData=agvsConnections)
tmsRoot = CompositionRoot()
tmsRoot.initialize(tmsInitInfo=initInfo)
tmsRoot.start()
input("Press any key to exit...\n")
tmsRoot.shutdown()