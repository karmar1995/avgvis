import threading
import time
import random

from model.entities.visobject import VisObject, VisObjectData


class FakeModelMap:
    def __init__(self, mapSize):
        self.__x = mapSize.x
        self.__y = mapSize.y
        self.__width = mapSize.width
        self.__height = mapSize.height

    def x(self):
        return self.__x

    def y(self):
        return self.__y

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def size(self):
        return self.width(), self.height()


class UpdatesGeneratingThread:
    def __init__(self, abstractView, objectsList, generationInterval, modelMap):
        self.__thread = None
        self.__abstractView = abstractView
        self.__objectsList = objectsList
        self.__stopped = False
        self.__generationInterval = generationInterval
        self.__modelMap = modelMap

    def start(self):
        self.__thread = threading.Thread(target=self.__generateUpdates)
        self.__thread.daemon = True
        self.__thread.start()

    def stop(self):
        self.__stopped = True
        self.__thread.join()
        self.__thread = None

    def __generateUpdates(self):
        while not self.__stopped:
            for objectId in self.__objectsList:
                self.__generateObjectUpdate(objectId)
            time.sleep(self.__generationInterval)

    def __generateObjectUpdate(self, objectId):
        x = random.randint(self.__modelMap.x(), self.__modelMap.x() + self.__modelMap.width())
        y = random.randint(self.__modelMap.y(), self.__modelMap.y() + self.__modelMap.height())
        rotation = random.randint(0, 360)
        objectWidth = 2
        objectHeight = 2
        objectToUpdate = VisObject(VisObjectData(objectId, x, y, rotation, objectWidth, objectHeight))
        self.__abstractView.renderObject(objectToUpdate)


class FakeBusinessRules:
    def __init__(self, objectIds, updatesInterval, mapSize):
        self.modelView = None
        self.userView = None
        self.updatesGenerator = None
        self.objectsIds = objectIds
        self.updatesInterval = updatesInterval
        self.fakeModelMap = FakeModelMap(mapSize)

    def setViewInterfaces(self, viewInterfaces):
        self.modelView = viewInterfaces.modelView
        self.userView = viewInterfaces.userView

    def initialize(self):
        self.updatesGenerator = UpdatesGeneratingThread(self.modelView,
                                                        self.objectsIds,
                                                        self.updatesInterval,
                                                        self.fakeModelMap)
        self.modelView.renderMap(self.fakeModelMap)

    def startApp(self):
        self.updatesGenerator.start()

