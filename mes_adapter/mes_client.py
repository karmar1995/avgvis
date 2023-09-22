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
                self.__tasksSource.handleRequest(self.__frameParser.onFrameReceived(self.__mesDataSource.readDataFromServer()).id)
                time.sleep(0.5)
            except ConnectionRefusedError as e:
                pass

    def start(self):
        self.__pollingThread.start()

    def kill(self):
        self.__running = False
        self.__pollingThread.join()

