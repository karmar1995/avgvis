import sys, signal, random, time
from tms.test_utils.test_mes.utils import MES_PROMPT
from tms.test_utils.test_mes.tcp_server import TcpServer
from tms.test_utils.logger import Logger


def sleepFunction(interval):
    return interval/2 + random.expovariate(interval/2)


class ServerListener:
    def __init__(self):
        self.__active = False
        self.logger = Logger('mes_log.txt')

    def onMsg(self, msg):
        if self.__active:
            self.logger.logLine(msg)

    def activate(self):
        self.__active = True

    def deactivate(self):
        self.__active = False

    def isActive(self):
        return  self.__active


class TestMes:
    def __init__(self):
        self.__serverListener = ServerListener()
        self.__server = TcpServer(self.__serverListener)
        self.__signal = signal.signal(signal.SIGINT, self.__onSigInt)
        self.__batchMode = False

    def run(self):
        while True:
            if not self.__serverListener.isActive():
                response = input(MES_PROMPT)
                splittedResponse = response.split(' ')
                cmd = splittedResponse[0]
                args = splittedResponse[1:]
                if cmd == 'set_port':
                    self.__setPort(args)
                if cmd == 'start':
                    self.__startServer(args)
                if cmd == 'show_tasks':
                    self.__showTasks(args)
                if cmd == 'add_tasks':
                    self.__addTask(args)
                if cmd == 'exit':
                    self.__exit(args)
                if cmd == 'set_interval':
                    self.__setInterval(args)
                if cmd == 'monitor':
                    self.__serverListener.activate()

    def runBatchMode(self, connectionString, interval, tasksNumber):
        self.__serverListener.logger.logLine("Running batch mode on : {} with interval: {} and tasksNumber: {}".format(connectionString, interval, tasksNumber))
        self.__batchMode = True
        self.__serverListener.activate()
        self.__server.setSleepFunction(sleepFunction)
        tmp = connectionString.split(':')
        host = tmp[0]
        self.__server.setHost(host)
        self.__server.setPort(int(tmp[1]))
        self.__server.setInterval(float(interval))
        self.__server.addTasks(list(range(0, int(tasksNumber))))
        self.__startServer(None)
        while len(self.__server.tasks()) > 0:
            time.sleep(1)


    def __exit(self, args):
        self.__server.kill()
        sys.exit(0)

    def __setPort(self, args):
        self.__server.setPort(int(args[0]))

    def __startServer(self, args):
        print("Starting server on port: {}".format(self.__server.port()))
        self.__server.start()

    def __showTasks(self, args):
        print("Tasks: {}".format(self.__server.tasks()))

    def __addTask(self, args):
        self.__server.addTasks(args)
        self.__showTasks(args)

    def __setInterval(self, args):
        self.__server.setInterval(float(args[0]))
        print("Interval: {}".format(self.__server.interval()))

    def __onSigInt(self, signum, frame):
        if self.__batchMode:
            sys.exit(2)
        if self.__serverListener.isActive():
            print("Exiting monitor mode")
            self.__serverListener.deactivate()
        else:
            print("Monitor inactive")

mes = TestMes()
if len(sys.argv) == 1:
    mes.run()
else:
    mes.runBatchMode(sys.argv[1], sys.argv[2], sys.argv[3])