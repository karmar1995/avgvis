class VisObjectData:
    def __init__(self, objectId, x, y, rotation):
        self.objectId = objectId
        self.x = x
        self.y = y
        self.rotation = rotation


class VisObject:
    def __init__(self, visObjectData):
        self.__objectId = visObjectData.objectId
        self.__x = visObjectData.x
        self.__y = visObjectData.y
        self.__rotation = visObjectData.rotation

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

    def setPosition(self, x, y):
        self.setX(x)
        self.setY(y)

    def setRotation(self, rotation):
        self.__rotation = rotation

    def updateProperties(self, properties):
        pass

    def getObjectId(self):
        return self.__objectId

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def rotation(self):
        return self.__rotation
