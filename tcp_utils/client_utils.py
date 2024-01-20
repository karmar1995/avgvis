import socket, select


class TcpClient:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__socket = None
        self.__connectionObservers = dict()
        self.connect()

    def readDataFromServer(self):
        try:
            if self.isConnected():
                ready = select.select([self.__socket], [], [], 0)
                if ready[0]:
                    return self.__socket.recv(1024)
        except BrokenPipeError:
            self.disconnect()
        except ConnectionResetError:
            self.disconnect()
        except ConnectionAbortedError:
            self.disconnect()
        return None

    def sendDataToServer(self, data):
        if self.isConnected():
            try:
                self.__socket.sendall(data)
            except BrokenPipeError:
                self.disconnect()
            except ConnectionResetError:
                self.disconnect()
            except ConnectionAbortedError:
                self.disconnect()

    def connect(self):
        try:
            print("Connecting to {}:{}".format(self.__host, self.__port))
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self.__host, self.__port))
        except ConnectionRefusedError:
            print("Cannot connect to: {}:{}".format(self.__host, self.__port))
            self.__socket = None

    def isConnected(self):
        return self.__socket is not None

    def addConnectionObserver(self, observer):
        self.__connectionObservers[id(observer)] = observer

    def removeConnectionObserver(self, observer):
        del self.__connectionObservers[id(observer)]

    def disconnect(self):
        self.__socket = None
        self.__broadcastDisconnected()

    def __broadcastDisconnected(self):
        for observerId in self.__connectionObservers:
            self.__connectionObservers[observerId].onConnectionLost()
