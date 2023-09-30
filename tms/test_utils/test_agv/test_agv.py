import socketserver, sys, time, threading, random, signal


def getAcknowledgementFrame(working):
    res = 0
    if working:
        res = 1
    return res.to_bytes(1, 'big')


working = False
workNumber = -1
interval = 1.0
executedTasks = 0

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
        global working, workNumber, interval, executedTasks
        working = True
        workTime = random.expovariate(interval)
        print("Starting work {}, number: {} for: {}...".format(workNumber, executedTasks, workTime))
        time.sleep(workTime)
        executedTasks += 1
        print("\nDone")
        working = False


def onSigInt(signum, frame):
    global executedTasks
    with open("agv_log.txt", 'w') as f:
        f.write("Executed tasks: {}".format(executedTasks))
    sys.exit(0)


host, port, interval = 'localhost', int(sys.argv[1]), float(sys.argv[2])
s = signal.signal(signal.SIGINT, onSigInt)

print("Starting test agv on: {}:{}".format(host, port))

with socketserver.TCPServer((host, port), TestTcpHandler) as server:
    server.serve_forever()
