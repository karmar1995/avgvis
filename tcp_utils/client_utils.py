import socket, select


class TcpClient:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__host, self.__port))

    def readDataFromServer(self):
        ready = select.select([self.__socket], [], [], 0)
        if ready[0]:
            return self.__socket.recv(1024)

        no_response_mark = 200
        return no_response_mark.to_bytes(1, 'big')

    def sendDataToServer(self, data):
        self.__socket.sendall(data)
