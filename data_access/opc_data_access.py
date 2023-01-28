import threading

import opcua
from threading import Thread
import time
import sys


class PollingThread:
    def __init__(self, client, signalsList, callback, event):
        self.__thread = None
        self.__client = client
        self.__signalsList = signalsList
        self.__callback = callback
        self.__stopped = False
        self.__event = event

    def start(self):
        self.__thread = Thread(target=self.__pollingMethod)
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
                signalsDict[str(signal)] = self.__client.get_objects_node().get_child(signal).get_value()
            self.__callback(signalsDict)
            self.__event.set()
            time.sleep(1)


class OpcDataAccess:
    def __init__(self):
        self.__event = threading.Event()
        self.__client = opcua.client.client.Client("opc.tcp://157.158.57.220:48040")
        self.__x_coordinate_path = ['4:Forbot_History','4:FH_ID_6000','4:[NNS] - Natural Navigation Signals','2:X-coordinate']
        self.__y_coordinate_path = ['4:Forbot_History','4:FH_ID_6000','4:[NNS] - Natural Navigation Signals','2:Y-coordinate']
        self.__keepAlive = opcua.client.client.KeepAlive(self.__client, 0)
        self.__keepAlive.daemon = True
        self.__client.connect()
        self.__keepAlive.start()
        self.__pollingThread = PollingThread(self.__client, [self.__x_coordinate_path, self.__y_coordinate_path], self.__dataPolledCallback, self.__event)
        self.__signalsDict = None

    def __dataPolledCallback(self, signalsDict):
        self.__signalsDict = signalsDict

    def start(self):
        self.__pollingThread.start()
        while True:
            self.__event.wait()
            self.__event.clear()
            for signal in self.__signalsDict:
                print(signal + ": " + str(self.__signalsDict[signal]))

    def stop(self):
        self.__pollingThread.stop()


opcDataAccess = OpcDataAccess()
try:
    opcDataAccess.start()
except KeyboardInterrupt:
    opcDataAccess.stop()
