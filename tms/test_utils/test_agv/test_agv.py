from tms.test_utils.logger import Logger
import socket, sys, time, threading, random, signal, select


def getAcknowledgementFrame(working):
    res = 0
    if working:
        res = 1
    return res.to_bytes(1, 'big')


working = False
workNumber = -1
interval = 1.0
executedTasks = 0


class AgvServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
        self.__workingThread = None

    def connect(self, host, port):
        self.socket.bind((host, port))
        self.socket.listen(1)
        self.connection, _ = self.socket.accept()

    def run(self):
        while True:
            global working, logger
            if not working:
                ready = select.select([self.connection], [], [], 0.25)
                if ready[0]:
                    received = self.connection.recv(4096)
                    logger.logLine("Received: {}".format(received))
                    print("Received: {}".format(received))
                    if len(received) > 0:
                        global workNumber
                        workNumber = int.from_bytes(received, 'big')
                        self.__createProcessingThread()
            frame = getAcknowledgementFrame(working)
            print("Sending working: {}".format(frame))
            self.connection.sendall(frame)
            time.sleep(0.5)

    def __createProcessingThread(self):
        self.__workingThread = threading.Thread(target=self.__processingThread)
        self.__workingThread.start()

    def __processingThread(self):
        global working, workNumber, interval, executedTasks, logger, tasksCountLogger
        working = True
        workTime = random.expovariate(interval)
        logger.logLine("Starting work {}, number: {} for: {}...".format(workNumber, executedTasks, workTime))
        time.sleep(workTime)
        executedTasks += 1
        tasksCountLogger.logLine("Executed tasks: {}".format(executedTasks))
        logger.logLine("\nDone")
        working = False



def onSigInt(signum, frame):
    global executedTasks, logger
    logger.logLine("SIGINT or SIGTERM handled")
    sys.exit(0)

tmp = sys.argv[1].split(':')
host, port, interval = tmp[0], int(tmp[1]), float(sys.argv[2])
s1 = signal.signal(signal.SIGINT, onSigInt)
s2 = signal.signal(signal.SIGTERM, onSigInt)

logger = Logger("test_agv_log_{}.txt".format(host).replace('.', '_'))
logger.logLine("Starting test agv on: {}:{}".format(host, port))
tasksCountLogger = Logger("agv_{}_tasks_count.txt".format(host).replace('.', '_'))
tasksCountLogger.logLine("Executed tasks: {}".format(executedTasks))

agvServer = AgvServer()
agvServer.connect(host, port)
agvServer.run()