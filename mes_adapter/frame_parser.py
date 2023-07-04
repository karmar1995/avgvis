import copy
from dataclasses import dataclass
from mes_adapter.test_data import getTestFrame


VARIABLE_LENGTH_MARK = -1


@dataclass
class FrameField:
    startingByte: int
    length: int


class DtlDateTime:
    def __init__(self, year, month, day, dayOfWeek, hour, minute, second, millisecond):
        self.year = year
        self.month = month
        self.day = day
        self.dayOfWeek = dayOfWeek
        self.hour = hour
        self.minute = minute
        self.second = second
        self.millisecond = millisecond

    @staticmethod
    def from_bytes(_bytes):
        year = int.from_bytes(_bytes[0: 2], 'big')
        month = int.from_bytes(_bytes[2: 3], 'big')
        day = int.from_bytes(_bytes[3: 4], 'big')
        dayOfWeek = int.from_bytes(_bytes[4: 5], 'big')
        hour = int.from_bytes(_bytes[5: 6], 'big')
        minute = int.from_bytes(_bytes[6:7], 'big')
        second = int.from_bytes(_bytes[7:8], 'big')
        millisecond = int.from_bytes(_bytes[8: 12], 'big')
        return DtlDateTime(year, month, day, dayOfWeek, hour, minute, second, millisecond)


beginningField = FrameField(startingByte=0, length=3)
emptyField = FrameField(startingByte=3, length=1)
idField = FrameField(startingByte=4, length=2)
statusField = FrameField(startingByte=6, length=2)
timestampField = FrameField(startingByte=8,length=12)
numberField = FrameField(startingByte=20,length=2)
versionField = FrameField(startingByte=22, length=2)
lengthField = FrameField(startingByte=24, length=2)
dataField = FrameField(startingByte=28, length=VARIABLE_LENGTH_MARK)
endingField = FrameField(startingByte=VARIABLE_LENGTH_MARK, length=3)

dataLengthByFrameId = {
    5000: 32
}


class FrameParser:
    def __init__(self):
        self.__data = None

    def onFrameReceived(self, frame):
        self.__data = frame
        self.__parse()
        for i in range(len(frame)):
            print(frame[i])

    def __parse(self):
        beginning = self.__parseField(beginningField)
        id = int.from_bytes(self.__parseField(idField), 'big')
        status = int.from_bytes(self.__parseField(statusField), 'big')
        timestamp = DtlDateTime.from_bytes(self.__parseField(timestampField))
        number = int.from_bytes(self.__parseField(numberField), 'big')
        version = int.from_bytes(self.__parseField(versionField), 'big')
        length = int.from_bytes(self.__parseField(lengthField), 'big')
        currentFrameDataField = copy.deepcopy(dataField)
        currentFrameDataField.length = dataLengthByFrameId[id]
        data = self.__parseField(currentFrameDataField)
        currentFrameEndingField = copy.deepcopy(endingField)
        currentFrameEndingField.startingIndex = currentFrameDataField.startingByte + currentFrameDataField.length - 2
        ending = self.__parseField(currentFrameEndingField)
        self.__validate(length)
        return beginning, id, status, timestamp, number, version, length, data, ending

    def __parseField(self, field):
        return copy.deepcopy(self.__data[field.startingByte: (field.startingByte + field.length)])

    def __validate(self, totalLength):
        if len(self.__data) != totalLength:
            raise Exception("Invalid frame!")

