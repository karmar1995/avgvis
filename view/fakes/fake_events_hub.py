import threading
import time
import random

from model.entities.visobject import VisObject, VisObjectData


class FakeObject:
    def __init__(self, objectId, x, y):
        self.objectId = objectId
        self.x = x
        self.y = y
        self.rotation = 0

    def properties(self):
        res = dict()
        res['id'] = self.objectId
        res['x'] = self.x
        res['y'] = self.y
        res['battery'] = random.randint(0, 100)
        return res


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
        self.__objectsList = list()
        self.__stopped = False
        self.__generationInterval = generationInterval
        self.__modelMap = modelMap
        self.__errorsListeners = list()
        for objectId in objectsList:
            self.__objectsList.append(FakeObject(objectId, self.__modelMap.x(), self.__modelMap.y()))

    def start(self):
        self.__thread = threading.Thread(target=self.__generateUpdates)
        self.__thread.daemon = True
        self.__thread.start()

    def stop(self):
        self.__stopped = True
        self.__thread.join()
        self.__thread = None

    def addErrorListener(self, listener):
        self.__errorsListeners.append(listener)

    def __generateUpdates(self):
        while not self.__stopped:
            for object in self.__objectsList:
                self.__generateObjectUpdate(object)
            time.sleep(self.__generationInterval)

    def __generateObjectUpdate(self, object):
        self.__logInformation("Moving object: {} to position: {} {}".format(object.objectId, object.x, object.y))
        objectWidth = 2
        objectHeight = 2
        objectToUpdate = VisObject(VisObjectData(object.objectId, object.x, object.y, 0, objectWidth, objectHeight, object.properties()))
        self.__abstractView.renderObject(objectToUpdate)
        if object.x >= self.__modelMap.width():
            object.y += self.__modelMap.height() / 10
            object.x = self.__modelMap.x()
        else:
            object.x += self.__modelMap.width() / 20

    def __logError(self, message):
        for listener in self.__errorsListeners:
            listener.logError(message)

    def __logInformation(self, message):
        for listener in self.__errorsListeners:
            listener.logInformation(message)


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

    def addErrorsListener(self, listener):
        self.updatesGenerator.addErrorListener(listener)
