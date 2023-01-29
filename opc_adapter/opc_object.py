from opc_adapter.opc_events_source import OpcEventSource


class OpcObject:

    def __init__(self, opcClient, objectId, width, height, type, xSignal, ySignal, connectionString, updateInterval, eventHandler):
        self.__opcClient = opcClient
        self.__opcEventSource = OpcEventSource(opcClient, objectId, xSignal, ySignal, updateInterval)
        self.__width = width
        self.__height = height
        self.__type = type
        self.__xSignal = xSignal
        self.__ySignal = ySignal
        self.__connectionString = connectionString
        self.__eventHandler = eventHandler

    def initialize(self):
        self.__opcClient.connect(self.__connectionString)
        self.__opcEventSource.addHandler(self.__eventHandler)
        self.__opcEventSource.start()

    def shutdown(self):
        self.__opcEventSource.stop()
        self.__opcEventSource.removeHandler(self.__eventHandler)

    def registerObject(self):
        self.__opcEventSource.sendRegisterObjectEvent(type=self.__type,
                                                      properties={'battery':'100%'},
                                                      height=self.__height,
                                                      width=self.__width)
