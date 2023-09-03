import socket, threading, time
from mes_adapter.frame_parser import FrameParser
from mes_adapter.tasks_source import MesTasksSource


class MesTcpClient:

    def __init__(self, host, port, tasksSource: MesTasksSource):
        self.__host = host
        self.__port = port
        self.__frameParser = FrameParser()
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
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.__host, self.__port))
                    data = s.recv(1024)
                    self.__tasksSource.handleRequest(self.__frameParser.onFrameReceived(data).id)
                    time.sleep(0.5)
            except ConnectionRefusedError as e:
                pass

    def start(self):
        self.__pollingThread.start()

    def kill(self):
        self.__running = False
        self.__pollingThread.join()

