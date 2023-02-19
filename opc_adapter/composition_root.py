from opc_adapter.opc_object import OpcObject


class OpcFactory:
    def __init__(self, opcClientFactory, eventsHandler, errorSink):
        self.__opcClientFactory = opcClientFactory
        self.__eventsHandler = eventsHandler
        self.__errorSink = errorSink

    def createObject(self, objectId, registerData, errorSink):
        opcObject = OpcObject(objectId=objectId,
                              name = registerData['name'],
                              opcClient=self.__opcClientFactory.createOpcClient(errorSink),
                              width=registerData['width'],
                              height=registerData['height'],
                              type=registerData['type'],
                              xSignal=registerData['xSignal'],
                              ySignal=registerData['ySignal'],
                              rotationSignal=registerData['rotationSignal'],
                              connectionString=registerData['connectionString'],
                              updateInterval=registerData['updateInterval'],
                              propertiesSignals=registerData['properties'],
                              alertsSignals=registerData['alerts'],
                              eventHandler=self.__eventsHandler)
        try:
            opcObject.initialize()
            return opcObject
        except Exception as e:
            self.__errorSink.logError(str(e))
        except:
            self.__errorSink.logError("Unknown error during object creation")


class CompositionRoot:
    def __init__(self, eventsHandler, opcClientFactory, opcFakesFactory, errorSink):
        self.__eventsHandler = eventsHandler
        self.__objectsFactory = OpcFactory(opcClientFactory=opcClientFactory,
                                           eventsHandler=self.__eventsHandler,
                                           errorSink=errorSink)
        self.__fakesFactory = OpcFactory(opcClientFactory=opcFakesFactory,
                                         eventsHandler=self.__eventsHandler,
                                         errorSink=errorSink)

    def objectsFactory(self):
        return self.__objectsFactory

    def fakesFactory(self):
        return self.__fakesFactory

    def initialize(self):
        return True