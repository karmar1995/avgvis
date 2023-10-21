from frames_utils.frame import *


class MesFrameBuilder(FrameBuilder):
    def __init__(self):
        super().__init__(GenericFrameDescription())


class MesFrameParser:
    def __init__(self):
        self.__data = None

    def onFrameReceived(self, frame):
        self.__data = frame
        return self.__parse()

    def __parse(self):
        try:
            genericFrameParser = FrameParser(GenericFrameDescription())
            frameData = genericFrameParser.parse(self.__data).data
            return FrameParser(Frame5000Description()).parse(frameData)
        except Exception as e:
            return Frame().addField('productionOrderId', -1)

    def __validate(self, totalLength):
        pass
        # todo: uncomment in production
        # if len(self.__data) != totalLength:
        #     raise Exception("Invalid frame!")

