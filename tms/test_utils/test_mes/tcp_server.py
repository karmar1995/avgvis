import threading, time, socket, sys
from mes_adapter.test_utils.test_data import getTestFrame


currentTask = -2
sleeping = False


class TcpServer():
    def __init__(self, listener):
        super().__init__()
        self.__tasksLists = []
        self.__port = 0
        self.__host = 'localhost'
        self.__interval = 1.0
        self.__killed = False
        self.__workerThread = threading.Thread(target=self.__threadMain)
        self.__workerThread.daemon = True
        self.__serverThread = threading.Thread(target=self.__serverMain)
        self.__serverThread.daemon = True
        self.__listener = listener
        self.__server = None
        self.__sleepFunction = None
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connection = None

    def tasks(self):
        return self.__tasksLists

    def addTasks(self, tasks):
        self.__tasksLists.extend(tasks)

    def setPort(self, port):
        self.__port = port

    def setHost(self, host):
        self.__host = host

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
                print("Sending task: {}".format(currentTask))
                self.__listener.onMsg("Sending task: {}".format(currentTask))
                sleeping = True
                if self.__sleepFunction is None:
                    time.sleep(self.__interval)
                else:
                    time.sleep(self.__sleepFunction(self.__interval))
                sleeping = False

    def __serverMain(self):
        global currentTask, sleeping
        self.__socket.bind((self.__host, self.__port))
        self.__socket.listen(1)
        self.__connection, _ = self.__socket.accept()
        while not self.__killed:
            oldStdOut = sys.stdout
            sys.stdout = None
            try:
                if not sleeping:
                    self.__connection.sendall(getTestFrame())
                    currentTask = -1
                else:
                    self.__connection.sendall(bytes())
                sys.stdout = oldStdOut
                time.sleep(0.1)
            except Exception:
                sys.stdout = oldStdOut

