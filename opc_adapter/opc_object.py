from opc_adapter.opc_events_source import OpcEventSource


class OpcObject:

    def __init__(self,
                 opcClient,
                 objectId,
                 name,
                 width,
                 height,
                 type,
                 xSignal,
                 ySignal,
                 rotationSignal,
                 propertiesSignals,
                 alertsSignals,
                 connectionString,
                 updateInterval,
                 eventsHub,
                 errorSink,
                 frontLidarRange,
                 rearLidarRange):
        self.__name = name
        self.__objectId = objectId
        self.__opcClient = opcClient
        self.__opcEventSource = OpcEventSource(opcClient, objectId, xSignal, ySignal, rotationSignal, propertiesSignals, updateInterval, errorSink, connectionString)
        self.__width = width
        self.__height = height
        self.__type = type
        self.__eventsHub = eventsHub
        self.__alertsSignalsRoots = alertsSignals
        self.__eventsHub.addHandler(self)
        self.__frontLidarRange = frontLidarRange
        self. __rearLidarRange = rearLidarRange

    def initialize(self):
        self.__initializeAlerts()
        self.__opcEventSource.addHandler(self.__eventsHub)
        self.__opcEventSource.start()

    def shutdown(self):
        self.__opcEventSource.stop()
        self.__opcEventSource.removeHandler(self.__eventsHub)

    def registerObject(self):
        self.__opcEventSource.sendRegisterObjectEvent(type=self.__type,
                                                      properties={},
                                                      height=self.__height,
                                                      width=self.__width,
                                                      name=self.__name,
                                                      frontLidarRange=self.__frontLidarRange,
                                                      rearLidarRange=self.__rearLidarRange
                                                      )

    def __initializeAlerts(self):
        for alertRoot in self.__alertsSignalsRoots:
            signals = self.__getAlertsSignalsForRoot(alertRoot)
            for signalName in signals:
                self.__opcEventSource.addAlertSignal(signalName, signals[signalName], alertRoot)

    def __getAlertsSignalsForRoot(self, alertRoot):
        return self.__opcClient.getChildSignals(self.__alertsSignalsRoots[alertRoot])

    def onRegisterObject(self, event):
        pass

    def onUpdateObjectPosition(self, event):
        pass

    def onUpdateObjectRotation(self, event):
        pass

    def onUpdateObjectProperties(self, event):
        pass

    def onUpdateObjectAlerts(self, event):
        pass

    def onUnregisterObject(self, event):
        if event.objectId == self.__objectId:
            self.__opcEventSource.stop()

    def onRefreshObject(self, event):
        if event.objectId == self.__objectId:
            self.__opcEventSource.stop()
            self.__opcEventSource.start()
