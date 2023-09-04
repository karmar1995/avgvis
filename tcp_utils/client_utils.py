import socket


class TcpClient:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    def readDataFromServer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.__host, self.__port))
            return s.recv(1024)

    def sendDataToServer(self, data):
        raise Exception("Not implemented!")