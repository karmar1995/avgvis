from model.visobjects_registry import VisObjectsRegistry
from model.visobject_factory import VisObjectFactory
from model.events_controller import EventsController
from model.events_hub import EventsHub
from model.map import Map
from model.error_sink import ErrorSink
from collections import namedtuple

MapData = namedtuple("MapData", 'x y width height')


class InitData:
    def __init__(self, mapData):
        self.mapData = mapData


class CompositionRoot:
    def __init__(self):
        self.__objectsRegistry = VisObjectsRegistry()
        self.__objectsFactory = VisObjectFactory()
        self.__map = Map(self.__objectsRegistry)
        self.__eventsHub = EventsHub()
        self.__errorSink = ErrorSink()
        self.__eventsController = EventsController(self.__objectsRegistry, self.__eventsHub, self.__map, self.__errorSink)
        self.__view = None

    def setView(self, view):
        self.__view = view

    def initialize(self, initData):
        mapData = initData.mapData
        self.__map.initialize(mapData.x, mapData.y, mapData.height, mapData.width, self.__view)
        return True

    def objectsIdsGenerator(self):
        return self.__objectsRegistry.idsGenerator()

    def eventsHub(self):
        return self.__eventsHub

    def addErrorListener(self, errorListener):
        self.__errorSink.addListener(errorListener)

    def startProcessingEvents(self):
        self.__eventsHub.start()
        