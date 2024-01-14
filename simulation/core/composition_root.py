from simulation.core.system_builder import SystemBuilder
from simulation.core.paths_controller import PathsController
from simulation.core.tasks_queue import TasksQueue
from simulation.core.tasks_scheduler import TasksScheduler
from simulation.core.job_executors_manager import JobExecutorsManager


class CompositionRoot:
    def __init__(self):
        self.__system = None
        self.__pathsController = None
        self.__tasksQueue = None
        self.__tasksScheduler = None
        self.__executorsManager = None

    def initialize(self, dependencies, topologyBuilder):
        systemBuilder = SystemBuilder()
        self.__tasksQueue = TasksQueue()
        topologyBuilder.build(systemBuilder)
        self.__system = systemBuilder.system()
        self.__executorsManager = JobExecutorsManager(taskExecutorsManager=dependencies['taskExecutorsManager'])
        self.__pathsController = PathsController(system=self.__system,
                                                 agentsFactory=dependencies['agentsFactory'],
                                                 simulation=dependencies['simulation'])
        self.__tasksScheduler = TasksScheduler(tasksQueue=self.__tasksQueue,
                                               pathsController=self.__pathsController,
                                               executorsManager=self.__executorsManager,
                                               traverserName='simulatedAnnealing')
        self.__executorsManager.setTasksScheduler(self.__tasksScheduler)
        self.__executorsManager.createExecutors()

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
