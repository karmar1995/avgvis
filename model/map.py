class Map:
    def __init__(self, objectsRegistry):
        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.view = None
        self.objectsRegistry = objectsRegistry
        self.collidedObjects = list()

    def initialize(self, x, y, width, height, view):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.view = view
        self.view.renderMap(self)

    def onChangedObjects(self, changedObjects):
        for changedObject in changedObjects:
            self.__onObjectChanged(changedObject)

    def topLeft(self):
        return self.x, self.y

    def bottomRight(self):
        return self.x + self.width, self.y + self.height

    def isValidPosition(self, x, y):
        if x >= self.topLeft()[0] and y >= self.topLeft()[1]:
            if x <= self.bottomRight()[0] and y <= self.bottomRight()[1]:
                return True
        return False

    def __onObjectChanged(self, visObjectId):
        visObject = self.objectsRegistry.object(visObjectId)
        if visObject:
            self.view.renderObject(visObject)
            self.__updateCollisions()
        else:
            self.view.cleanupObject(visObjectId)

    def __updateCollisions(self):
        if len(self.collidedObjects) > 0:
            self.view.showCollision(self.collidedObjects)
