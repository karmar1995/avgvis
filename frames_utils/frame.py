import copy
from dataclasses import dataclass


@dataclass
class FrameField:
    startingByte: int
    length: int
    type: type
    endianStyle: str
    name: str


dataLengthByFrameId = {
    5000: 32
}


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

    def parse(self, data):
        frame = Frame()
        frameId = None
        for frameField in self.__description.fields:
            fieldName = frameField.name
            field = self.__parseField(data, frameField, frameId)
            if fieldName == 'id':
                frameId = field
            frame.addField(fieldName, field)
        return frame

    def __parseField(self, data, field, frameId):
        length = field.length
        if length == VARIABLE_LENGTH_MARK and frameId is not None:
            length = dataLengthByFrameId[frameId]
        tmp = copy.deepcopy(data[field.startingByte: (field.startingByte + length)])
        if field.type == bytes:
            return tmp
        return field.type.from_bytes(tmp, field.endianStyle)


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

    def __buildField(self, frameField, frameBytes):
        value = self.__fields[frameField.name]
        length = frameField.length
        if length == VARIABLE_LENGTH_MARK:
            length = dataLengthByFrameId[self.__fields['id']]
        if type(value) != bytes:
            bytesValue = value.to_bytes(length, frameField.endianStyle)
        else:
            bytesValue = value
        frameBytes.extend(bytesValue)


class GenericFrameDescription(FrameDescription):
    beginningField = FrameField(startingByte=0, length=3, type=int, endianStyle='big', name='beginning')
    emptyField = FrameField(startingByte=3, length=1, type=int, endianStyle='big', name='empty')
    idField = FrameField(startingByte=4, length=2, type=int, endianStyle='big', name='id')
    statusField = FrameField(startingByte=6, length=2, type=int, endianStyle='big', name='status')
    timestampField = FrameField(startingByte=8, length=12, type=DtlDateTime, endianStyle='big', name='timestamp')
    numberField = FrameField(startingByte=20, length=2, type=int, endianStyle='big', name='number')
    versionField = FrameField(startingByte=22, length=2, type=int, endianStyle='big', name='version')
    lengthField = FrameField(startingByte=24, length=2, type=int, endianStyle='big', name='length')
    dataField = FrameField(startingByte=28, length=VARIABLE_LENGTH_MARK, type=bytes, endianStyle='big', name='data')
    endingField = FrameField(startingByte=VARIABLE_LENGTH_MARK, length=3, type=int, endianStyle='big', name='ending')

    def __init__(self):
        super().__init__()
        self.addField(GenericFrameDescription.beginningField).\
            addField(GenericFrameDescription.emptyField).\
            addField(GenericFrameDescription.idField). \
            addField(GenericFrameDescription.statusField).\
            addField(GenericFrameDescription.timestampField).\
            addField(GenericFrameDescription.numberField). \
            addField(GenericFrameDescription.versionField).\
            addField(GenericFrameDescription.lengthField).\
            addField(GenericFrameDescription.dataField).addField(GenericFrameDescription.endingField)


class Frame5000Description(FrameDescription):
    timestampField = FrameField(startingByte=0, length=12, type=DtlDateTime, endianStyle='big', name='timestamp')
    productionOrderIdField = FrameField(startingByte=12, length=2, type=int, endianStyle='big', name='productionOrderId')
    orderPriorityField = FrameField(startingByte=14, length=2, type=int, endianStyle='big', name='orderPriority')
    sourcePointIdField = FrameField(startingByte=16, length=2, type=int, endianStyle='big', name='sourcePointId')
    destinationPointIdField = FrameField(startingByte=18, length=2, type=int, endianStyle='big', name='destinationPointId')
    requiredOutputTimeField = FrameField(startingByte=20, length=12, type=DtlDateTime, endianStyle='big', name='requiredOutputTime')

    def __init__(self):
        super().__init__()
        self.addField(Frame5000Description.timestampField).\
            addField(Frame5000Description.productionOrderIdField).\
            addField(Frame5000Description.orderPriorityField). \
            addField(Frame5000Description.sourcePointIdField).\
            addField(Frame5000Description.destinationPointIdField).\
            addField(Frame5000Description.requiredOutputTimeField)
