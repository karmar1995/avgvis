from simulation.core.tasks_source import TasksSource, TasksQueue


class MesTasksSource(TasksSource):

    def __init__(self, requestMapper):
        self.__tasksQueue = None
        self.__requestMapper = requestMapper

    def setTasksQueue(self, queue: TasksQueue):
        self.__tasksQueue = queue

    def handleRequest(self, requestId):
        task = self.__requestMapper.getTaskFromId(requestId)
        if task is not None:
            if self.__tasksQueue is not None:
                self.__tasksQueue.enqueue(task)
        else:
            print("Unkown request ID: " + str(requestId))