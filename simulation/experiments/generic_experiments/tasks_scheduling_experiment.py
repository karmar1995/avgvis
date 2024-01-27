import copy, time
from simulation.core.composition_root import CompositionRoot as CoreRoot
from simulation.core.composition_root import SimulationInitInfo
from simulation.simpy_adapter.composition_root import CompositionRoot as SimpyRoot
from simulation.core.tasks_executor_manager import TasksExecutorManager
from simulation.core.task_executor import TaskExecutor


class FakeTaskExecutor(TaskExecutor):
    def __init__(self, executorId):
        self.__executorId = executorId

    def execute(self, jobId):
        pass

    def getId(self):
        return self.__executorId


class FakeTasksExecutorsManager(TasksExecutorManager):
    def __init__(self, executorsNumber):
        self.__executorsNumber = executorsNumber
        self.__executors = []
        for i in range(self.__executorsNumber):
            self.__executors.append(FakeTaskExecutor(i))

    def tasksExecutors(self):
        return self.__executors

    def addTasksExecutorObserver(self, observer):
        pass

    def removeTasksExecutorObserver(self, observer):
        pass


class RandomTasksScheduling:

    def __init__(self, tasksQueue, executorsNumber, iterations, builder, traverserName):
        self.__coreRoot = CoreRoot()
        self.__simpyRoot = SimpyRoot(10000000)
        self.__tasksQueue = tasksQueue
        self.__iterations = iterations
        self.__testGraphBuilder = builder.setEnvironment(self.__simpyRoot.simulation.env)
        self.__traverserName = traverserName
        self.__executorsManager = FakeTasksExecutorsManager(executorsNumber)

    def run(self, statisticsCollector):
        dependencies = {'agentsFactory': self.__simpyRoot.simpyAgentsFactory,
                        'simulation': self.__simpyRoot.simulation,
                        'taskExecutorsManager': self.__executorsManager}
        simulationInitInfo = SimulationInitInfo(traverserName=self.__traverserName)
        self.__coreRoot.initialize(dependencies, self.__testGraphBuilder, simulationInitInfo)
        self.__coreRoot.tasksQueue().batchEnqueue(copy.deepcopy(self.__tasksQueue))
        t1 = time.time()
        queueView = self.__coreRoot.tasksScheduler().optimizeQueue(self.__iterations)
        t2 = time.time()
        elapsedTime = t2-t1
        statisticsCollector.collect('time', elapsedTime)
        statisticsCollector.collect('cost', queueView.cost)
#        statisticsCollector.collect('collisions', path.collisions)
#        statisticsCollector.collect('timeInQueue', path.timeInQueue)
#        statisticsCollector.collect('timeInPenalty', path.timeInPenalty)
#        statisticsCollector.collect('timeInTransition', path.timeInTransition)

#        for i in range(0, self.__coreRoot.system().nodesCount()):
#            tmp = self.__coreRoot.system().node(i).queueLengthHistory()
#            statisticsCollector.collect('queueLength', sum(tmp) / len(tmp))
