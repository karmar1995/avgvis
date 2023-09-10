import socketserver, sys, time, threading, random


def getAcknowledgementFrame(working):
    res = 0
    if working:
        res = 1
    return res.to_bytes(1, 'big')


working = False
workNumber = -1


class TestTcpHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.__workingThread = None

    def handle(self):
        global working
        if not working:
            received = self.request.recv(4096)
            print("Received: {}".format(received))
            if len(received) > 0:
                global workNumber
                workNumber = int.from_bytes(received, 'big')
                self.__createProcessingThread()
        self.request.sendall(getAcknowledgementFrame(working))

    def __createProcessingThread(self):
        self.__workingThread = threading.Thread(target=self.__processingThread)
        self.__workingThread.start()

    def __processingThread(self):
        global working, workNumber
        working = True
        print("Starting work {}...".format(workNumber))
        for i in range(0, random.randint(5, 15)):
            time.sleep(1)
            sys.stdout.write('.')
        print("\nDone")
        working = False


host, port = 'localhost', int(sys.argv[1])

with socketserver.TCPServer((host, port), TestTcpHandler) as server:
    server.serve_forever()
