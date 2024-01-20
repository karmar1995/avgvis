from simulation.core.task import Task


testRequest2TaskMapping = {
    23: Task(23, 0, 1)
}


class RequestToTaskMapper:
    def __init__(self, configPath):
        #todo: read it from some file or smth
        self.__mapping = testRequest2TaskMapping

    def getTaskFromId(self, id):
        try:
            return self.__mapping[id]
        except KeyError:
            return None
