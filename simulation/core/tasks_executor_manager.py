class TasksExecutorManager:

    def tasksExecutors(self):
        raise NotImplementedError()

    def addTasksExecutorObserver(self, observer):
        raise NotImplementedError()

    def removeTasksExecutorObserver(self, observer):
        raise NotImplementedError()