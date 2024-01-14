import socket, select


class TcpClient:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.connect()

    def readDataFromServer(self):
        if self.isConnected():
            ready = select.select([self.__socket], [], [], 0)
            if ready[0]:
                return self.__socket.recv(1024)
        return None

    def sendDataToServer(self, data):
        if self.isConnected():
            self.__socket.sendall(data)

    def connect(self):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__socket.connect((self.__host, self.__port))
        except ConnectionRefusedError:
            print("Cannot connect to: {}:{}".format(self.__host, self.__port))
            self.__socket = None

    def isConnected(self):
        return self.__socket is not None
