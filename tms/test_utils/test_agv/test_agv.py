from tms.test_utils.logger import Logger
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
        global working, logger
        if not working:
            received = self.request.recv(4096)
            logger.logLine("Received: {}".format(received))
            if len(received) > 0:
                global workNumber
                workNumber = int.from_bytes(received, 'big')
                self.__createProcessingThread()
        self.request.sendall(getAcknowledgementFrame(working))

    def __createProcessingThread(self):
        self.__workingThread = threading.Thread(target=self.__processingThread)
        self.__workingThread.start()

    def __processingThread(self):
        global working, workNumber, interval, executedTasks, logger
        working = True
        workTime = random.expovariate(interval)
        logger.logLine("Starting work {}, number: {} for: {}...".format(workNumber, executedTasks, workTime))
        time.sleep(workTime)
        executedTasks += 1
        logger.logLine("\nDone")
        working = False


def onSigInt(signum, frame):
    global executedTasks, logger
    logger.logLine("SIGINT handled")
    with open("agv_log.txt", 'w') as f:
        f.write("Executed tasks: {}".format(executedTasks))
    sys.exit(0)

tmp = sys.argv[1].split(':')
host, port, interval = tmp[0], int(tmp[1]), float(sys.argv[2])
s = signal.signal(signal.SIGINT, onSigInt)

logger = Logger("test_agv_log.txt")
logger.logLine("Starting test agv on: {}:{}".format(host, port))

with socketserver.TCPServer((host, port), TestTcpHandler) as server:
    server.serve_forever()
