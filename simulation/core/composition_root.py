from simulation.core.system_builder import SystemBuilder
from simulation.core.paths_controller import PathsController
from simulation.core.tasks_queue import TasksQueue
from simulation.core.tasks_scheduler import TasksScheduler


class CompositionRoot:
    def __init__(self):
        self.__system = None
        self.__pathsController = None
        self.__tasksQueue = None
        self.__tasksScheduler = None

    def initialize(self, dependencies, topologyBuilder, initInfo):
        systemBuilder = SystemBuilder()
        self.__tasksQueue = TasksQueue()
        topologyBuilder.build(systemBuilder)
        self.__system = systemBuilder.system()
        self.__pathsController = PathsController(system=self.__system,
                                                 agentsFactory=dependencies['agentsFactory'],
                                                 simulation=dependencies['simulation'])
        self.__tasksScheduler = TasksScheduler(tasksQueue=self.__tasksQueue,
                                               pathsController=self.__pathsController,
                                               executorsNumber=initInfo['executorsNumber'])

    def pathsController(self):
        return self.__pathsController

    def tasksQueue(self):
        return self.__tasksQueue

    def tasksScheduler(self):
        return self.__tasksScheduler

    def system(self):
        return self.__system

