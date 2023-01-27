from model.abstract_event_source import AbstractEventSource
from model.events import *


class OpcEventSource(AbstractEventSource):

    def __init__(self, dataAccess, objectId):
        super().__init__()
        self.__handlers = dict()
        self.__dataAccess = dataAccess
        self.__id = objectId

    def addHandler(self, handler):
        self.__handlers[id(handler)] = handler

    def removeHandler(self, handler):
        del self.__handlers[id(handler)]

    def sendRegisterObjectEvent(self, type, properties, width, height):
        registerObjectEvent = RegisterObjectEvent(objectId=self.__id,
                                                  type=type,
                                                  properties=properties,
                                                  width=width,
                                                  height=height)
        self.__broadcastEvent(registerObjectEvent)

    def __broadcastEvent(self, event):
        for handlerId in self.__handlers:
            self.__handlers[handlerId].onEvent(event)


