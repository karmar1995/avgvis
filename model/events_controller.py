from model.entities.agv import *


class EventsController:
    def __init__(self, visobjectsRegistry, eventsSource, map, errorSink):
        self.visobjectsRegistry = visobjectsRegistry
        self.eventsSource = eventsSource
        self.eventsSource.addHandler(self)
        self.objectsObservers = list()
        self.map = map
        self.errorSink = errorSink
        self.registerObjectObserver(self.map)

    def registerObjectObserver(self, observer):
        self.objectsObservers.append(observer)

    def broadcastObjectsChanged(self, changedObjects):
        for observer in self.objectsObservers:
            observer.onChangedObjects(changedObjects)

    def __del__(self):
        self.eventsSource.removeHandler(self)

    def onRegisterObject(self, registerObjectEvent):
        newObjectId = registerObjectEvent.objectId
        if not self.visobjectsRegistry.object(newObjectId):
            if registerObjectEvent.type == 'AGV':
                AGV_HEIGHT = 3  # #todo: read from configuration
                AGV_WIDTH = 4  # #todo: read from configuration
                visObjectData = VisObjectData(newObjectId, 0, 0, 0, AGV_WIDTH, AGV_HEIGHT)
                agvObjectData = AgvObjectData(visObjectData, registerObjectEvent.properties['battery'])
                self.visobjectsRegistry.registerObject(AgvObject(agvObjectData))
                self.broadcastObjectsChanged([newObjectId])
        else:
            self.errorSink.logError("Object %s already exists!".format(newObjectId))

    def onUpdateObjectPosition(self, updateObjectPositionEvent):
        objectId = updateObjectPositionEvent.objectId
        x = updateObjectPositionEvent.x
        y = updateObjectPositionEvent.y

        visObject = self.visobjectsRegistry.object(objectId)
        if visObject:
            if self.map.isValidPosition(x, y):
                visObject.setPosition(x, y)
                self.broadcastObjectsChanged([objectId])
            else:
                self.errorSink.logError("Invalid position: (%s, %s)".format(x, y))
        else:
            self.errorSink.logError("Object %s does not exists!".format(objectId))

    def onUpdateObjectRotation(self, updateObjectRotationEvent):
        objectId = updateObjectRotationEvent.objectId
        rotation = updateObjectRotationEvent.rotation % 360

        visObject = self.visobjectsRegistry.object(objectId)
        if visObject:
            visObject.setRotation(rotation)
            self.broadcastObjectsChanged([objectId])
        else:
            self.errorSink.logError("Object %s does not exists!".format(objectId))

    def onUpdateObjectProperties(self, updateObjectPropertiesEvent):
        objectId = updateObjectPropertiesEvent.objectId
        properties = updateObjectPropertiesEvent.properties

        visObject = self.visobjectsRegistry.object(objectId)
        if visObject:
            visObject.updateProperties(properties)
            self.broadcastObjectsChanged([objectId])
        else:
            self.errorSink.logError("Object %s does not exists!".format(objectId))

    def onUnregisterObject(self, unregisterObjectEvent):
        objectId = unregisterObjectEvent.objectId
        self.visobjectsRegistry.unregisterObject(objectId)
        self.broadcastObjectsChanged([objectId])

