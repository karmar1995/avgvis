class TaskExecutor:

    def execute(self, task):
        raise NotImplementedError()

    def getId(self):
        raise NotImplementedError()

    def getLocation(self):
        raise NotImplementedError()

    def isOnline(self):
        raise NotImplementedError()
