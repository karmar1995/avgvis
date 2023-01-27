from model.abstract_event_source import AbstractEventSource
from model.abstract_event_handler import AbstractEventHandler
from model.events import *


class FakeEventsSource(AbstractEventSource):
    def __init__(self):
        super().__init__()
        self.handlers = dict()

    def addHandler(self, handler):
        if issubclass(type(handler), AbstractEventHandler):
            self.handlers[id(handler)] = handler
        else:
            raise Exception("Not a handler!")

    def removeHandler(self, handler):
        if id(handler) not in self.handlers:
            raise Exception("Unregistering non-existing handler!")
        else:
            self.handlers.pop(id(handler))

    def registerAgvObject(self, objectId):
        event = RegisterObjectEvent(objectId=objectId, type="AGV", properties={"battery": "10%"}, width=4, height=3)
        self.__broadcastEvent(event)

    def updateObjectPosition(self, objectId, x, y):
        event = UpdateObjectPositionEvent(objectId=objectId, x=x, y=y)
        self.__broadcastEvent(event)

    def updateObjectRotation(self, objectId, rotation):
        event = UpdateObjectRotationEvent(objectId=objectId, rotation=rotation)
        self.__broadcastEvent(event)

    def updateObjectProperties(self, objectId, properties):
        event = UpdateObjectPropertiesEvent(objectId=objectId, properties=properties)
        self.__broadcastEvent(event)

    def unregisterObject(self, objectId):
        self.__broadcastEvent(UnregisterObjectEvent(objectId=objectId))

    def __broadcastEvent(self, event):
        for handlerId in self.handlers:
            self.handlers[handlerId].onEvent(event)

