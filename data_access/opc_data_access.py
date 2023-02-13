import opcua
from opc_adapter.opc_client_factory import AbstractOpcClientFactory


class OpcClientFactory(AbstractOpcClientFactory):
    def __init__(self):
        super().__init__()
        pass

    def createOpcClient(self, errorSink):
        return OpcClient(errorSink)


class OpcClient:
    def __init__(self, errorSink):
        self.__client = None
        self.__keepAlive = None
        self.__connected = False
        self.__errorSink = errorSink

    def connect(self, connectionString):
        try:
            self.__client = opcua.client.client.Client(connectionString)
            self.__client.connect()
            self.__keepAlive = opcua.client.client.KeepAlive(self.__client, 0)
            self.__keepAlive.daemon = True
            self.__keepAlive.start()
            self.__connected = True
        except OSError:
            self.__errorSink.logError("Cannot connect to OPC server: " + connectionString)

    def getSignalValue(self, signal):
        try:
            if self.__connected:
                client = self.__client
                if client is not None:
                    objectsNode = client.get_objects_node()
                    if objectsNode is not None:
                        signalNode = objectsNode.get_child(signal)
                        if signalNode:
                            return signalNode.get_value()
        except Exception as e:
            self.__errorSink.logError("GetSignalValue failed: " + str(e))
        return ""

