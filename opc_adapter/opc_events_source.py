import threading
import time

from model.abstract_event_source import AbstractEventSource
from model.events import *


class PollingThread:
    def __init__(self, client, signalsList, callback, pollingInterval):
        self.__thread = None
        self.__client = client
        self.__signalsList = signalsList
        self.__callback = callback
        self.__stopped = False
        self.__pollingInterval = pollingInterval

    def addSignal(self, signal):
        self.__signalsList.append(signal)

    def start(self):
        self.__thread = threading.Thread(target=self.__pollingMethod)
        self.__thread.daemon = True
        self.__thread.start()

    def stop(self):
        self.__stopped = True
        self.__thread.join()
        self.__thread = None

    def __pollingMethod(self):
        while not self.__stopped:
            signalsDict = {}
            for signal in self.__signalsList:
                if len(signal) > 0:
                    signalsDict[str(signal)] = self.__client.getSignalValue(signal)
            self.__callback(signalsDict)
            time.sleep(self.__pollingInterval)


class OpcEventSource(AbstractEventSource):
    def __init__(self, opcClient, objectId, xSignal, ySignal, rotationSignal, propertiesSignalsDict, updateInterval):
        super().__init__()
        signalsList = [xSignal, ySignal, rotationSignal]
        self.__handlers = dict()
        self.__opcClient = opcClient
        self.__id = objectId
        self.__xSignalStr = str(xSignal)
        self.__ySignalStr = str(ySignal)
        self.__rotationSignalStr = str(rotationSignal)
        self.__currentSignalsState = {self.__xSignalStr: 0, self.__ySignalStr: 0, self.__rotationSignalStr: 0}
        self.__propertiesSignalsStrings = dict()
        self.__alertsSignalsStrings = dict()
        for propertyName in propertiesSignalsDict:
            signal = propertiesSignalsDict[propertyName]
            self.__propertiesSignalsStrings[propertyName] = str(signal)
            self.__currentSignalsState[str(signal)] = 0
            signalsList.append(signal)
        self.__pollingThread = PollingThread(opcClient, signalsList, self.__dataPolledCallback, updateInterval)

    def addHandler(self, handler):
        self.__handlers[id(handler)] = handler

    def removeHandler(self, handler):
        del self.__handlers[id(handler)]

    def addAlertSignal(self, alertSignalName, alertSignal):
        self.__pollingThread.addSignal(alertSignal)
        self.__alertsSignalsStrings[alertSignalName] = str(alertSignal)
        self.__currentSignalsState[str(alertSignal)] = 0

    def start(self):
        self.__pollingThread.start()

    def stop(self):
        self.__pollingThread.stop()

    def sendRegisterObjectEvent(self, type, properties, width, height, name):
        registerObjectEvent = RegisterObjectEvent(objectId=self.__id,
                                                  type=type,
                                                  properties=properties,
                                                  width=width,
                                                  height=height,
                                                  name = name)
        self.__broadcastEvent(registerObjectEvent)

    def __broadcastEvent(self, event):
        for handlerId in self.__handlers:
            self.__handlers[handlerId].onEvent(event)

    def __dataPolledCallback(self, signalsDict):
        self.__signalsDictToEvent(signalsDict)

    def __signalsDictToEvent(self, signalsDict):
        self.__processPositionSignals(signalsDict)
        self.__processPropertiesSignals(signalsDict)

    def __processPositionSignals(self, signalsDict):
        newX = None
        newY = None
        if signalsDict[self.__xSignalStr] != self.__currentSignalsState[self.__xSignalStr]:
            newX = signalsDict[self.__xSignalStr]
        if signalsDict[self.__ySignalStr] != self.__currentSignalsState[self.__ySignalStr]:
            newY = signalsDict[self.__ySignalStr]
        if newX or newY:
            self.__onPositionChanged(newX, newY)

    def __onPositionChanged(self, newX, newY):
        if newX:
            self.__currentSignalsState[self.__xSignalStr] = newX
        if newY:
            self.__currentSignalsState[self.__ySignalStr] = newY
        self.__broadcastEvent(UpdateObjectPositionEvent(objectId=self.__id,
                                                        x=self.__currentSignalsState[self.__xSignalStr],
                                                        y=self.__currentSignalsState[self.__ySignalStr]))

    def __processPropertiesSignals(self, signalsDict):
        changed = False
        for propertyName in self.__propertiesSignalsStrings:
            signalStr = self.__propertiesSignalsStrings[propertyName]
            if signalsDict[signalStr] != self.__currentSignalsState[signalStr]:
                self.__currentSignalsState[signalStr] = signalsDict[signalStr]
                changed = True
        if changed:
            self.__onPropertiesChanged()

    def __onPropertiesChanged(self):
        self.__broadcastEvent(UpdateObjectPropertiesEvent(objectId=self.__id, properties=self.__getPropertiesDict()))

    def __getPropertiesDict(self):
        res = dict()
        for propertyName in self.__propertiesSignalsStrings:
            signalStr = self.__propertiesSignalsStrings[propertyName]
            signalValue = self.__currentSignalsState[signalStr]
            res[propertyName] = signalValue
        return res