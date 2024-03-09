import random
import socket, sys, time, signal, select, json, threading
from tms.test_utils.logger import Logger


FAILURE_PROBABILITY = 0.1
EMERGENCY_PROBABILITY = 0.0


class FakeAgv:
    def __init__(self, agvId, online = True, faulty = False):
        self.agvId = agvId
        self.online = online
        self.location = "-1"
        self.__workingThread = None
        self.__headingToLocation = ""
        self.__taskId = -1
        self.faulty = faulty
        self.dead = False

    def goToPoint(self, newLocation, taskId):
        self.__headingToLocation = newLocation
        self.__taskId = taskId
        self.__workingThread = threading.Thread(target=self.__processingThread)
        self.__workingThread.start()

    def __processingThread(self):
        print("AGV: {} heading to: {}, task id: {}".format(self.agvId, self.__headingToLocation, self.__taskId))
        time.sleep(random.gauss(10))
        self.location = self.__headingToLocation
        if self.faulty:
            if random.random() < FAILURE_PROBABILITY:
                self.online = False
                print("Faulty AGV going offline")
                time.sleep(random.gauss(10))
                self.online = True
                print("Faulty AGV going online")
            else:
                if random.random() < EMERGENCY_PROBABILITY:
                    self.online = False
                    self.dead = True
                    print("Faulty AGV going dead")
                    time.sleep(random.gauss(10))
                    self.dead = False
                    self.online = True
                    print("Faulty AGV going dead")

        self.__workingThread = None

    def busy(self):
        return self.__workingThread is not None

    def status(self):
        return {'agvId': self.agvId, 'online': self.online, 'location': self.location}


class AgvControllerServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None
        self.__workingThread = None
        self.agvs = {}
        self.addFakeAgv('agv1', online=True, faulty=True)
        self.addFakeAgv('agv2', online=True, faulty=True)
        self.addFakeAgv('agv3', online=True, faulty=True)
        self.addFakeAgv('agv4', online=False)

    def connect(self, host, port):
        self.socket.bind((host, port))
        self.socket.listen(1)
        self.connection, _ = self.socket.accept()

    def run(self):
        while True:
            ready = select.select([self.connection], [], [], 0)
            if ready[0]:
                received = self.connection.recv(4096)
                logger.logLine("Received: {}".format(received))
                if len(received) > 0:
                    tmsRequest = self.parseTmsRequest(received)
                    response = self.processTmsRequest(tmsRequest)
                    time.sleep(random.random()*3)
                    self.connection.sendall(response)
                    time.sleep(1)

    def processTmsRequest(self, request):
        print("processing request: {}".format(request))
        response = None
        if request['id'] == "GetAgvsIds":
            agvs = []
            for agvId in self.agvs:
                if not self.agvs[agvId].dead:
                    agvs.append(agvId)
            response = { 'agvs': agvs }
        if request['id'] == "GetAgvStatus":
            response = self.agvs[request['agv_id']].status()
        if request['id'] == "GoToPoints":
            self.agvs[request['agv_id']].goToPoint(request['points'][-1], request['task_id'])
            response = { 'accepted': True }
        if request['id'] == "GoToPoint":
            self.agvs[request['agv_id']].goToPoint(request['point'], request['task_id'])
            response = {'accepted': True}
        return json.dumps(response).encode('ASCII')

    def parseTmsRequest(self, receivedBytes):
        request = receivedBytes.decode()
        print("Processing request: {}".format(request))
        return json.loads(request)

    def addFakeAgv(self, agvId, online = True, faulty = False):
        self.agvs[agvId] = FakeAgv(agvId, online, faulty)

def onSigInt(signum, frame):
    global executedTasks, logger
    logger.logLine("SIGINT or SIGTERM handled")
    sys.exit(0)

tmp = sys.argv[1].split(':')
host, port = tmp[0], int(tmp[1])
s1 = signal.signal(signal.SIGINT, onSigInt)
s2 = signal.signal(signal.SIGTERM, onSigInt)

logger = Logger("test_agv_log_{}.txt".format(host).replace('.', '_'))
logger.logLine("Starting test agv on: {}:{}".format(host, port))

agvServer = AgvControllerServer()
agvServer.connect(host, port)
agvServer.run()