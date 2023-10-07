import socket, select


class TcpClient:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    def readDataFromServer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.__host, self.__port))
            s.setblocking(False)
            ready = select.select([s], [], [], 0.25)
            if ready[0]:
                return s.recv(1024)
            no_response_mark = 200
            return no_response_mark.to_bytes(1, 'big')

    def sendDataToServer(self, data):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.__host, self.__port))
            return s.sendall(data)
