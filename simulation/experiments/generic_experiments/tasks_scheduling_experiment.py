import copy, time
from simulation.core.composition_root import CompositionRoot as CoreRoot
from simulation.simpy_adapter.composition_root import CompositionRoot as SimpyRoot


class RandomTasksScheduling:

    def __init__(self, tasksQueue, executorsNumber, iterations, builder):
        self.__coreRoot = CoreRoot()
        self.__simpyRoot = SimpyRoot(1000000)
        self.__executorsNumber = executorsNumber
        self.__tasksQueue = tasksQueue
        self.__iterations = iterations
        self.__testGraphBuilder = builder.setEnvironment(self.__simpyRoot.simulation.env)

    def run(self, statisticsCollector):
        dependencies = {'agentsFactory': self.__simpyRoot.simpyAgentsFactory, 'simulation': self.__simpyRoot.simulation}
        initInfo = {'executorsNumber': self.__executorsNumber}
        self.__coreRoot.initialize(dependencies, self.__testGraphBuilder, initInfo)
        self.__coreRoot.tasksQueue().batchEnqueue(copy.deepcopy(self.__tasksQueue))
        t1 = time.time()
        pathsPerJobId = self.__coreRoot.tasksScheduler().coordinateJobs(self.__iterations)
        t2 = time.time()
        elapsedTime = t2-t1
        statisticsCollector.collect('time', elapsedTime)
        for jobId in pathsPerJobId:
            path = pathsPerJobId[jobId]
            statisticsCollector.collect('cost', path.cost)
            statisticsCollector.collect('collisions', path.collisions)

