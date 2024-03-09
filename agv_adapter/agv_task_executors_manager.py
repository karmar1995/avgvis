import time, threading, inspect
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
        self.__refreshCounter = 0

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

    def onExecutorChanged(self):
        self.__broadcastExecutorsChanged()

    def __broadcastExecutorsChanged(self):
        for observerId in self.__observers:
            self.__observers[observerId].onTasksExecutorsChanged()

    def refreshTasksExecutors(self):
        if self.__agvControllerClient.busy() or not self.isClientRunning():
            return
        if self.__refreshCounter > 2:
            self.__refreshCounter = 0
            newAvailableAgvIds = self.__agvControllerClient.requestAgvsIds()
            if newAvailableAgvIds is not None and newAvailableAgvIds != self.__availableAgvs():
                self.__unregisterUnavailableExecutors(newAvailableAgvIds)
                self.__registerNewAvailableExecutors(newAvailableAgvIds)
                self.__broadcastExecutorsChanged()
            self.__refreshExecutors()
        else:
            self.__refreshCounter += 1

    def __unregisterUnavailableExecutors(self, availableAgvIds):
        executorsToCleanup = []
        for agvId in self.__agvTaskExecutors:
            if agvId not in availableAgvIds:
                executorsToCleanup.append(agvId)

        for agvId in executorsToCleanup:
            del self.__agvTaskExecutors[agvId]

    def __registerNewAvailableExecutors(self, availableAgvIds):
        for agvId in availableAgvIds:
            agvStatus = self.__agvControllerClient.requestAgvStatus(agvId)
            if agvStatus is None:
                raise Exception("No response!")

            if agvId not in self.__agvTaskExecutors:
                self.__agvTaskExecutors[agvId] = AgvTaskExecutor(agvId, self.__agvControllerClient, agvStatus, self)

    def __refreshExecutors(self):
        for agvId in self.__agvTaskExecutors:
            self.__agvTaskExecutors[agvId].updateStatus(self.__agvControllerClient.requestAgvStatus(agvId))

    def __availableAgvs(self):
        return list(self.__agvTaskExecutors.keys())

    def __cleanupTasksExecutors(self):
        if len(self.__availableAgvs()) > 0:
            self.__agvTaskExecutors = dict()
            self.__broadcastExecutorsChanged()

    def __ensureClientRunning(self):
        if not self.isClientRunning():
            self.__agvControllerClient = AgvControllerClient(self.__ip, self.__port)
        if self.isClientRunning():
            self.refreshTasksExecutors()
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