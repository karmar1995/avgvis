from opc_adapter.opc_events_source import OpcEventSource


class OpcObject:

    def __init__(self, dataAccess, objectId, width, height, type):
        self.__opcEventSource = OpcEventSource(dataAccess, objectId)
        self.__width = width
        self.__height = height
        self.__type = type

    def registerObject(self):
        self.__opcEventSource.sendRegisterObjectEvent(type=self.__type,
                                                      properties={},
                                                      height=self.__height,
                                                      width=self.__width)
