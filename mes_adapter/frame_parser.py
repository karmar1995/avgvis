from frames_utils.frame import *



beginningField = FrameField(startingByte=0, length=3, type=int, endianStyle='big', name='beginning')
emptyField = FrameField(startingByte=3, length=1, type=int, endianStyle='big', name='empty')
idField = FrameField(startingByte=4, length=2, type=int, endianStyle='big', name='id')
statusField = FrameField(startingByte=6, length=2, type=int, endianStyle='big', name='status')
timestampField = FrameField(startingByte=8,length=12, type=DtlDateTime, endianStyle='big', name='timestamp')
numberField = FrameField(startingByte=20,length=2, type=int, endianStyle='big', name='number')
versionField = FrameField(startingByte=22, length=2, type=int, endianStyle='big', name='version')
lengthField = FrameField(startingByte=24, length=2, type=int, endianStyle='big', name='length')
dataField = FrameField(startingByte=28, length=VARIABLE_LENGTH_MARK, type=int, endianStyle='big', name='data')
endingField = FrameField(startingByte=VARIABLE_LENGTH_MARK, length=3, type=int, endianStyle='big', name='ending')

dataLengthByFrameId = {
    5000: 32
}

def getMesFrameDescription():
    return FrameDescription(). \
        addField(beginningField).addField(emptyField).addField(idField). \
        addField(statusField).addField(timestampField).addField(numberField). \
        addField(versionField).addField(lengthField).addField(dataField).addField(endingField)


class MesFrameBuilder(FrameBuilder):
    def __init__(self):
        super().__init__(getMesFrameDescription())


class MesFrameParser:
    def __init__(self):
        self.__data = None
        self.__mesFrameDescription = getMesFrameDescription()

    def onFrameReceived(self, frame):
        self.__data = frame
        return self.__parse()

    def __parse(self):
        try:
            return FrameParser(self.__mesFrameDescription).parse(self.__data)
        except Exception as e:
            print("MesFrameParser, frame parsing error: {}".format(str(e)))
            return Frame().addField('id', -1)

    def __validate(self, totalLength):
        pass
        # todo: uncomment in production
        # if len(self.__data) != totalLength:
        #     raise Exception("Invalid frame!")

