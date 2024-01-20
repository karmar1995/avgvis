class Task:
    def __init__(self, taskNumber, source, destination):
        self.__taskNumber = taskNumber
        self.__source = source
        self.__destination = destination

    def source(self):
        return self.__source

    def destination(self):
        return self.__destination

    def taskNumber(self):
        return self.__taskNumber

    def __str__(self):
        return "[{}, {}]".format(self.__source, self.__destination)

