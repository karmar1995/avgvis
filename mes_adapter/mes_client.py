import threading, time
from mes_adapter.frame_parser import MesFrameParser
from mes_adapter.tasks_source import MesTasksSource


class MesClient:

    def __init__(self, mesDataSource, tasksSource: MesTasksSource):
        self.__mesDataSource = mesDataSource
        self.__frameParser = MesFrameParser()
        self.__pollingThread = None
        self.__running = True
        self.__tasksSource = tasksSource
        self.__createThread()

    def __createThread(self):
        self.__pollingThread = threading.Thread(target=self.__pollMes)
        self.__pollingThread.daemon = True

    def __pollMes(self):
        while self.__running:
            try:
                while not self.isConnected():
                    self.__mesDataSource.connect()
                    time.sleep(5)
                    if not self.__running: # TMS killed in the meantime
                        break
                self.__mesDataSource.sendDataToServer(bytes("OK",encoding='ASCII'))
                data = self.__mesDataSource.readDataFromServer()
                if data is not None:
                    frame = self.__frameParser.onFrameReceived(data)
                    self.__tasksSource.handleRequest(frame.productionOrderId)
                    confirmation = bytes(str(frame.productionOrderId),encoding='ASCII')
                    self.__mesDataSource.sendDataToServer(confirmation)
                time.sleep(1)
            except ConnectionRefusedError as e:
                pass

    def start(self):
        self.__pollingThread.start()

    def kill(self):
        self.__running = False
        self.__pollingThread.join()

    def isConnected(self):
        return self.__mesDataSource.isConnected()