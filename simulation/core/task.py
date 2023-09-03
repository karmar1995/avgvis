class Task:
    def __init__(self, source, destination):
        self.__source = source
        self.__destination = destination

    def source(self):
        return self.__source

    def destination(self):
        return self.__destination

    def __str__(self):
        return "[{}, {}]".format(self.__source, self.__destination)

