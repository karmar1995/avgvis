import copy
from dataclasses import dataclass


VARIABLE_LENGTH_MARK = -1


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
    def from_bytes(_bytes, byteorder):
        year = int.from_bytes(_bytes[0: 2], byteorder)
        month = int.from_bytes(_bytes[2: 3], byteorder)
        day = int.from_bytes(_bytes[3: 4], byteorder)
        dayOfWeek = int.from_bytes(_bytes[4: 5], byteorder)
        hour = int.from_bytes(_bytes[5: 6], byteorder)
        minute = int.from_bytes(_bytes[6:7], byteorder)
        second = int.from_bytes(_bytes[7:8], byteorder)
        millisecond = int.from_bytes(_bytes[8: 12], byteorder)
        return DtlDateTime(year, month, day, dayOfWeek, hour, minute, second, millisecond)

    def to_bytes(self, unusedLength, byteorder):
        res = bytearray()
        res.extend(self.year.to_bytes(2, byteorder))
        res.extend(self.month.to_bytes(1, byteorder))
        res.extend(self.day.to_bytes(1, byteorder))
        res.extend(self.dayOfWeek.to_bytes(1, byteorder))
        res.extend(self.hour.to_bytes(1, byteorder))
        res.extend(self.minute.to_bytes(1, byteorder))
        res.extend(self.second.to_bytes(1, byteorder))
        res.extend(self.millisecond.to_bytes(4, byteorder))
        return bytes(res)


@dataclass
class FrameField:
    startingByte: int
    length: int
    type: type
    endianStyle: str
    name: str


class Frame:
    def addField(self, name, value):
        self.__dict__[name] = value
        return self


class FrameDescription:
    def __init__(self):
        self.fields = list()

    def addField(self, field: FrameField):
        self.fields.append(field)
        return self


class FrameParser:
    def __init__(self, frameDescription: FrameDescription):
        self.__description = frameDescription

    #todo: support variable length
    def parse(self, data):
        frame = Frame()
        for frameField in self.__description.fields:
            fieldName = frameField.name
            field = self.__parseField(data, frameField)
            frame.addField(fieldName, field)
        return frame

    def __parseField(self, data, field):
        return field.type.from_bytes(copy.deepcopy(data[field.startingByte: (field.startingByte + field.length)]), field.endianStyle)


class FrameBuilder:

    def __init__(self, frameDescription: FrameDescription):
        self.__description = frameDescription
        self.__fields = dict()

    def setFieldValue(self, name, value):
        self.__fields[name]=value
        return self

    def build(self):
        frameBytes = bytearray()
        for frameField in self.__description.fields:
            self.__buildField(frameField, frameBytes)
        return bytes(frameBytes)

    #todo: support variable length
    def __buildField(self, frameField, frameBytes):
        value = self.__fields[frameField.name]
        length = frameField.length
        if length == VARIABLE_LENGTH_MARK:
            length = 32
        bytesValue = value.to_bytes(length, frameField.endianStyle)
        frameBytes.extend(bytesValue)
