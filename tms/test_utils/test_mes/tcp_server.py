import threading, time, socketserver, sys
from mes_adapter.test_utils.test_data import getTestFrame


currentTask = -1


class TestTcpHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global currentTask
        oldStdOut = sys.stdout
        sys.stdout = None
        try:
            self.request.sendall(getTestFrame())
            sys.stdout = oldStdOut
        except Exception:
            sys.stdout = oldStdOut
        currentTask = -1


class TcpServer():
    def __init__(self, listener):
        super().__init__()
        self.__tasksLists = []
        self.__port = 0
        self.__interval = 1.0
        self.__killed = False
        self.__workerThread = threading.Thread(target=self.__threadMain)
        self.__workerThread.daemon = True
        self.__serverThread = threading.Thread(target=self.__serverMain)
        self.__serverThread.daemon = True
        self.__listener = listener
        self.__server = None

    def tasks(self):
        return self.__tasksLists

    def addTasks(self, tasks):
        self.__tasksLists.extend(tasks)

    def setPort(self, port):
        self.__port = port

    def port(self):
        return self.__port

    def setInterval(self, interval):
        self.__interval = interval

    def interval(self):
        return self.__interval

    def start(self):
        self.__workerThread.start()
        self.__serverThread.start()

    def kill(self):
        self.__killed = True
        if self.__server is not None:
            self.__server.shutdown()

    def __threadMain(self):
        while not self.__killed:
            global currentTask
            if len(self.__tasksLists) > 0 and currentTask == -1:
                currentTask = self.__tasksLists.pop(0)
                self.__listener.onMsg("Sending task: {}".format(currentTask))
                time.sleep(self.__interval)

    def __serverMain(self):
        host, port = 'localhost', self.__port

        with socketserver.TCPServer((host, port), TestTcpHandler) as server:
            server.serve_forever()
