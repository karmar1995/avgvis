import time, threading
from simulation.core.tasks_executor_manager import TasksExecutorManager
from agv_adapter.agv_task_executor import AgvTaskExecutor
from agv_adapter.agv_controller_client import AgvControllerClient


class AgvTaskExecutorManager(TasksExecutorManager):
    def __init__(self, agvControllerIp, agvControllerPort):
        self.__agvTaskExecutors = dict()
        self.__ip = agvControllerIp
        self.__port = agvControllerPort
        self.__agvControllerClient = None
        self.__observers = dict()
        self.__killed = False
        self.__pollingThread = None
        self.__ensureClientRunning()
        self.__createRefreshThread()

    def tasksExecutors(self):
        return list(self.__agvTaskExecutors.values())

    def addTasksExecutorObserver(self, observer):
        self.__observers[id(observer)] = observer

    def removeTasksExecutorObserver(self, observer):
        del self.__observers[id(observer)]

    def kill(self):
        self.__killed = True

    def isClientRunning(self):
        return self.__agvControllerClient is not None and self.__agvControllerClient.connected()

    def __broadcastExecutorsChanged(self):
        for observerId in self.__observers:
            self.__observers[observerId].onTasksExecutorsChanged()

    def __createTasksExecutors(self):
        self.__agvTaskExecutors = dict()
        for agvId in self.__agvControllerClient.requestAgvsIds():
            agvStatus = self.__agvControllerClient.requestAgvStatus(agvId)
            if agvStatus.online:
                self.__agvTaskExecutors[agvId] = AgvTaskExecutor(agvId, self.__agvControllerClient)
        self.__broadcastExecutorsChanged()

    def __cleanupTasksExecutors(self):
        self.__agvTaskExecutors = dict()
        self.__broadcastExecutorsChanged()

    def __ensureClientRunning(self):
        if not self.isClientRunning():
            self.__agvControllerClient = AgvControllerClient(self.__ip, self.__port)
        if self.isClientRunning():
            self.__createTasksExecutors()
        else:
            self.__cleanupTasksExecutors()

    def __reconnect(self):
        while not self.isClientRunning():
            self.__ensureClientRunning()
            time.sleep(5)
            if self.__killed:
                break

    def __createRefreshThread(self):
        self.__pollingThread = threading.Thread(target=self.__refreshConnection)
        self.__pollingThread.daemon = True
        self.__pollingThread.start()

    def __refreshConnection(self):
        while not self.__killed:
            time.sleep(5)
            self.__reconnect()