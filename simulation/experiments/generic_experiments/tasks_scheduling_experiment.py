import copy, time
from simulation.core.composition_root import CompositionRoot as CoreRoot
from simulation.simpy_adapter.composition_root import CompositionRoot as SimpyRoot


class FakeTaskExecutor:
    def execute(self, jobId):
        pass


class RandomTasksScheduling:

    def __init__(self, tasksQueue, executorsNumber, iterations, builder, traverserName):
        self.__coreRoot = CoreRoot()
        self.__simpyRoot = SimpyRoot(10000000)
        self.__executorsNumber = executorsNumber
        self.__tasksQueue = tasksQueue
        self.__iterations = iterations
        self.__testGraphBuilder = builder.setEnvironment(self.__simpyRoot.simulation.env)
        self.__traverserName = traverserName

    def run(self, statisticsCollector):
        dependencies = {'agentsFactory': self.__simpyRoot.simpyAgentsFactory, 'simulation': self.__simpyRoot.simulation, 'tasksExecutorsFactory': FakeTaskExecutor}
        initInfo = {'executorsNumber': self.__executorsNumber}
        self.__coreRoot.initialize(dependencies, self.__testGraphBuilder, initInfo)
        self.__coreRoot.tasksQueue().batchEnqueue(copy.deepcopy(self.__tasksQueue))
        t1 = time.time()
        pathsPerJobId = self.__coreRoot.tasksScheduler().coordinateJobs(self.__iterations, self.__traverserName)
        t2 = time.time()
        elapsedTime = t2-t1
        statisticsCollector.collect('time', elapsedTime)
        for jobId in pathsPerJobId:
            path = pathsPerJobId[jobId]
            statisticsCollector.collect('cost', path.cost)
            statisticsCollector.collect('collisions', path.collisions)
            statisticsCollector.collect('timeInQueue', path.timeInQueue)
            statisticsCollector.collect('timeInPenalty', path.timeInPenalty)
            statisticsCollector.collect('timeInTransition', path.timeInTransition)

        for i in range(0, self.__coreRoot.system().nodesCount()):
            tmp = self.__coreRoot.system().node(i).queueLengthHistory()
            statisticsCollector.collect('queueLength', sum(tmp) / len(tmp))
