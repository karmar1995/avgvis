from opc_adapter.opc_object import OpcObject


class OpcFactory:
    def __init__(self, opcClientFactory, eventsHandler):
        self.__opcClientFactory = opcClientFactory
        self.__eventsHandler = eventsHandler

    def createObject(self, objectId, registerData):
        opcObject = OpcObject(objectId=objectId,
                              opcClient=self.__opcClientFactory.createOpcClient(),
                              width=registerData['width'],
                              height=registerData['height'],
                              type=registerData['type'],
                              xSignal=registerData['xSignal'],
                              ySignal=registerData['ySignal'],
                              connectionString=registerData['connectionString'],
                              updateInterval=registerData['updateInterval'],
                              eventHandler=self.__eventsHandler)
        opcObject.initialize()
        return opcObject


class CompositionRoot:
    def __init__(self, eventsHandler, opcClientFactory):
        self.__eventsHandler = eventsHandler
        self.__objectsFactory = OpcFactory(opcClientFactory=opcClientFactory, eventsHandler=self.__eventsHandler)

    def objectsFactory(self):
        return self.__objectsFactory

    def initialize(self):
        return True