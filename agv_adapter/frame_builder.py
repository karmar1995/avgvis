import copy


class FrameBuilder:
    def __init__(self):
        self.__frame = None
        self.__nodeToVisit = None

    def startFrame(self):
        self.__frame = str()
        return self

    def withNodeToVisit(self, nodeNumber):
        self.__frame += str(nodeNumber)
        return self

    def consumeFrame(self):
        frame = copy.deepcopy(self.__frame)
        self.__frame = None
        self.__nodeToVisit = None
        return frame