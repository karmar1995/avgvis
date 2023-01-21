class VisObjectsRegistry:
    def __init__(self):
        self.visObjectsById = {}

    def registerObject(self, visObject):
        self.visObjectsById[visObject.getObjectId()] = visObject

    def unregisterObject(self, visObjectId):
        if self.object(visObjectId):
            del self.visObjectsById[visObjectId]

    def object(self, objectId):
        try:
            return self.visObjectsById[objectId]
        except KeyError:
            return None


