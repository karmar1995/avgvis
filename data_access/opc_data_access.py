import opcua
from opc_adapter.opc_client_factory import AbstractOpcClientFactory


class OpcClientFactory(AbstractOpcClientFactory):
    def __init__(self):
        super().__init__()
        pass

    def createOpcClient(self):
        return OpcClient()


class OpcClient:
    def __init__(self):
        self.__client = None
        self.__keepAlive = None

    def connect(self, connectionString):
        self.__client = opcua.client.client.Client(connectionString)
        self.__client.connect()
        self.__keepAlive = opcua.client.client.KeepAlive(self.__client, 0)
        self.__keepAlive.daemon = True
        self.__keepAlive.start()

    def getSignalValue(self, signal):
        return self.__client.get_objects_node().get_child(signal).get_value()

# connectionString = "opc.tcp://157.158.57.220:48040"
# signalsList = [
#     ['4:Forbot_History','4:FH_ID_6000','4:[NNS] - Natural Navigation Signals','2:X-coordinate'],
#     ['4:Forbot_History','4:FH_ID_6000','4:[NNS] - Natural Navigation Signals','2:Y-coordinate']
# ]
