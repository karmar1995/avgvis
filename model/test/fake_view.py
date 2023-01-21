from model.abstract_view import AbstractView
from copy import deepcopy


class FakeView(AbstractView):
    def __init__(self):
        super().__init__()
        self.renderedMap = None
        self.renderedObjects = list()
        self.knownObjects = dict()

    def renderObject(self, visObject):
        if visObject.getObjectId() not in self.knownObjects:
            self.knownObjects[visObject.getObjectId()] = visObject
        self.renderedObjects.append(deepcopy(visObject))

    def cleanupObject(self, visObjectId):
        if visObjectId in self.knownObjects:
            self.knownObjects.pop(visObjectId)
        else:
            raise "Unknown object: " + str(visObjectId)

    def showCollision(self, collidingObjects):
        pass

    def renderMap(self, visMap):
        self.renderedMap = visMap

    def lastRenderedObject(self):
        return self.renderedObjects[len(self.renderedObjects)-1]

