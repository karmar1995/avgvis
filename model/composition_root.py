from model.visobjects_registry import VisObjectsRegistry
from model.visobject_factory import VisObjectFactory
from model.events_controller import EventsController
from model.events_hub import EventsHub
from model.map import Map
from model.error_sink import ErrorSink
from collections import namedtuple

MapData = namedtuple("MapData", 'x y width height')


class InitData:
    def __init__(self, view, errorListener, mapData):
        self.view = view
        self.eventSources = list()
        self.errorListener = errorListener
        self.mapData = mapData

    def addEventSource(self, source):
        self.eventSources.append(source)


class CompositionRoot:
    def __init__(self):
        self.objectsRegistry = VisObjectsRegistry()
        self.objectsFactory = VisObjectFactory()
        self.map = Map(self.objectsRegistry)
        self.eventsHub = EventsHub()
        self.errorSink = ErrorSink()
        self.eventsController = EventsController(self.objectsRegistry, self.eventsHub, self.map, self.errorSink)

    def initialize(self, initData):
        mapData = initData.mapData
        self.map.initialize(mapData.x, mapData.y, mapData.height, mapData.width, initData.view)
        for eventSource in initData.eventSources:
            self.eventsHub.addEventsSource(eventSource)
        self.errorSink.addListener(initData.errorListener)
