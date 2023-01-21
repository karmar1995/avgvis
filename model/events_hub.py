from model.abstract_event_source import AbstractEventSource
from model.abstract_event_handler import AbstractEventHandler
from model.events import *


class EventsHub(AbstractEventSource, AbstractEventHandler):

    def __init__(self):
        super().__init__()
        self.sources = list()
        self.handlers = dict()
        self.handlersMap = dict()
        self.handlersMap[RegisterObjectEvent] = self.__onRegisterObjectEvent
        self.handlersMap[UpdateObjectPositionEvent] = self.__onUpdateObjectPositionEvent
        self.handlersMap[UpdateObjectRotationEvent] = self.__onUpdateObjectRotationEvent
        self.handlersMap[UpdateObjectPropertiesEvent] = self.__onUpdateObjectPropertiesEvent
        self.handlersMap[UnregisterObjectEvent] = self.__onUnregisterObjectEvent

    def __del__(self):
        for source in self.sources:
            source.removeHandler(self)

    def addEventsSource(self, newSource):
        self.sources.append(newSource)
        newSource.addHandler(self)

    def addHandler(self, handler):
        self.handlers[id(handler)] = handler

    def removeHandler(self, handler):
        self.handlers.pop(id(handler))

    def onEvent(self, event):
        self.handlersMap[type(event)](event)

    def __onRegisterObjectEvent(self, event):
        for handlerId in self.handlers:
            self.handlers[handlerId].onRegisterObject(event)

    def __onUpdateObjectPositionEvent(self, event):
        for handlerId in self.handlers:
            self.handlers[handlerId].onUpdateObjectPosition(event)

    def __onUpdateObjectRotationEvent(self, event):
        for handlerId in self.handlers:
            self.handlers[handlerId].onUpdateObjectRotation(event)

    def __onUpdateObjectPropertiesEvent(self, event):
        for handlerId in self.handlers:
            self.handlers[handlerId].onUpdateObjectProperties(event)

    def __onUnregisterObjectEvent(self, event):
        for handlerId in self.handlers:
            self.handlers[handlerId].onUnregisterObject(event)
