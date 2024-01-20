import tempfile
from flask import Flask, request, render_template, abort, send_file
from dataclasses import dataclass
from composition_root import CompositionRoot, TmsInitInfo, QueueObserver

@dataclass
class AGV:
    name: str
    tasks: list


class WebQueueObserver(QueueObserver):
    def __init__(self):
        self.agvs = []
        self.tasks = []

    def probeQueueState(self, queue, executorsViews, timePoint):
        self.tasks = []
        self.agvs = []
        for executorView in executorsViews:
            self.agvs.append(AGV(executorView.executorId(), executorView.tasksSequence()))
        for task in queue:
            self.tasks.append(task.taskNumber())


class WebTms:
    def __init__(self):
        self.__tms = None
        self.queueObserver = WebQueueObserver()
        self.tmsInitInfo = None

    def start(self, initInfo : TmsInitInfo):
        if not self.isRunning():
            self.tmsInitInfo = initInfo
            self.__tms = CompositionRoot()
            self.__tms.initialize(self.tmsInitInfo)
            self.__tms.start()

    def shutdown(self):
        self.__tms.shutdown()
        self.__tms = None

    def isRunning(self):
        return self.__tms is not None

    def mesStatus(self):
        connected = False
        if self.__tms:
            connected = self.__tms.isMesConnected()
        if connected:
            return "Connected"
        return "Disconnected"

    def agvHubStatus(self):
        if self.__tms and self.__tms.isAgvHubConnected():
            return "Connected"
        return "Disconnected"

app = Flask(__name__)
tms = WebTms()

@app.route('/')
def index():
    disabledTag = ''
    #if False:
    #    disabledTag = 'disabled'

    return render_template('index.html', runDisabledTag=disabledTag)

def getFileFromRequest(request, filename, tmpFile):
    if filename not in request.files:
        return ''
    file = request.files[filename]
    if file.filename == '':
        return ''
    tmpFileName = tmpFile.name
    file.save(tmpFileName)
    return tmpFileName


@app.route('/run', methods=['GET', 'POST'])
def run():
    mesConnectionString = ""
    agvHubConnectionString = ""
    if request.method == 'POST':
        if request.form.get('Run') == 'Run':
            if not tms.isRunning():
                with tempfile.NamedTemporaryFile() as graphFile, tempfile.NamedTemporaryFile() as mesMappingFile:
                    topologyDescriptionFile = getFileFromRequest(request, 'graphDescription', graphFile)
                    mesMappingFile = getFileFromRequest(request, 'mesMappingFile', mesMappingFile)
                    mesConnectionString = request.form.get('mesConnectionString').split(':')
                    agvHubConnectionString = request.form.get('agvHubConnectionString').split(':')
                    tmsInitInfo = TmsInitInfo(topologyDescriptionPath=topologyDescriptionFile,
                                              mesIp=mesConnectionString[0], mesPort=int(mesConnectionString[1]),
                                              agvControllerIp=agvHubConnectionString[0], agvControllerPort=int(agvHubConnectionString[1]),
                                              mesTasksMappingPath=mesMappingFile, queueObserver=tms.queueObserver)
                    tms.start(tmsInitInfo)

    if tms.tmsInitInfo is not None:
        mesConnectionString = "{}:{}".format(tms.tmsInitInfo.mesIp, tms.tmsInitInfo.mesPort)
        agvHubConnectionString = "{}:{}".format(tms.tmsInitInfo.agvControllerIp, tms.tmsInitInfo.agvControllerPort)

    return render_template('tms.html',
                           mesStatus=tms.mesStatus(),
                           agvHubStatus=tms.agvHubStatus(),
                           mesConnectionString=mesConnectionString,
                           agvHubConnectionString=agvHubConnectionString,
                           tasksQueue=tms.queueObserver.tasks,
                           agvs=tms.queueObserver.agvs)
