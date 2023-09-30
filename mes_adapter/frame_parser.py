from frames_utils.frame import *


class MesFrameBuilder(FrameBuilder):
    def __init__(self):
        super().__init__(GenericFrameDescription())


class MesFrameParser:
    def __init__(self):
        self.__data = None
        self.__mesFrameDescription = GenericFrameDescription()

    def onFrameReceived(self, frame):
        self.__data = frame
        return self.__parse()

    def __parse(self):
        try:
            return FrameParser(self.__mesFrameDescription).parse(self.__data)
        except Exception as e:
            return Frame().addField('id', -1)

    def __validate(self, totalLength):
        pass
        # todo: uncomment in production
        # if len(self.__data) != totalLength:
        #     raise Exception("Invalid frame!")

