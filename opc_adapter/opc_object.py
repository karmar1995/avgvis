from opc_adapter.opc_events_source import OpcEventSource


class OpcObject:

    def __init__(self, opcClient, objectId, name, width, height, type, xSignal, ySignal, rotationSignal, propertiesSignals, alertsSignals, connectionString, updateInterval, eventHandler, errorSink):
        self.__name = name
        self.__objectId = objectId
        self.__opcClient = opcClient
        self.__opcEventSource = OpcEventSource(opcClient, objectId, xSignal, ySignal, rotationSignal, propertiesSignals, updateInterval, errorSink, connectionString)
        self.__width = width
        self.__height = height
        self.__type = type
        self.__eventHandler = eventHandler
        self.__alertsSignalsRoots = alertsSignals

    def initialize(self):
        self.__initializeAlerts()
        self.__opcEventSource.addHandler(self.__eventHandler)
        self.__opcEventSource.start()

    def shutdown(self):
        self.__opcEventSource.stop()
        self.__opcEventSource.removeHandler(self.__eventHandler)

    def registerObject(self):
        self.__opcEventSource.sendRegisterObjectEvent(type=self.__type,
                                                      properties={},
                                                      height=self.__height,
                                                      width=self.__width,
                                                      name=self.__name)

    def __initializeAlerts(self):
        for alertRoot in self.__alertsSignalsRoots:
            signals = self.__getAlertsSignalsForRoot(alertRoot)
            for signalName in signals:
                self.__opcEventSource.addAlertSignal(signalName, signals[signalName])

    def __getAlertsSignalsForRoot(self, alertRoot):
        return self.__opcClient.getChildSignals(self.__alertsSignalsRoots[alertRoot])
