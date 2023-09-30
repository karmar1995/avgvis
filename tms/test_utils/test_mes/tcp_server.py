import threading, time, socketserver, sys
from mes_adapter.test_utils.test_data import getTestFrame


currentTask = -2
sleeping = False


class TestTcpHandler(socketserver.BaseRequestHandler):

    def handle(self):
        global currentTask, sleeping
        oldStdOut = sys.stdout
        sys.stdout = None
        try:
            if not sleeping:
                self.request.sendall(getTestFrame())
                currentTask = -1
            else:
                self.request.sendall(bytes())
            sys.stdout = oldStdOut
        except Exception:
            sys.stdout = oldStdOut


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
        self.__sleepFunction = None

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

    def setSleepFunction(self, function):
        self.__sleepFunction = function

    def __threadMain(self):
        while not self.__killed:
            global currentTask, sleeping
            if len(self.__tasksLists) > 0 and currentTask == -1:
                currentTask = self.__tasksLists.pop(0)
                self.__listener.onMsg("Sending task: {}".format(currentTask))
                sleeping = True
                if self.__sleepFunction is None:
                    time.sleep(self.__interval)
                else:
                    time.sleep(self.__sleepFunction(self.__interval))
                sleeping = False

    def __serverMain(self):
        host, port = 'localhost', self.__port

        with socketserver.TCPServer((host, port), TestTcpHandler) as server:
            server.serve_forever()
