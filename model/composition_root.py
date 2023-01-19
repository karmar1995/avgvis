from visobjects_registry import VisObjectsRegistry
from visobject_factory import VisObjectFactory


class InitData:
    def __init__(self, view):
        self.view = view
        self.eventSources = list()

    def addEventSource(self, source):
        self.eventSources.append(source)


class CompositionRoot:
    def __init__(self):
        self.objectsRegistry = VisObjectsRegistry()
        self.objectsFactory = VisObjectFactory()
        self.view = None
        self.eventSources = list()

    def initialize(self, initData):
        self.view = initData.view
        self.eventSources = initData.eventSources

