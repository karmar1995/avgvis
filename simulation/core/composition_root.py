from dataclasses import dataclass
from simulation.core.system_builder import SystemBuilder
from simulation.core.paths_controller import PathsController
from simulation.core.tasks_queue import TasksQueue
from simulation.core.tasks_scheduler import TasksScheduler
from simulation.core.job_executors_manager import JobExecutorsManager
from simulation.core.simulated_annealing_traverser2 import SimulatedAnnealingTraverser
from simulation.core.genetic_algorithm_traverser2 import GeneticAlgorithmTraverser
from simulation.core.queue_optimizer import QueueOptimizer


TRAVERSERS = {
    'simulatedAnnealing': SimulatedAnnealingTraverser,
    'geneticAlgorithm': GeneticAlgorithmTraverser
}


@dataclass
class SimulationInitInfo:
    traverserName: str


class CompositionRoot:
    def __init__(self):
        self.__system = None
        self.__pathsController = None
        self.__tasksQueue = None
        self.__tasksScheduler = None
        self.__executorsManager = None
        self.__queueOptimizer = None

    def initialize(self, dependencies, topologyBuilder, simulationInitInfo):
        systemBuilder = SystemBuilder()
        self.__tasksQueue = TasksQueue()
        topologyBuilder.build(systemBuilder)
        self.__system = systemBuilder.system()
        self.__executorsManager = JobExecutorsManager(taskExecutorsManager=dependencies['taskExecutorsManager'])
        self.__executorsManager.createExecutors()
        self.__pathsController = PathsController(system=self.__system,
                                                 agentsFactory=dependencies['agentsFactory'],
                                                 simulation=dependencies['simulation'])
        self.__queueOptimizer = QueueOptimizer(system=self.__system,
                                               agentsFactory=dependencies['agentsFactory'],
                                               simulation=dependencies['simulation'],
                                               traverserFactory=TRAVERSERS[simulationInitInfo.traverserName],
                                               queue=self.__tasksQueue,
                                               agentsNumber=self.__executorsManager.executorsNumber()
                                               )
        self.__tasksScheduler = TasksScheduler(executorsManager=self.__executorsManager,
                                               queueOptimizer=self.__queueOptimizer)

    def start(self):
        self.__tasksScheduler.start()

    def shutdown(self):
        self.__tasksScheduler.shutdown()

    def pathsController(self):
        return self.__pathsController

    def tasksQueue(self):
        return self.__tasksQueue

    def tasksScheduler(self):
        return self.__tasksScheduler

    def executorsManager(self):
        return self.__executorsManager

    def system(self):
        return self.__system
