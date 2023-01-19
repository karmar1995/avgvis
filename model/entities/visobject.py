class VisObjectData:
    def __init__(self, id, x, y, rotation):
        self.id = id
        self.x = x
        self.y = y
        self.rotation = rotation


class VisObject:
    def __init__(self, visObjectData):
        self.id = visObjectData.id
        self.x = visObjectData.x
        self.y = visObjectData.y
        self.rotation = visObjectData.rotation

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setRotation(self, rotation):
        self.rotation = rotation

    def id(self):
        return self.id
